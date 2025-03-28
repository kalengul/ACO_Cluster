import random as rnd
from all_functions import *

import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
from datetime import datetime
import win32com.client  # Для загрузки из Excel

class Individ():
    """ Класс одного индивида в популяции"""
    def __init__(self, start, end, mutationSteps, function):
        # пределы поиска минимума
        self.start = start
        self.end = end
        # позиция индивида по Х (первый раз определяется случайно)
        self.x = rnd.triangular(self.start, self.end)
        # позиция индивида по Y (первый раз определяется случайно)
        self.y = rnd.triangular(self.start, self.end)
        # значение функции, которую реализует индивид
        self.score = 0
        # передаем функцию для оптимизации
        self.function = function
        # количество шагов мутации
        self.mutationSteps = mutationSteps
        # считаем сразу значение функции
        self.calculateFunction()


    def calculateFunction(self):
        """ Функция для пересчета значения значение в индивиде"""
        self.score = self.function(self.x, self.y)

    def mutate(self):
        """ Функция для мутации индивида"""
        # задаем отклонение по Х
        delta = 0
        for i in range(1, self.mutationSteps+1):
            if rnd.random() < 1 / self.mutationSteps:
                delta += 1 / (2 ** i)
        if rnd.randint(0, 1):
            delta = self.end * delta
        else:
            delta = self.start * delta
        self.x += delta
        # ограничим наших индивидом по Х
        if self.x < 0:
            self.x = max(self.x, self.start)
        else:
            self.x = min(self.x, self.end)
        # отклонение по У
        delta = 0
        for i in range(1, self.mutationSteps+1):
            if rnd.random() < 1 / self.mutationSteps:
                delta += 1 / (2 ** i)
        if rnd.randint(0, 1):
            delta = self.end * delta
        else:
            delta = self.start * delta
        self.y += delta
        # ограничим наших индивидом по У
        if self.y < 0:
            self.y = max(self.y, self.start)
        else:
            self.y = min(self.y, self.end)

class Genetic:
    """ Класс, отвечающий за реализацию генетического алгоритма"""
    def __init__(self,
                 numberOfIndividums,
                 crossoverRate,
                 mutationSteps,
                 chanceMutations,
                 numberLives,
                 function,
                 start,
                 end,
                 goGif):
        # размер популяции
        self.numberOfIndividums = numberOfIndividums
        # какая часть популяции должна производить потомство (в % соотношении)
        self.crossoverRate = crossoverRate
        # количество шагов мутации
        self.mutationSteps = mutationSteps
        # шанс мутации особи
        self.chanceMutations = chanceMutations
        # сколько раз будет появляться новое поколение (сколько раз будет выполняться алгоритм)
        self.numberLives = numberLives
        # функция для поиска минимума
        self.function = function
        self.goGif=goGif

        # самое минимальное значение, которое было в нашей популяции
        self.bestScore = float('inf')
        # точка Х, У, где нашли минимальное значение
        self.xy = [float('inf'), float('inf')]
        # область поиска
        self.start = start
        self.end = end



    def crossover(self, parent1:Individ, parent2:Individ):
        """ Функция для скрещивания двух родителей

        :return: 2 потомка, полученных путем скрещивания
        """
        # создаем 2х новых детей
        child1 = Individ(self.start, self.end, self.mutationSteps, self.function)
        child2 = Individ(self.start, self.end, self.mutationSteps, self.function)
        # создаем новые координаты для детей
        alpha = rnd.uniform(0.01, 1)
        child1.x = parent1.x + alpha * (parent2.x - parent1.x)

        alpha = rnd.uniform(0.01, 1)
        child1.y = parent1.y + alpha * (parent2.y - parent1.y)

        alpha = rnd.uniform(0.01, 1)
        child2.x = parent1.x + alpha * (parent1.x - parent2.x)

        alpha = rnd.uniform(0.01, 1)
        child2.y = parent1.y + alpha * (parent1.y - parent2.y)
        return child1, child2


    def startGenetic(self):
        # будем собирать данные для gif
        dataForGIF = []

        # создаем стартовую популяцию
        pack = [self.start, self.end, self.mutationSteps,self.function]
        population = [Individ(*pack) for _ in range(self.numberOfIndividums)]

        # запускаем алгоритм
        for _ in range(self.numberLives):
            # сортируем популяцию по значению score
            population = sorted(population, key=lambda item: item.score, reverse=True)
            # данные для отрисовки GIF
            oneStepDataX = [individ.x for individ in population]
            oneStepDataY = [individ.y for individ in population]
            dataForGIF.append([oneStepDataX, oneStepDataY])

            # берем ту часть лучших индивидов, которых будем скрещивать между собой
            bestPopulation = population[:int(self.numberOfIndividums*self.crossoverRate)]
            # теперь проводим скрещивание столько раз, сколько было задано по коэффициенту кроссовера
            childs = []
            for individ1 in bestPopulation:
                # находим случайную пару для каждого индивида и скрещиваем
                individ2 = rnd.choice(bestPopulation)
                while individ1 == individ2:
                    individ2 = rnd.choice(bestPopulation)
                child1, child2 = self.crossover(individ1, individ2)
                childs.append(child1)
                childs.append(child2)
            # добавляем всех новых потомков в нашу популяцию
            population.extend(childs)

            for individ in population:
                # проводим мутации для каждого индивида
                individ.mutate()
                # пересчитываем значение функции для каждого индивида
                individ.calculateFunction()
            # отбираем лучших индивидов
            population = sorted(population, key=lambda item: item.score)
            population = population[:self.numberOfIndividums]
            # теперь проверим значение функции лучшего индивида на наилучшее значение экстремума
            if population[0].score < self.bestScore:
                self.bestScore = population[0].score
                self.xy = [population[0].x, population[0].y]

        # print("ОПТИМИЗИРОВАННОЕ ЗНАЧЕНИЕ ФУНКЦИИ:", self.xy, self.bestScore)
        if self.goGif:
            # рисуем gif
            fnames = []
            i = 0
            for x, y in dataForGIF:
                i += 1
                fname = f"g{i}.png"
                fig, (ax1, ax2) = plt.subplots(1, 2)
                fig.suptitle(f"Итерация: {i}")
                ax2.plot(x, y, 'bo')
                ax2.set_xlim(self.start, self.end)
                ax2.set_ylim(self.start, self.end)
                ax1.plot(x, y, 'bo')
                fig.savefig(fname)
                plt.close()

                fnames.append(fname)

            with imageio.get_writer('genetic.gif', mode='I') as writer:
                for filename in fnames:
                    image = imageio.imread(filename)
                    writer.append_data(image)

            for filename in set(fnames):
                os.remove(filename)

