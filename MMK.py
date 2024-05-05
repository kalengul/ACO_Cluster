# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 15:57:32 2022

@author: Юрий
"""

import os
from colorama import init, Fore
import sys #для максимального отрицательного числа
import threading

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
import ant_thread

version='1.5.0'
dateversion='20.01.2024'

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
        pg.NomSolution = 0
        Ant.createElitAgent(pg.MaxOptimization==1)
        Hash.HashPath.clear()
        Hash.MaxPath.clear()
        Stat.SbrosStatistic()
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
       
    def EndSolution(NomAnt,NomIteration):
        KolAntEnd=NomAnt 
        KolIterationEnd=NomIteration
        print(NomProc,KolAntEnd,KolIterationEnd)
        return KolAntEnd,KolIterationEnd
    
    def AddPheromonAnt(ant,NomIteration, addKolSolution = True):
        print(wayPg.pg.AllSolution,wayPg.pg.NomSolution,ant.ignore,ant.way,NomIteration,len(wayPg.pg.ParametricGraph[0].node[0].KolSolutionIteration),addKolSolution,ant.OF, wayPg.pg.difZero,ant.OF+wayPg.pg.difZero)
        if ant.ignore==0:
           
            #print('ant.OF=',ant.OF,'wayPg.pg.difZero=',wayPg.pg.difZero,'=',(1-Ant.Ro)*Ant.Q*(ant.OF+wayPg.pg.difZero))
            NomWay = 0
            while NomWay<len(ant.way):
                if wayPg.pg.MaxOptimization==1:
                    wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon + (1-Ant.Ro)*Ant.Q*(ant.OF+wayPg.pg.difZero)
                else:
                    if ant.OF+wayPg.pg.difZero!=0:
                        wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon = wayPg.pg.ParametricGraph[NomWay].node[ant.way[NomWay]].pheromon + (1-Ant.Ro)*Ant.Q/(ant.OF+wayPg.pg.difZero)
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
    
       
    
    init() # инициализация модуля colorama
    
    colored_print(NomProc)
    print(GoTime.now(),NomProc,' Start Program ',TextPrint)     
    if os.path.exists(folder+'/setting.ini'):
        colored_print(NomProc)
        print(GoTime.now(),NomProc,' LOAD  '+folder+'/setting.ini')  
        Setting.readSetting(folder+'/setting.ini')
    

    St.JSONFile.folderJSON=folder
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
        Stat.StartStatistic()
        Stat.StartStatisticGrahTree(len(wayPg.pg.ParametricGraph))
        if Setting.GoSaveMap2==1:
            SaveMap.CreateElMap2(len(wayPg.pg.ParametricGraph[0].node), len(wayPg.pg.ParametricGraph[1].node))
        ant_tread_array=[]
        NomStatIteration = 0
        while NomStatIteration<Setting.KolStatIteration:
            GoTime.setPrintTime()
            NomStatIteration,Par=St.JSONFile.LoadIterJSONFileIfExist(Stat,Par)
            # Очистка статстисики и обнуление графа
            optPathHash,optOFHash,KolAntEndWay,KolAntEnd,KolIterationEnd,NomIterationTime=clearStartIteration(Stat,wayPg.pg)
            #Проверка на выполнение определенного количества найденных решений
            while KolAntEndWay<KolIterationEnd*KolAntEnd:
                #Проверка на количество одновременно работающих агентов
                if len(Ant.AntArr)<=KolAntEnd:
                    #Создание агента-потока, добавление его в список текущих агентов
                    NomAnt=Ant.AddAntArray()
                    #Поиск агентом маршрута и вычисление целевой функции на кластере + повторный поиск, если найден маршрут в Хэше
                    ant = threading.Thread(target=ant_thread.go_ant, args=(wayPg,wayGT,Ant.AntArr[NomAnt]))
                    ant_tread_array.append(ant)
                    ant.start()
                #
            
            
            
            while NomIteration<KolIterationEnd:
                SaveTimeFromFile(NomIterationTime,NomIteration)
                #Создание агентов
                #Ant.CreateAntArray(Ant.N+1)
                NomAnt=0
                KolAntZero=0

                    
                #print('wayPg.pg.AddIterationLayerKolSolution')
                if Ant.DeltZeroPheromon != 0:
                    wayPg.pg.AddIterationLayerKolSolution()
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
                    AddPheromonAnt(Ant.AntArr[NomAnt],NomIteration)
                    NomAnt=NomAnt+1
                NomAnt=0
                while NomAnt<Ant.KolElitAgent:
                    AddPheromonAnt(Ant.ElitAntArr[NomAnt],NomIteration, addKolSolution = False)
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
            print(GoTime.now(),NomProc,' END ',TextPrint,(GoTime.DeltStartTime())*(Setting.KolStatIteration-NomStatIteration),' typeParametr=',Setting.typeParametr,Par,' NomStatIteration ',NomStatIteration,"{:8.3f}".format(Stat.MIterationAntZero/NomStatIteration),' Duration: {} '.format(GoTime.DeltStartTime()),' optPathHash ',optPathHash,version) 
        
        St.JSONFile.RemoveJSONFile()
        lock_excel.acquire()
        Stat.SaveStatisticsExcel(NameFileRes,GoTime.DeltStartTime(),NomStatIteration,optPathHash,Par)
        if Setting.GoSaveMap2==1:
            SaveMap.PrintElMap2(folder+'/'+'MapFile.xlsx')
        lock_excel.release()
        Par=Par+Setting.shagParametr
        Setting.EndTypeParametr(Setting.typeParametr,Par)

        if Setting.SocketKolCluster!=0:
            ClientSocket.SocketEnd(Stat)