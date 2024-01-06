# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 15:57:32 2022

@author: Юрий
"""

import os
from colorama import init, Fore

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

version='1.4.6.4'
dateversion='15.10.2023'

def run_script(TextPrint,NomProc,folder,folderPg,lock_excel):
    
    def colored_print(NomProc):
        if NomProc==0 or NomProc==7: print(Fore.RED, end=" ")
        if NomProc==1 or NomProc==8: print(Fore.GREEN, end=" ")
        if NomProc==2 or NomProc==9: print(Fore.YELLOW, end=" ")
        if NomProc==3 or NomProc==10: print(Fore.BLUE, end=" ")
        if NomProc==4 or NomProc==11: print(Fore.MAGENTA, end=" ")
        if NomProc==5 or NomProc==12: print(Fore.CYAN, end=" ")
        if NomProc==6 or NomProc==13: print(Fore.WHITE, end=" ")
    
    def clearOptimPath(OptimPath,maxHashWay):
        OptimPath=''
        maxHashWay=-100000000
        return OptimPath,maxHashWay
        
    def clearStartIteration(Stat,pg,OptimPath,maxHashWay,NomIteration,KolAntZero,KolAntEnd,KolIterationEnd,NomIterationTime):
        pg.ClearPheromon(1)
        Ant.createElitAgent()
        Hash.HashPath.clear()
        Hash.MaxPath.clear()
        Stat.SbrosStatistic()
        NomIteration = 1
        pg.NomSolution = 0
        KolAntZero=0
        OptimPath,maxHashWay=clearOptimPath(OptimPath,maxHashWay)
        KolAntEnd=Ant.N
        KolIterationEnd=Setting.KolIteration
        NomIterationTime=Setting.KolIteration/Stat.KolTimeDelEl
        GoTime.setStartTime()
        GoTime.setTimeIteration()
        return OptimPath,maxHashWay,NomIteration,KolAntZero,KolAntEnd,KolIterationEnd,NomIterationTime
        
    def SaveTimeFromFile(NomIterationTime,NomIteration):
         #Сохранение времени в файл
         if (NomIteration == NomIterationTime):
             Stat.SaveTime(NomIteration/Setting.KolIteration*Stat.KolTimeDelEl,(GoTime.DeltTimeIteration()).total_seconds())
            # print(NomIterationTime,datetime.now()-TimeIteration)
             GoTime.setTimeIteration() 
             NomIterationTime=NomIterationTime+Setting.KolIteration/Stat.KolTimeDelEl       
    
    def GiveAntPheromonAndHash(pg,PathWay,NomAnt,OptimPath,maxHashWay):
        # Получение нового пути в графе
        # Получения значения целевой функции
        if Setting.SocketCluster==0:
            Ant.AntArr[NomAnt].pheromon = Klaster.GetObjectivFunction(pg.GetWayGraphValue(Ant.AntArr[NomAnt].way),pg.TypeKlaster,Setting.SocketClusterTime)
        elif Setting.SocketCluster==1:
            Ant.AntArr[NomAnt].pheromon = ClientSocket.SocketSendOF(Stat,pg.GetWayGraphValue(Ant.AntArr[NomAnt].way),pg.TypeKlaster)
        # Элитные агенты, добавление в массив
        Ant.addElitAgent(Ant.AntArr[NomAnt])
        # Добавление нового ключа в Хэш-таблицу
        Hash.addPath(PathWay,Ant.AntArr[NomAnt].pheromon)
        if Setting.GoSaveMap2==1:
            SaveMap.AddElMap2(Ant.AntArr[NomAnt].way[0], Ant.AntArr[NomAnt].way[1], pg.NomSolution)
        if Ant.AntArr[NomAnt].pheromon>maxHashWay:
            maxHashWay=Ant.AntArr[NomAnt].pheromon
            OptimPath=PathWay
        Stat.ProcBestOF(Ant.AntArr[NomAnt].pheromon,pg.MaxOptimization,NomIteration,pg.NomSolution)
        return OptimPath,maxHashWay
    
    def GoPathWayHash(pg,NomAnt,OptimPath,maxHashWay):
        PathWay=Hash.goPathStr(Ant.AntArr[NomAnt].way)
        HashWay = Hash.getPath(PathWay)
        if HashWay==0:   
            pg.NomSolution = pg.NomSolution+1
            OptimPath,maxHashWay=GiveAntPheromonAndHash(pg,PathWay,NomAnt,OptimPath,maxHashWay)
        return HashWay,OptimPath,maxHashWay
    
    def EndSolution(NomAnt,NomIteration):
        KolAntEnd=NomAnt 
        KolIterationEnd=NomIteration
        print(NomProc,KolAntEnd,KolIterationEnd)
        return KolAntEnd,KolIterationEnd
    
    def AddPheromonAnt(ant, addKolSolution = True):
        if ant.pheromon!=0:
            NomWay = 0
            while NomWay<len(ant.way):
                if wayPg.pg.MaxOptimization==1:
                    wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon + (1-Ant.Ro)*Ant.Q*ant.pheromon
                else:
                    wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon + (1-Ant.Ro)*Ant.Q/ant.pheromon
                if addKolSolution:
                    wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolution = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolution + 1
                    wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolutionAll = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].KolSolutionAll + 1
                NomWay = NomWay+1
    
    init() # инициализация модуля colorama
    
    colored_print(NomProc)
    print(GoTime.now(),NomProc,' Start Program ',TextPrint)     
    if os.path.exists(folder+'/setting.ini'):
        colored_print(NomProc)
        print(GoTime.now(),NomProc,' LOAD  '+folder+'/setting.ini')  
        Setting.readSetting(folder+'/setting.ini')
    
    OptimPath=''
    maxHashWay=-100000000
    NomIteration = 1
    KolAntZero=0
    KolAntEnd=0
    KolIterationEnd=0
    NomIterationTime=0
    St.JSONFile.folderJSON=folder
    OptimPath,maxHashWay=clearOptimPath(OptimPath,maxHashWay)
    colored_print(NomProc)
    print(NomProc,'Go Parametric Graph')
    # Создание параметрического графа
    NameFile=folderPg+'/'+Setting.NameFileGraph
    Stat=St.stat()
    Par=Setting.GoNZTypeParametr(Setting.typeParametr)
    lock_excel.acquire()
    colored_print(NomProc)
    print(NomProc,NameFile)
    wayPg = pg.ProbabilityWay(NameFile)
    wayGT = gt.GraphWay(NameFile)
    NameFileRes = folder+'/'+'res.xlsx'
    Stat.SaveParametr(version,NameFileRes,Ant.N,Ant.Ro,Ant.Q,pg.PG.alf1,pg.PG.alf2,pg.PG.alf3,pg.PG.koef1,pg.PG.koef2,pg.PG.koef3,pg.PG.typeProbability,pg.PG.EndAllSolution,NameFile,Setting.AddFeromonAntZero,Setting.SbrosGraphAllAntZero,Setting.goNewIterationAntZero,Setting.goGraphTree,gt.SortPheromon,Setting.KolIteration,Setting.KolStatIteration,Setting.MaxkolIterationAntZero,Setting.typeParametr,len(wayPg.pg.ParametricGraph),wayPg.pg.OF,wayPg.pg.MinOF)
    lock_excel.release()
    colored_print(NomProc)
    print(NomProc,'Go',TextPrint)
    while Par<=Setting.endParametr:
        if Setting.SocketCluster==1:
           ClientSocket.ConnectSocket(Stat)
        Stat.StartStatistic()
        Stat.StartStatisticGrahTree(len(wayPg.pg.ParametricGraph))
        if Setting.GoSaveMap2==1:
            SaveMap.CreateElMap2(len(wayPg.pg.ParametricGraph[0].node), len(wayPg.pg.ParametricGraph[1].node))
        NomStatIteration = 0
        while NomStatIteration<Setting.KolStatIteration:
            GoTime.setPrintTime()
            NomStatIteration,Par=St.JSONFile.LoadIterJSONFileIfExist(Stat,Par)
            OptimPath,maxHashWay,NomIteration,KolAntZero,KolAntEnd,KolIterationEnd,NomIterationTime=clearStartIteration(Stat,wayPg.pg,OptimPath,maxHashWay,NomIteration,KolAntZero,KolAntEnd,KolIterationEnd,NomIterationTime)
            while NomIteration<KolIterationEnd:
                SaveTimeFromFile(NomIterationTime,NomIteration)
                #Создание агентов
                Ant.CreateAntArray(Ant.N+1)
                NomAnt=0
                KolAntZero=0
                # Проход по всем агентам
                while NomAnt<KolAntEnd:
                    try:
                        Ant.AntArr[NomAnt].way=next(wayPg)
                    except StopIteration:
                        KolAntEnd,KolIterationEnd=EndSolution(NomAnt,NomIteration) 
                    else:
                        # Проверка полученного пути в Хэш-Таблице
                        HashWay,OptimPath,maxHashWay=GoPathWayHash(wayPg.pg,NomAnt,OptimPath,maxHashWay)
                        if HashWay!=0:
                            # Такой путь уже есть в Хэш-таблице
                            if Setting.AddFeromonAntZero==0:
                                Ant.AntArr[NomAnt].pheromon=0
                            else:
                                Ant.AntArr[NomAnt].pheromon=HashWay
                            Stat.KolAntZero = Stat.KolAntZero+1
                            KolAntZero = KolAntZero+1
                            
                            #Если включены повторные итерации алгоритма
                            if Setting.goNewIterationAntZero==1:
                                #Если путь не найден, то продолжать генерацию маршрутов, пока не найдется уникальный
                                kolIterationAntZero=0
                                while HashWay!=0 and kolIterationAntZero<Setting.MaxkolIterationAntZero:
                                    kolIterationAntZero = kolIterationAntZero+1
                                    try:
                                        Ant.AntArr[NomAnt].way=next(wayPg)
                                    except StopIteration:
                                        KolAntEnd,KolIterationEnd=EndSolution(NomAnt,NomIteration) 
                                        HashWay=10
                                    else:
                                        HashWay,OptimPath,maxHashWay=GoPathWayHash(wayPg.pg,NomAnt,OptimPath,maxHashWay)
                                Stat.StatIterationAntZero(kolIterationAntZero)
                            
                            #Если путь не найден, то обход графа в виде дерева 
                            if Setting.goGraphTree==1:
                              try:
                                  gt.StartWayGraphTree=Ant.AntArr[NomAnt].way 
                                  Ant.AntArr[NomAnt].way=next(wayGT)
                              except StopIteration:
                                  KolAntEnd,KolIterationEnd=EndSolution(NomAnt,NomIteration) 
                              else:
                                  HashWay,OptimPath,maxHashWay=GoPathWayHash(wayGT.pg,NomAnt,OptimPath,maxHashWay)
                                  Stat.StatIterationAntZero(gt.KolIterWay) 
                                  Stat.StatIterationAntZeroGraphTree(gt.NomElKolIterWay)
                        # Переход к следующему агенту
                        NomAnt=NomAnt+1
                    
                #Все агенты не нашли новых путей в графе
                Stat.ProcAntZero = Stat.ProcAntZero+KolAntZero/Ant.N
                if KolAntZero==Ant.N:
                    if Setting.SbrosGraphAllAntZero==1:
                      wayPg.pg.ClearPheromon(0)  
                    Stat.KolAllAntZero = Stat.KolAllAntZero+1
                    Stat.StatAllAntZero(NomIteration, wayPg.pg.NomSolution)
        
                # Испарение феромона
                wayPg.pg.DecreasePheromon(Ant.Ro)
                    
                # Добавление феромона
                NomAnt=0
                while NomAnt<KolAntEnd:
                    AddPheromonAnt(Ant.AntArr[NomAnt])
                    NomAnt=NomAnt+1
                NomAnt=0
                while NomAnt<Ant.KolElitAgent:
                    AddPheromonAnt(Ant.ElitAntArr[NomAnt], addKolSolution = False)
                    NomAnt=NomAnt+1
                
                
                # Переход к следующей итерации
                if (pg.PG.typeProbability==1) or (pg.PG.typeProbability==3):
                    wayPg.pg.NormPheromon()
                Ant.DelAllAgent()
                NomIteration=NomIteration+1
                #wayPg.pg.PrintParametricGraph(1)
    
            
            
            Stat.EndStatistik(NomIteration, wayPg.pg.NomSolution)
            Stat.SaveTimeIteration((GoTime.DeltStartTime()).total_seconds())
            NomStatIteration=NomStatIteration+1
            St.JSONFile.SaveIterJSONFile(Stat,NomStatIteration,Par)
    
            colored_print(NomProc)
            print(GoTime.now(),NomProc,' END ',TextPrint,(GoTime.DeltStartTime())*(Setting.KolStatIteration-NomStatIteration),' typeParametr=',Setting.typeParametr,Par,' NomStatIteration ',NomStatIteration,"{:8.3f}".format(Stat.MIterationAntZero/NomStatIteration),' Duration: {} '.format(GoTime.DeltStartTime()),' OptimPath ',OptimPath,version) 
        
        St.JSONFile.RemoveJSONFile()
        lock_excel.acquire()
        Stat.SaveStatisticsExcel(NameFileRes,GoTime.DeltStartTime(),NomStatIteration,OptimPath,Par)
        if Setting.GoSaveMap2==1:
            SaveMap.PrintElMap2(folder+'/'+'MapFile.xlsx')
        lock_excel.release()
        Par=Par+Setting.shagParametr
        Setting.EndTypeParametr(Setting.typeParametr,Par)

        if Setting.SocketCluster==1:
            ClientSocket.SocketEnd(Stat)