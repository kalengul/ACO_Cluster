# Импорт библиотек
from sys import float_info

import numpy as np
import matplotlib.pyplot as plt
from all_functions import *
import imageio.v2 as imageio
import os
from datetime import datetime
import win32com.client  # Для загрузки из Excel
# Определение тестовых функций
def schaffer(x, y):
    return 0.5 + (np.sin(x**2 - y**2)**2 - 0.5) / ((1 + 0.001*(x**2 + y**2))**2)

def ackley(x, y):
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2))) - np.exp(
        0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))
    ) + 20 + np.e

def rastrigin(x, y):
    return 20 + (x**2 - 10 * np.cos(2 * np.pi * x)) + (y**2 - 10 * np.cos(2 * np.pi * y))

# Реализация алгоритма имитации отжига
def simulated_annealing(func, bounds, max_iter=10000, T_max=1000, T_min=1e-8, alpha=0.99, goGif=True):
    x_curr = np.random.uniform(bounds[0], bounds[1])
    y_curr = np.random.uniform(bounds[0], bounds[1])
    f_curr = func(x_curr, y_curr)

    x_best, y_best, f_best = x_curr, y_curr, f_curr
    T = T_max
    trajectory = [(x_curr, y_curr)]  # Запись первой точки траектории

    for i in range(max_iter):
        x_new = np.clip(x_curr + np.random.uniform(-1, 1), bounds[0], bounds[1])
        y_new = np.clip(y_curr + np.random.uniform(-1, 1), bounds[0], bounds[1])
        f_new = func(x_new, y_new)

        trajectory.append((x_curr, y_curr))

        # Условие принятия новой точки
        if f_new < f_curr or np.exp((f_curr - f_new) / T) > np.random.rand():
            x_curr, y_curr, f_curr = x_new, y_new, f_new

            if f_new < f_best:
                x_best, y_best, f_best = x_new, y_new, f_new

        T *= alpha
        if T < T_min:
            break

    return x_best, y_best, f_best, trajectory
# Функция визуализации
def plot_function_and_trajectory(func, func_name, bounds=(-10, 10)):
    x = np.linspace(bounds[0], bounds[1], 400)
    y = np.linspace(bounds[0], bounds[1], 400)
    X, Y = np.meshgrid(x, y)
    Z = func(x, y)

    x_best, y_best, f_best, trajectory = simulated_annealing(func, bounds)
    trajectory = np.array(trajectory)

    plt.figure(figsize=(8, 6))
    plt.contour(x, y, func(*np.meshgrid(x, y)), levels=50, cmap='coolwarm')
    plt.plot(trajectory[:, 0], trajectory[:, 1], 'g-o', markersize=3, label="Путь")
    plt.scatter(trajectory[0, 0], trajectory[0, 1], color='blue', label='Начало', s=50, zorder=5)
    plt.scatter(x_best, y_best, color='red', s=50, label='Лучшая точка', zorder=5)
    plt.title(f"{func_name} Оптимизация с помощью SA")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

# ЗАДАНИЕ 1: Варирование параметров алгоритма и визуализация
def vary_parameters(func, bounds, params_list):
    results = []
    labels = []
    for T_max, alpha in params_list:
        _, _, f_best, _ = simulated_annealing(
            func, bounds, T_max=T_max, alpha=alpha
        )
        results.append(f_best)

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(params_list)), results, tick_label=[f"T={T_max}, α={alpha}" for T_max, alpha in params_list])
    plt.xlabel("Параметры (T_max, alpha)")
    plt.ylabel("Лучшее найденное значение функции")
    plt.title(f"Влияние параметров на оптимизацию функции {func.__name__}")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# ЗАДАНИЕ 2: Сбор статистики по разным начальным точкам
