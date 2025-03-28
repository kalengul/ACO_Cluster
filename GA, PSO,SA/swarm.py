from all_functions import *
from math import *
import random as rnd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
from datetime import datetime
import win32com.client  # Для загрузки из Excel



class Unit:

    def __init__(self, start, end, currentVelocityRatio, localVelocityRatio, globalVelocityRatio, function):
        # область поиска
        self.start = start
        self.end = end
        # коэффициенты для изменения скорости
        self.currentVelocityRatio = currentVelocityRatio
        self.localVelocityRatio = localVelocityRatio
        self.globalVelocityRatio = globalVelocityRatio
        # функция
        self.function = function
        # лучшая локальная позиция
        self.localBestPos = self.getFirsPos()
        self.localBestScore = self.function(*self.localBestPos)
        # текущая позиция
        self.currentPos = self.localBestPos[:]
        self.score = self.function(*self.localBestPos)
        # значение глобальной позиции
        self.globalBestPos = []
        # скорость
        self.velocity = self.getFirstVelocity()


    def getFirstVelocity(self):
        """ Метод для задания первоначальной скорости"""
        minval = -(self.end - self.start)
        maxval = self.end - self.start
        return [rnd.uniform(minval, maxval), rnd.uniform(minval, maxval)]

    def getFirsPos(self):
        """ Метод для получения начальной позиции"""
        return [rnd.uniform(self.start, self.end), rnd.uniform(self.start, self.end)]


    def nextIteration(self):
        """ Метод для нахождения новой позиции частицы"""
        # случайные данные для изменения скорости
        rndCurrentBestPosition = [rnd.random(), rnd.random()]
        rndGlobalBestPosition = [rnd.random(), rnd.random()]
        # делаем перерасчет скорости частицы исходя из всех введенных параметров
        velocityRatio = self.localVelocityRatio + self.globalVelocityRatio
        commonVelocityRatio = 2 * self.currentVelocityRatio / abs(2-velocityRatio-sqrt(velocityRatio ** 2 - 4 * velocityRatio))
        multLocal = list(map(lambda x: x*commonVelocityRatio * self.localVelocityRatio, rndCurrentBestPosition))
        betweenLocalAndCurPos = [self.localBestPos[0] - self.currentPos[0], self.localBestPos[1] - self.currentPos[1]]
        betweenGlobalAndCurPos = [self.globalBestPos[0] - self.currentPos[0], self.globalBestPos[1] - self.currentPos[1]]
        multGlobal = list(map(lambda x: x*commonVelocityRatio * self.globalVelocityRatio, rndGlobalBestPosition))
        newVelocity1 = list(map(lambda coord: coord * commonVelocityRatio, self.velocity))
        newVelocity2 = [coord1 * coord2 for coord1, coord2 in zip(multLocal, betweenLocalAndCurPos)]
        newVelocity3 = [coord1 * coord2 for coord1, coord2 in zip(multGlobal, betweenGlobalAndCurPos)]
        self.velocity = [coord1 + coord2 + coord3 for coord1, coord2, coord3 in zip(newVelocity1, newVelocity2, newVelocity3)]
        # передвигаем частицу и смотрим, какое значение целевой фунции получается
        self.currentPos = [coord1 + coord2 for coord1, coord2 in zip(self.currentPos, self.velocity)]
        newScore = self.function(*self.currentPos)
        if newScore < self.localBestScore:
            self.localBestPos = self.currentPos[:]
            self.localBestScore = newScore
        return newScore


class Swarm:

    def __init__(self, sizeSwarm,
                 currentVelocityRatio,
                 localVelocityRatio,
                 globalVelocityRatio,
                 numbersOfLife,
                 function,
                 start,
                 end,
                 goGif):
        # размер популяции частиц
        self.sizeSwarm = sizeSwarm
        # коэффициенты изменения скорости
        self.currentVelocityRatio = currentVelocityRatio
        self.localVelocityRatio = localVelocityRatio
        self.globalVelocityRatio = globalVelocityRatio
        # количество итераций алгоритма
        self.numbersOfLife = numbersOfLife
        # функция для поиска экстремума
        self.function = function
        # область поиска
        self.start = start
        self.end = end
        self.goGif=goGif
        # рой частиц
        self.swarm = []
        # данные о лучшей позиции
        self.globalBestPos = []
        self.globalBestScore = float('inf')
        # создаем рой
        self.createSwarm()


    def createSwarm(self):
        """ Метод для создания нового роя"""
        pack = [self.start, self.end, self.currentVelocityRatio, self.localVelocityRatio, self.globalVelocityRatio, self.function]
        self.swarm = [Unit(*pack) for _ in range(self.sizeSwarm)]
        # пересчитываем лучшее значение для только что созданного роя
        for unit in self.swarm:
            if unit.localBestScore < self.globalBestScore:
                self.globalBestScore = unit.localBestScore
                self.globalBestPos = unit.localBestPos



    def startSwarm(self):
        """ Метод для запуска алгоритма"""
        dataForGIF = []
        for _ in range(self.numbersOfLife):
            oneDataX = []
            oneDataY = []
            for unit in self.swarm:
                oneDataX.append(unit.currentPos[0])
                oneDataY.append(unit.currentPos[1])
                unit.globalBestPos = self.globalBestPos
                score = unit.nextIteration()
                if score < self.globalBestScore:
                    self.globalBestScore = score
                    self.globalBestPos = unit.localBestPos
            dataForGIF.append([oneDataX, oneDataY])
        if self.goGif:
            # рисуем gif
            fnames = []
            i = 0
            # dataForGIF = []
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

            with imageio.get_writer('swarm.gif', mode='I') as writer:
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
    currentVelocityRatio = 0.1
    localVelocityRatio=1
    globalVelocityRatio = 5
    numberLives = 2000
    textFunction = 'BenchEkliFunctionx10'
    NameFile =os.getcwd()+ '/swarm.xlsx'

    Individ_Lives = numberOfIndividums*numberLives
    MaxPar = 500
    ShagPar = 50

    Excel = win32com.client.Dispatch("Excel.Application")
    wb = Excel.Workbooks.Open(NameFile)
    sheet = wb.ActiveSheet
    sheet.Cells(1, 1).value = 'numberOfIndividums'
    sheet.Cells(1, 2).value = 'currentVelocityRatio'
    sheet.Cells(1, 3).value = 'localVelocityRatio'
    sheet.Cells(1, 4).value = 'globalVelocityRatio'
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
            a = Swarm(numberOfIndividums, currentVelocityRatio, localVelocityRatio, globalVelocityRatio, numberLives, BenchEkliFunctionx10, -10, 10, False)
            a.startSwarm()
            deltTime=(datetime.now()-StartTime).total_seconds()
            mTime=mTime+deltTime
            laTime = laTime + deltTime*deltTime
            mBest=mBest+a.globalBestScore
            laBest=laBest+a.globalBestScore*a.globalBestScore
            print(datetime.now(),NomStat,mBest,laBest, a.globalBestPos, a.globalBestScore)
            NomStat=NomStat+1
        mBest=mBest/KolIterStatistics
        laBest=laBest/KolIterStatistics
        print(mBest, laBest)
        sheet.Cells(NomPar + 2, 1).value = numberOfIndividums
        sheet.Cells(NomPar + 2, 2).value = currentVelocityRatio
        sheet.Cells(NomPar + 2, 3).value = localVelocityRatio
        sheet.Cells(NomPar + 2, 4).value = globalVelocityRatio
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
