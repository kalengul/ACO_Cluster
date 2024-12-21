# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 15:57:32 2022

@author: Юрий
"""

import os
import threading
import concurrent.futures
import multiprocessing
from numba import jit,njit
import time
from colorama import init, Fore
import sys #для максимального отрицательного числа

import LoadSettingsIniFile as Setting
import ParametricGraph as pg
import Ant
import VirtualKlaster as Klaster
import Hash
import Stat as St
import GraphTree as gt
import SaveMap
import GoTime
import ClientSocket
import GoParetto
import Model.Rosaviation.Rosaviation

version='1.4.10'
dateversion='13.12.2024'

def run_script(TextPrint,NomProc,folder,folderPg,lock_excel):

    def colored_print(NomProc):
        if NomProc==0 or NomProc==7: print(Fore.RED, end=" ")
        if NomProc==1 or NomProc==8: print(Fore.GREEN, end=" ")
        if NomProc==2 or NomProc==9: print(Fore.YELLOW, end=" ")
        if NomProc==3 or NomProc==10: print(Fore.BLUE, end=" ")
        if NomProc==4 or NomProc==11: print(Fore.MAGENTA, end=" ")
        if NomProc==5 or NomProc==12: print(Fore.CYAN, end=" ")
        if NomProc==6 or NomProc==13: print(Fore.WHITE, end=" ")

    def clearoptPathHash(optMax = True):
        optPathHash=''
        if optMax:
            optOFHash=-sys.maxsize - 1
        else:
            optOFHash=+sys.maxsize - 1
        return optPathHash,optOFHash

    def clearStartIteration(Stat,pg):
        pg.ClearPheromon(1)
        Ant.createElitAgent(Setting.KolParetto,pg.MaxOptimization==1)
        Hash.HashPath.clear()
        Hash.MaxPath.clear()
        Stat.SbrosStatistic(Setting.KolParetto)
        NomIteration = 1
        optPathHash,optOFHash=clearoptPathHash(pg.MaxOptimization==1)
        KolAntEnd=Ant.N
        KolIterationEnd=Setting.KolIteration
        NomIterationTime=Setting.KolIteration/Stat.KolTimeDelEl
        GoTime.setStartTime()
        GoTime.setTimeIteration()
        return optPathHash,optOFHash,NomIteration,KolAntEnd,KolIterationEnd,NomIterationTime

    def SaveTimeFromFile(NomIterationTime,NomIteration):
         #Сохранение времени в файл
         if (NomIteration == NomIterationTime):
             Stat.SaveTime(NomIteration/Setting.KolIteration*Stat.KolTimeDelEl,(GoTime.DeltTimeIteration()).total_seconds())
            # print(NomIterationTime,datetime.now()-TimeIteration)
             GoTime.setTimeIteration()
             NomIterationTime=NomIterationTime+Setting.KolIteration/Stat.KolTimeDelEl

    def AddDeltZeroPheromon(pg,delt,NomPheromon):
        #Пройти во всем слоям параметрического графа
        NomParametr=0
        while NomParametr<len(pg.ParametricGraph):
            NomNode=0
            #Пройти по всем вершинам слоя параметрического графа
            while NomNode<len(pg.ParametricGraph[NomParametr].node):
                #Пройти по всем элементам массива итераций
                NomSolution=0
                while NomSolution<len(pg.ParametricGraph[NomParametr].node[NomNode].KolSolutionIteration):
                    if len(pg.ParametricGraph[NomParametr].node[NomNode].KolSolutionIteration)-NomSolution>0.9:
                        if NomPheromon==None:
                            pg.ParametricGraph[NomParametr].node[NomNode].pheromon=pg.ParametricGraph[NomParametr].node[NomNode].pheromon+pow((1-Ant.Ro)*Ant.Q,((len(pg.ParametricGraph[NomParametr].node[NomNode].KolSolutionIteration)-NomSolution)))*delt*pg.ParametricGraph[NomParametr].node[NomNode].KolSolutionIteration[NomSolution]
                        else:
                            pg.ParametricGraph[NomParametr].node[NomNode].ArrPheromon[NomPheromon] = \
                            pg.ParametricGraph[NomParametr].node[NomNode].ArrPheromon[NomPheromon] + pow((1 - Ant.Ro) * Ant.Q, ((len(
                                pg.ParametricGraph[NomParametr].node[NomNode].KolSolutionIteration) - NomSolution))) * delt * \
                            pg.ParametricGraph[NomParametr].node[NomNode].KolSolutionIteration[NomSolution]
                    NomSolution=NomSolution+1
                NomNode=NomNode+1
            NomParametr=NomParametr+1

    def GiveAntPheromonAndHash(pg,PathWay,NomAnt,optPathHash,optOFHash):
        global ParetoSet,kolParetoSet
        # Получение нового пути в графе
        # Получения значения целевой функции
        if Setting.SocketKolCluster==0:
            Ant.AntArr[NomAnt].OF,Ant.AntArr[NomAnt].ArrOF = Klaster.GetObjectivFunction(pg.GetWayGraphValue(Ant.AntArr[NomAnt].way),pg.TypeKlaster,Setting.SocketClusterTime, pg.typeProbability-30)
        if (pg.typeProbability >= 30) and (pg.typeProbability < 40):
            ParetoSet,kolParetoSet= GoParetto.update_pareto_set(ParetoSet,kolParetoSet, None, PathWay, Ant.AntArr[NomAnt].ArrOF)
        #print(Ant.AntArr[NomAnt].OF,Ant.AntArr[NomAnt].ArrOF)
        #elif Setting.SocketCluster==1:
        #    Ant.AntArr[NomAnt].OF = ClientSocket.SocketSendOF(Stat,pg.GetWayGraphValue(Ant.AntArr[NomAnt].way),pg.TypeKlaster)
        # Добавление нового ключа в Хэш-таблицу
        Hash.addPath(PathWay,Ant.AntArr[NomAnt].OF)
        # Элитные агенты, добавление в массив
        if Ant.KolElitAgent !=0:
            Ant.addElitAgent(Ant.AntArr[NomAnt],pg.MaxOptimization==1)
            if (pg.typeProbability >= 30) and (pg.typeProbability < 40):
                nomPareto=0
                while nomPareto<Setting.KolParetto:
                    Ant.addElitAgentPareto(Ant.AntArr[NomAnt],nomPareto,pg.MaxOptimization==1)
                    nomPareto=nomPareto+1
        #Проверка на отрицательный феромон
        if Ant.DeltZeroPheromon != 0:
            if Ant.AntArr[NomAnt].OF+pg.difZero<0:
                #Учет смещения в каждой вершине параметрического графа
                AddDeltZeroPheromon(pg,abs(pg.difZero+Ant.AntArr[NomAnt].OF),None)
                #Установка нового значения смещения
                pg.difZero=abs(Ant.AntArr[NomAnt].OF)
            NomPareto=0
            while NomPareto<len(Ant.AntArr[NomAnt].ArrOF):
                if Ant.AntArr[NomAnt].ArrOF[NomPareto] + pg.ArrDifZero[NomPareto] < 0:
                    # Учет смещения в каждой вершине параметрического графа
                    AddDeltZeroPheromon(pg, abs(pg.ArrDifZero[NomPareto] + Ant.AntArr[NomAnt].ArrOF[NomPareto]),NomPareto)
                    # Установка нового значения смещения
                    pg.ArrDifZero[NomPareto] = abs(Ant.AntArr[NomAnt].ArrOF[NomPareto])
                NomPareto=NomPareto+1
        #print(Ant.AntArr[NomAnt].way,Ant.AntArr[NomAnt].ArrOF,pg.ArrDifZero)
        if Setting.GoSaveMap2==1:
            SaveMap.AddElMap2(Ant.AntArr[NomAnt].way[0]*(Ant.AntArr[NomAnt].way[1]+Ant.AntArr[NomAnt].way[2]+Ant.AntArr[NomAnt].way[3]+Ant.AntArr[NomAnt].way[4]+Ant.AntArr[NomAnt].way[5]), Ant.AntArr[NomAnt].way[6]*(Ant.AntArr[NomAnt].way[7]+Ant.AntArr[NomAnt].way[8]+Ant.AntArr[NomAnt].way[9]+Ant.AntArr[NomAnt].way[10]+Ant.AntArr[NomAnt].way[11]), pg.NomSolution)
        if ((pg.MaxOptimization==1) and (Ant.AntArr[NomAnt].OF>optOFHash)) or \
                ((pg.MaxOptimization==0) and (Ant.AntArr[NomAnt].OF<optOFHash)):
            optOFHash=Ant.AntArr[NomAnt].OF
            optPathHash=PathWay
        Stat.ProcBestOF(Ant.AntArr[NomAnt].OF,pg.MaxOptimization,NomIteration,pg.NomSolution)
        NomPareto = 0
        while NomPareto < len(Ant.AntArr[NomAnt].ArrOF):
            Stat.ProcBestOFArray(Ant.AntArr[NomAnt].ArrOF[NomPareto],NomPareto,pg.MaxOptimization,NomIteration,pg.NomSolution)
            NomPareto = NomPareto + 1
        return optPathHash,optOFHash

    def GoPathWayHash(pg,NomAnt,optPathHash,optOFHash):
        PathWay=Hash.goPathStr(Ant.AntArr[NomAnt].way)
        FindHash, HashWay = Hash.getPath(PathWay)
        #if PathWay==';150;150':
        #    print(FindHash,HashWay,Ant.AntArr[NomAnt].way,NomAnt,Ant.AntArr[NomAnt].OF)
        if FindHash==False:
            pg.NomSolution = pg.NomSolution+1

            optPathHash,optOFHash=GiveAntPheromonAndHash(pg,PathWay,NomAnt,optPathHash,optOFHash)
        return HashWay,optPathHash,optOFHash

    def EndSolution(NomAnt,NomIteration):
        KolAntEnd=NomAnt
        KolIterationEnd=NomIteration
        print(NomProc,KolAntEnd,KolIterationEnd)
        return KolAntEnd,KolIterationEnd

    def AddPheromonAnt(ant,NomIteration, addKolSolution = True):
        #print(wayPg.pg.AllSolution,wayPg.pg.NomSolution,ant.ignore,ant.way,NomIteration,len(wayPg.pg.ParametricGraph[0].node[0].KolSolutionIteration),addKolSolution,ant.OF, wayPg.pg.difZero,ant.OF+wayPg.pg.difZero)
        if ant.ignore==0:

            #print('ant.OF=',ant.OF,'wayPg.pg.difZero=',wayPg.pg.difZero,'=',(1-Ant.Ro)*Ant.Q*(ant.OF+wayPg.pg.difZero))
            NomWay = 0
            while NomWay<len(ant.way):
                if wayPg.pg.MaxOptimization==1:
                    wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon + (1-Ant.Ro)*Ant.Q*(ant.OF+wayPg.pg.difZero)
                    nomDifZer = 0
                    while nomDifZer < len(wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].ArrPheromon):
                        wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].ArrPheromon[nomDifZer] = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].ArrPheromon[nomDifZer] + (1-Ant.Ro)*Ant.Q*(ant.ArrOF[nomDifZer]+wayPg.pg.ArrDifZero[nomDifZer])
                        nomDifZer = nomDifZer + 1
                else:
                    if ant.OF+wayPg.pg.difZero!=0:
                        wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon + (1-Ant.Ro)*Ant.Q/(ant.OF+wayPg.pg.difZero)
                    nomDifZer = 0
                    while nomDifZer < len(wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].ArrPheromon):
                        if (ant.ArrOF[nomDifZer]+wayPg.pg.ArrDifZero[nomDifZer]) != 0:
                            wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].ArrPheromon[nomDifZer] = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].ArrPheromon[nomDifZer] + (1-Ant.Ro)*Ant.Q/(ant.ArrOF[nomDifZer]+wayPg.pg.ArrDifZero[nomDifZer])
                        nomDifZer = nomDifZer + 1
                if addKolSolution:
                    wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolution = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolution + 1
                    wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolutionAll = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolutionAll + 1
                    if Ant.DeltZeroPheromon != 0:
                        if NomIteration>len(wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolutionIteration):
                            NomIteration=len(wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolutionIteration)
                        if NomIteration<=0:
                            NomIteration=1
                        wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolutionIteration[NomIteration-1]=wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolutionIteration[NomIteration-1]+1
                #print(NomIteration-1,wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolutionIteration)
                NomWay = NomWay+1

#    @njit(parallel=True)
    def GoAnt(NomAnt,KolAntZero,optPathHash, optOFHash):
        EndIteration = False
        try:
            Ant.AntArr[NomAnt].way = next(wayPg)
        except StopIteration:
            EndIteration = True

        else:
            # Проверка полученного пути в Хэш-Таблице
            kolIterationAntZero = 0
            HashWay, optPathHash, optOFHash = GoPathWayHash(wayPg.pg, NomAnt, optPathHash, optOFHash)
            if HashWay != 0:
                # Такой путь уже есть в Хэш-таблице
                if Setting.AddFeromonAntZero == 0:
                    Ant.AntArr[NomAnt].OF = 0
                    Ant.AntArr[NomAnt].ignore = 1
                else:
                    Ant.AntArr[NomAnt].OF = HashWay
                Stat.KolAntZero = Stat.KolAntZero + 1
                KolAntZero = KolAntZero + 1

                # Если включены повторные итерации алгоритма
                if Setting.goNewIterationAntZero == 1:
                    # Если путь не найден, то продолжать генерацию маршрутов, пока не найдется уникальный
                    Ant.AntArr[NomAnt].ignore = 0
                    while HashWay != 0 and kolIterationAntZero < Setting.MaxkolIterationAntZero:
                        kolIterationAntZero = kolIterationAntZero + 1
                        try:
                            Ant.AntArr[NomAnt].way = next(wayPg)
                        except StopIteration:
                            EndIteration = True
                            return EndIteration,optPathHash, optOFHash
                            HashWay = 10
                        else:
                            HashWay, optPathHash, optOFHash = GoPathWayHash(wayPg.pg, NomAnt, optPathHash, optOFHash)
                    if kolIterationAntZero == Setting.MaxkolIterationAntZero:
                        Ant.AntArr[NomAnt].ignore = 1
                # Если путь не найден, то обход графа в виде дерева
                if Setting.goGraphTree == 1:
                    Ant.AntArr[NomAnt].ignore = 0
                    try:
                        gt.StartWayGraphTree = Ant.AntArr[NomAnt].way
                        Ant.AntArr[NomAnt].way = next(wayGT)
                    except StopIteration:
                        KolAntEnd, KolIterationEnd = EndSolution(NomAnt, NomIteration)
                    else:
                        HashWay, optPathHash, optOFHash = GoPathWayHash(wayGT.pg, NomAnt, optPathHash, optOFHash)
                        Stat.StatIterationAntZero(gt.KolIterWay)
                        Stat.StatIterationAntZeroGraphTree(gt.NomElKolIterWay)
        if Ant.AntArr[NomAnt].OF==sys.maxsize:
            Ant.AntArr[NomAnt].ignore = 1
        return EndIteration,KolAntZero,optPathHash, optOFHash, kolIterationAntZero

    init() # инициализация модуля colorama

    global ParetoSet, kolParetoSet

    colored_print(NomProc)
    print(GoTime.now(),NomProc,' Start Program ',TextPrint)
    if os.path.exists(folder+'/setting.ini'):
        colored_print(NomProc)
        print(GoTime.now(),NomProc,' LOAD  '+folder+'/setting.ini')
        Setting.readSetting(folder+'/setting.ini')

    St.JSONFile.folderJSON=folder
    colored_print(NomProc)
    print(GoTime.now(),NomProc,'Go Parametric Graph')
    # Создание параметрического графа
    NameFile=folderPg+'/'+Setting.NameFileGraph
    Stat=St.stat(Setting.KolParetto)
    Par=Setting.GoNZTypeParametr(Setting.typeParametr)
    lock_excel.acquire()
    colored_print(NomProc)
    print(GoTime.now(),NomProc,NameFile)
    wayPg = pg.ProbabilityWay(NameFile,Setting.KolParetto)
    wayGT = gt.GraphWay(NameFile)
    NameFileRes = folder+'/'+'res.xlsx'
    Stat.SaveParametr(version,NameFileRes,Ant.N,Ant.Ro,Ant.Q,Ant.KolElitAgent, Ant.DeltZeroPheromon, pg.PG.alf1,pg.PG.alf2,pg.PG.alf3,pg.PG.koef1,pg.PG.koef2,pg.PG.koef3,pg.PG.typeProbability,pg.PG.EndAllSolution,NameFile,Setting.AddFeromonAntZero,Setting.SbrosGraphAllAntZero,Setting.goNewIterationAntZero,Setting.goGraphTree,gt.SortPheromon,Setting.KolIteration,Setting.KolStatIteration,Setting.MaxkolIterationAntZero,Setting.typeParametr,Setting.GoParallelAnt,Setting.KolParallelAnt,len(wayPg.pg.ParametricGraph),wayPg.pg.KoefLineSummPareto,Setting.KolParetto,wayPg.pg.OF,wayPg.pg.MinOF)

    if (wayPg.pg.TypeKlaster>=6000) and (wayPg.pg.TypeKlaster<=6010):
       Model.Rosaviation.Rosaviation.load_data_rosaviation_excel(column_index=Model.Rosaviation.Rosaviation.column_index_rosaviation, tren_size=0.75)
    print(GoTime.now(),NomProc,'Go ParetoSet')
    if (pg.PG.typeProbability>=30) and (pg.PG.typeProbability<40):
        if (wayPg.pg.TypeKlaster >= 6000) and (wayPg.pg.TypeKlaster <= 6010):
            NameFileParetoSet=folderPg + '/EnableParetoSet/'+Setting.NameFileGraph[:-5]+str(Setting.KolParetto)+'_'+str(Model.Rosaviation.Rosaviation.column_index_rosaviation)+'.xlsx'
        else:
            NameFileParetoSet = folderPg + '/EnableParetoSet/' + Setting.NameFileGraph[:-5] + str(
                Setting.KolParetto) + '.xlsx'
        print(NameFileParetoSet)
        if Setting.GoLoadParetto == 1:
            if os.path.exists(NameFileParetoSet):
                GoParetto.AllParetoSet, GoParetto.pathArrParetoSet, GoParetto.AllSolution = Stat.load_pareto_set_excel(NameFileParetoSet, Setting.KolParetto)
            else:
                GoParetto.CreateAllParetoSet(wayPg.pg.ParametricGraph, wayPg.pg.TypeKlaster, wayPg.pg.typeProbability-30,Stat,folder+'/'+'ParetoSet.xlsx',lock_excel)

    lock_excel.release()
    colored_print(NomProc)
    print(GoTime.now(),NomProc,'Go',TextPrint)
    while Par<=Setting.endParametr:
        print('Setting.KolParetto,wayPg.pg.MaxOptimization',Setting.KolParetto,wayPg.pg.MaxOptimization)
        Stat.StartStatistic(Setting.KolParetto,wayPg.pg.MaxOptimization)
        Stat.StartStatisticGrahTree(len(wayPg.pg.ParametricGraph))
        if Setting.GoSaveMap2==1:
            SaveMap.CreateElMap2(1200, 1200)
#            SaveMap.CreateElMap2(len(wayPg.pg.ParametricGraph[0].node), len(wayPg.pg.ParametricGraph[1].node))
        NomStatIteration = 0
        while NomStatIteration<Setting.KolStatIteration:
            GoTime.setPrintTime()
            ParetoSet = []
            kolParetoSet=0
            kolIterationAntZero = 0
            NomStatIteration,Par=St.JSONFile.LoadIterJSONFileIfExist(Stat,Par)
            optPathHash,optOFHash,NomIteration,KolAntEnd,KolIterationEnd,NomIterationTime=clearStartIteration(Stat,wayPg.pg)
            while NomIteration<KolIterationEnd:
                SaveTimeFromFile(NomIterationTime,NomIteration)
                #Создание агентов
                Ant.CreateAntArray(Ant.N+1)
                NomAnt=0
                KolAntZero=0
                if (Setting.GoParallelAnt == 0):
                # Проход по всем агентам
                    while NomAnt<KolAntEnd:
                        wayPg.NomArr=NomAnt % Setting.KolParetto
                        TrueEndGoAnt, KolAntZero, optPathHash, optOFHash, kolAntZero = GoAnt(NomAnt, KolAntZero, optPathHash, optOFHash)
                        kolIterationAntZero=kolIterationAntZero+kolAntZero
                        if TrueEndGoAnt:
                            KolAntEnd, KolIterationEnd = EndSolution(NomAnt, NomIteration)
                        else:
                            # Переход к следующему агенту
                            NomAnt=NomAnt+1
                elif (Setting.GoParallelAnt == 1):
                    # Определение количества потоков
                    if Setting.KolParallelAnt==0:
                        max_workers=KolAntEnd
                    else:
                        max_workers = min(int(Setting.KolParallelAnt), KolAntEnd)
                    # Использование ThreadPoolExecutor для запуска функции GoAnt в нескольких потоках
                    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                        # Список для хранения результатов
                        results = []
                        # Запуск функции GoAnt для каждого потока
                        while NomAnt < KolAntEnd:
                            future = executor.submit(GoAnt, NomAnt, KolAntZero, optPathHash, optOFHash)
                            # Переход к следующему агенту
                            NomAnt = NomAnt + 1
                            results.append(future)
                        # Обработка результатов
                        for future in concurrent.futures.as_completed(results):
                            TrueEndGoAnt, KolAntZero, optPathHash, optOFHash = future.result()
                            if TrueEndGoAnt:
                                KolAntEnd, KolIterationEnd = EndSolution(NomAnt, NomIteration)
                elif (Setting.GoParallelAnt == 2) and (Setting.KolParallelAnt==0):
                    threads = []
                    # Запуск функции GoAnt в KolAntEnd потоках
                    for NomAnt in range(int(KolAntEnd)):
                        thread = threading.Thread(target=GoAnt, args=(NomAnt, KolAntZero, optPathHash, optOFHash))
                        threads.append(thread)
                        thread.start()
                    # Ожидание завершения всех потоков
                    for thread in threads:
                        thread.join()
                elif (Setting.GoParallelAnt == 3) and (Setting.KolParallelAnt==0):
                    # Создание ThreadPoolExecutor с KolAntEnd потоками
                    with concurrent.futures.ProcessPoolExecutor(max_workers=int(KolAntEnd)) as executor:
                        # Запуск функции GoAnt для каждого процесса
                        future = executor.submit(GoAnt, NomAnt, KolAntZero, optPathHash, optOFHash)
                        # Ожидание результата и получение его
                        #TrueEndGoAnt, optPathHash, optOFHash = future.result()
                elif (Setting.GoParallelAnt == 4) and (Setting.KolParallelAnt==0):
                    processes = []
                    # Запуск функции GoAnt в KolAntEnd процессах
                    for NomAnt in range(int(KolAntEnd)):
                        p = multiprocessing.Process(target=GoAnt, args=(NomAnt, KolAntZero, optPathHash, optOFHash))
                        processes.append(p)
                        p.start()
                    # Ждем завершения всех процессов
                    for p in processes:
                        p.join()

                if Ant.DeltZeroPheromon != 0:
                    wayPg.pg.AddIterationLayerKolSolution()
                #Все агенты не нашли новых путей в графе
                Stat.ProcAntZero = Stat.ProcAntZero+KolAntZero/Ant.N
                if KolAntZero==Ant.N:
                    if Setting.SbrosGraphAllAntZero==1:
                      wayPg.pg.ClearPheromon(0)
                    Stat.KolAllAntZero = Stat.KolAllAntZero+1
                    #Stat.StatAllAntZero(NomIteration, wayPg.pg.NomSolution)
                # Испарение феромона
                wayPg.pg.DecreasePheromon(Ant.Ro)

                # Добавление феромона
                NomAnt=0
                while NomAnt<KolAntEnd:
                    AddPheromonAnt(Ant.AntArr[NomAnt],NomIteration)
                    NomAnt=NomAnt+1

                if (pg.PG.typeProbability>=30) and (pg.PG.typeProbability<40):
                    NomPareto=0
                    while NomPareto<Setting.KolParetto:
                        NomAnt = 0
                        while NomAnt < Ant.KolElitAgent:
                            AddPheromonAnt(Ant.ElitAntArrPareto[NomPareto][NomAnt], NomIteration, addKolSolution=False)
                            NomAnt = NomAnt + 1
                        NomPareto=NomPareto+1
                else:
                    NomAnt = 0
                    while NomAnt<Ant.KolElitAgent:
                        AddPheromonAnt(Ant.ElitAntArr[NomAnt],NomIteration, addKolSolution = False)
                        NomAnt=NomAnt+1


                # Переход к следующей итерации
                if (pg.PG.typeProbability==1) or (pg.PG.typeProbability==3) or (pg.PG.typeProbability>=30) and (pg.PG.typeProbability<40):
                    wayPg.pg.NormPheromon()
                Ant.DelAllAgent()
                NomIteration=NomIteration+1
                #wayPg.pg.PrintParametricGraph(1)


            Stat.StatIterationAntZero(kolIterationAntZero)
            Stat.EndStatistik(NomIteration, wayPg.pg.NomSolution)
            Stat.SaveTimeIteration((GoTime.DeltStartTime()).total_seconds())
            NomStatIteration=NomStatIteration+1
            if (pg.PG.typeProbability >= 30) and (pg.PG.typeProbability < 40):

                Stat.StatParettoSet(Setting.KolParetto,len(GoParetto.AllParetoSet), GoParetto.AllSolution, len(ParetoSet), kolParetoSet, GoParetto.ComparisonParetoSet(ParetoSet))
                # lock_excel.acquire()
                #Stat.save_pareto_set_excel(folder+'/'+'ParetoSet600.xlsx', GoTime.DeltStartTime(), GoParetto.ComparisonParetoSet(ParetoSet), [], pg.PG.typeProbability)
                #lock_excel.release()
            St.JSONFile.SaveIterJSONFile(Stat, NomStatIteration, Par)
            colored_print(NomProc)
            print(len(ParetoSet),kolParetoSet)
            print(GoTime.now(),NomProc,' END ',TextPrint,(GoTime.DeltStartTime())*(Setting.KolStatIteration-NomStatIteration),' typeParametr=',Setting.typeParametr,Par,' NomStatIteration ',NomStatIteration,"{:8.3f}".format(Stat.MIterationAntZero/NomStatIteration),' Duration: {} '.format(GoTime.DeltStartTime()),' optPathHash ',optPathHash,version)

        St.JSONFile.RemoveJSONFile()
        lock_excel.acquire()
        Stat.SaveStatisticsExcel(NameFileRes,Ant.N, Setting.KolParetto,GoTime.DeltStartTime(),NomStatIteration,optPathHash,Par)
        if (pg.PG.typeProbability >= 30) and (pg.PG.typeProbability < 40):
            Stat.SaveStatisticsExcelParetto(NameFileRes,NomStatIteration,31)
        if Setting.GoSaveMap2==1:
            SaveMap.PrintElMap2(folder+'/'+'MapFile.xlsx')
        lock_excel.release()
        Par=Par+Setting.shagParametr
        Setting.EndTypeParametr(Setting.typeParametr,Par)

        if Setting.SocketKolCluster!=0:
            ClientSocket.SocketEnd(Stat)