def gather_statistics(func, bounds, num_runs=500):
    best_values = []
    for _ in range(num_runs):
        # Каждый раз новая случайная начальная точка
        _, _, f_best, _ = simulated_annealing(func, bounds)
        best_values.append(f_best)

    avg_best = np.mean(best_values)
    std_best = np.std(best_values)

    plt.figure(figsize=(8, 6))
    plt.hist(best_values, bins=30, color='lightgreen', edgecolor='black')
    plt.xlabel('Лучшее найденное значение функции')
    plt.ylabel('Частота')
    plt.title(f"Статистика оптимизации функции {func.__name__}: среднее={avg_best:.6f}, стандартное отклонение={std_best:.6f}")
    plt.grid(True)
    plt.show()

    print(f"Функция: {func.__name__}\nСреднее значение: {avg_best:.6f}\nСтандартное отклонение: {std_best:.6f}")

if __name__ == "__main__":
    MaxZn=10000000000000000000
    mBest=0
    laBest=0
    mTime=0
    laTime=0
    NomPar = 0
    numberOfIndividums = 50
    T_max = 1000
    T_min=1e-8
    alpha=0.99
    numberLives = 2000
    textFunction = 'BenchRozenbrokx10'
    NameFile =os.getcwd()+ '/annealing.xlsx'

    Individ_Lives = numberOfIndividums*numberLives
    MaxPar = 500
    ShagPar = 50

    Excel = win32com.client.Dispatch("Excel.Application")
    wb = Excel.Workbooks.Open(NameFile)
    sheet = wb.ActiveSheet
    sheet.Cells(1, 1).value = 'numberOfIndividums'
    sheet.Cells(1, 2).value = 'T_max'
    sheet.Cells(1, 3).value = 'T_min'
    sheet.Cells(1, 4).value = 'alpha'
    sheet.Cells(1, 5).value = 'numberLives'
    sheet.Cells(1, 6).value = 'textFunction'
    sheet.Cells(1, 7).value = 'mBest'
    sheet.Cells(1, 8).value = 'laBest'
    sheet.Cells(1, 9).value = 'mTime'
    sheet.Cells(1, 10).value = 'laTime'


    Par=numberOfIndividums
    while Par<=MaxPar:

        numberOfIndividums=Par
        numberLives = int(Individ_Lives/numberOfIndividums)
        print('numberOfIndividums=',numberOfIndividums,'numberLives=',numberLives)

        mBest=0
        laBest=0
        mTime=0
        laTime=0
        NomStat = 0
        while NomStat<KolIterStatistics:
            StartTime = datetime.now()
            f_best=MaxZn
            for _ in range(numberOfIndividums):
                x_i, y_i, f_i, trajectory = simulated_annealing(func=BenchRozenbrokx10, bounds=(-10, 10), max_iter=numberLives, T_max=T_max, T_min=T_min, alpha=alpha,goGif=False)
                if f_best>f_i:
                    f_best=f_i
                    x_best=x_i
                    y_best=y_i
            deltTime=(datetime.now()-StartTime).total_seconds()
            mTime=mTime+deltTime
            laTime = laTime + deltTime*deltTime
            mBest=mBest+f_best
            laBest=laBest+f_best*f_best
            print(datetime.now(),NomStat,mBest,laBest, x_best, y_best, f_best)
            NomStat=NomStat+1
        mBest=mBest/KolIterStatistics
        laBest=laBest/KolIterStatistics
        print(mBest, laBest)
        sheet.Cells(NomPar + 2, 1).value = numberOfIndividums
        sheet.Cells(NomPar + 2, 2).value = T_max
        sheet.Cells(NomPar + 2, 3).value = T_min
        sheet.Cells(NomPar + 2, 4).value = alpha
        sheet.Cells(NomPar + 2, 5).value = numberLives
        sheet.Cells(NomPar + 2, 6).value = textFunction
        sheet.Cells(NomPar + 2, 7).value = mBest
        sheet.Cells(NomPar + 2, 8).value = laBest
        sheet.Cells(NomPar + 2, 9).value = mTime
        sheet.Cells(NomPar + 2, 10).value = laTime
        Par=Par+ShagPar
        NomPar=NomPar+1
    # сохраняем рабочую книгу
    wb.Save()
    # закрываем ее
    wb.Close()
    # закрываем COM объект
    Excel.Quit()