if __name__ == "__main__":
    mBest=0
    laBest=0
    mTime=0
    laTime=0
    NomPar = 0
    numberOfIndividums = 50
    crossoverRate = 0.5
    mutationSteps=150
    chanceMutations = 0.9
    numberLives = 2000
    textFunction = 'BenchEkliFunctionx10'
    NameFile =os.getcwd()+ '/genetic.xlsx'

    Individ_Lives = numberOfIndividums*numberLives
    MaxPar = 500
    ShagPar = 50

    Excel = win32com.client.Dispatch("Excel.Application")
    wb = Excel.Workbooks.Open(NameFile)
    sheet = wb.ActiveSheet
    sheet.Cells(1, 1).value = 'numberOfIndividums'
    sheet.Cells(1, 2).value = 'crossoverRate'
    sheet.Cells(1, 3).value = 'mutationSteps'
    sheet.Cells(1, 4).value = 'chanceMutations'
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
            a = Genetic(numberOfIndividums=numberOfIndividums, crossoverRate=crossoverRate, mutationSteps=mutationSteps,
                        chanceMutations=chanceMutations,
                        numberLives=numberLives, function=BenchEkliFunctionx10, start=-10, end=10, goGif=False)
            a.startGenetic()
            deltTime=(datetime.now()-StartTime).total_seconds()
            mTime=mTime+deltTime
            laTime = laTime + deltTime*deltTime
            mBest=mBest+a.bestScore
            laBest=laBest+a.bestScore*a.bestScore
            print(datetime.now(),NomStat,mBest,laBest, a.xy, a.bestScore)
            NomStat=NomStat+1
        mBest=mBest/KolIterStatistics
        laBest=laBest/KolIterStatistics
        print(mBest, laBest)
        sheet.Cells(NomPar + 2, 1).value = numberOfIndividums
        sheet.Cells(NomPar + 2, 2).value = crossoverRate
        sheet.Cells(NomPar + 2, 3).value = mutationSteps
        sheet.Cells(NomPar + 2, 4).value = chanceMutations
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