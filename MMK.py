# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 15:57:32 2022

@author: Юрий
"""

import os


import LoadSettingsIniFile as Setting
import ParametricGraph as pg
import Ant
import VirtualKlaster as Klaster
import Hash
import Stat as St
import GraphTree as gt
import SaveMap
import GoTime

version='1.4.5'
dateversion='02.01.2023'

def clearOptimPath():
    global OptimPath
    global maxHashWay
    OptimPath=''
    maxHashWay=-100000000
    
def clearStartIteration(Stat,pg):
    global NomIteration
    global KolAntZero
    global KolAntEnd
    global KolIterationEnd
    global NomIterationTime
    pg.ClearPheromon()
    Hash.HashPath.clear()
    Hash.MaxPath.clear()
    Stat.SbrosStatistic()
    NomIteration = 1
    pg.NomSolution = 0
    KolAntZero=0
    clearOptimPath()
    KolAntEnd=Ant.N
    KolIterationEnd=Setting.KolIteration
    NomIterationTime=Setting.KolIteration/Stat.KolTimeDelEl
    GoTime.setStartTime()
    GoTime.setTimeIteration()
    
def SaveTimeFromFile():
     global NomIterationTime
     global NomIteration      
     global TimeIteration       
     #Сохранение времени в файл
     if (NomIteration == NomIterationTime):
         Stat.SaveTime(NomIteration/Setting.KolIteration*Stat.KolTimeDelEl,(GoTime.DeltTimeIteration()).total_seconds())
        # print(NomIterationTime,datetime.now()-TimeIteration)
         GoTime.setTimeIteration() 
         NomIterationTime=NomIterationTime+Setting.KolIteration/Stat.KolTimeDelEl       

def GiveAntPheromonAndHash(pg,PathWay,NomAnt):
    global OptimPath 
    global maxHashWay
    # Получение нового пути в графе
    # Получения значения целевой функции
    Ant.AntArr[NomAnt].pheromon = Klaster.GetObjectivFunction(pg.GetWayGraphValue(Ant.AntArr[NomAnt].way),pg.TypeKlaster)
    # Добавление нового ключа в Хэш-таблицу
    Hash.addPath(PathWay,Ant.AntArr[NomAnt].pheromon)
    if Setting.GoSaveMap2==1:
        SaveMap.AddElMap2(Ant.AntArr[NomAnt].way[0], Ant.AntArr[NomAnt].way[1], pg.NomSolution)
    if Ant.AntArr[NomAnt].pheromon>maxHashWay:
        maxHashWay=Ant.AntArr[NomAnt].pheromon
        OptimPath=PathWay
    Stat.ProcBestOF(Ant.AntArr[NomAnt].pheromon,NomIteration,pg.NomSolution)

def GoPathWayHash(pg,NomAnt):
    PathWay=Hash.goPathStr(Ant.AntArr[NomAnt].way)
    HashWay = Hash.getPath(PathWay)
    if HashWay==0:   
        pg.NomSolution = pg.NomSolution+1
        GiveAntPheromonAndHash(pg,PathWay,NomAnt)
    return HashWay

def EndSolution(NomAnt,NomIteration):
    KolAntEnd=NomAnt 
    KolIterationEnd=NomIteration
    print(KolAntEnd,KolIterationEnd)
    return KolAntEnd,KolIterationEnd
    
print(GoTime.now(),' Start Program ')    
if os.path.exists('setting.ini'):
    Setting.readSetting('setting.ini')

clearOptimPath()
print('Go Parametric Graph')
# Создание параметрического графа
NameFile=os.getcwd()+'/ParametricGraph/'+Setting.NameFileGraph
#Klaster.TypeKlaster,MaxIter,Stat.BestOF,Stat.LowOF = pg.ReadParametrGraphExcelFile(NameFile)
Stat=St.stat()
Par=Setting.GoNZTypeParametr(Setting.typeParametr)
wayPg = pg.ProbabilityWay(NameFile)
wayGT = gt.GraphWay(NameFile)
#wayPg.pg.PrintParametricGraph(1)
NameFileRes = os.getcwd()+'/'+'res.xlsx'
Stat.SaveParametr(version,NameFileRes,Ant.N,Ant.Ro,Ant.Q,pg.PG.alf1,pg.PG.alf2,pg.PG.alf3,pg.PG.koef1,pg.PG.koef2,pg.PG.koef3,pg.PG.typeProbability,pg.PG.EndAllSolution,NameFile,Setting.AddFeromonAntZero,Setting.SbrosGraphAllAntZero,Setting.goNewIterationAntZero,Setting.goGraphTree,gt.SortPheromon,Setting.KolIteration,Setting.KolStatIteration,Setting.MaxkolIterationAntZero,Setting.typeParametr,len(wayPg.pg.ParametricGraph),wayPg.pg.OF,wayPg.pg.MinOF)
print('Go')
while Par<=Setting.endParametr:
    Stat.StartStatistic()
    Stat.StartStatisticGrahTree(len(wayPg.pg.ParametricGraph))
    if Setting.GoSaveMap2==1:
        SaveMap.CreateElMap2(len(wayPg.pg.ParametricGraph[0].node), len(wayPg.pg.ParametricGraph[1].node))
    NomStatIteration = 0
    while NomStatIteration<Setting.KolStatIteration:
        GoTime.setPrintTime()
        NomStatIteration,Par=St.JSONFile.LoadIterJSONFileIfExist(Stat,Par)
        clearStartIteration(Stat,wayPg.pg)
        while NomIteration<KolIterationEnd:
            SaveTimeFromFile()
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
                    HashWay=GoPathWayHash(wayPg.pg,NomAnt)
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
                                    HashWay=GoPathWayHash(wayPg.pg,NomAnt)
                            Stat.StatIterationAntZero(kolIterationAntZero)
                        
                        #Если путь не найден, то обход графа в виде дерева 
                        if Setting.goGraphTree==1:
                          try:
                              gt.StartWayGraphTree=Ant.AntArr[NomAnt].way 
                              Ant.AntArr[NomAnt].way=next(wayGT)
                          except StopIteration:
                              KolAntEnd,KolIterationEnd=EndSolution(NomAnt,NomIteration) 
                          else:
                              HashWay=GoPathWayHash(wayGT.pg,NomAnt)
                              Stat.StatIterationAntZero(gt.KolIterWay) 
                              Stat.StatIterationAntZeroGraphTree(gt.NomElKolIterWay)
                    # Переход к следующему агенту
                    NomAnt=NomAnt+1
                
            #Все агенты не нашли новых путей в графе
            Stat.ProcAntZero = Stat.ProcAntZero+KolAntZero/Ant.N
            if KolAntZero==Ant.N:
                if Setting.SbrosGraphAllAntZero==1:
                  wayPg.pg.ClearPheromon()  
                Stat.KolAllAntZero = Stat.KolAllAntZero+1
                Stat.StatAllAntZero(NomIteration, wayPg.pg.NomSolution)
    
            # Испарение феромона
            wayPg.pg.DecreasePheromon(Ant.Ro)
                
            # Добавление феромона
            NomAnt=0
            while NomAnt<KolAntEnd:
                if Ant.AntArr[NomAnt].pheromon!=0:
                    NomWay = 0
                    while NomWay<len(Ant.AntArr[NomAnt].way):
                        wayPg.pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].pheromon = wayPg.pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].pheromon + (1-Ant.Ro)*Ant.AntArr[NomAnt].pheromon
                        wayPg.pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].KolSolution = wayPg.pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].KolSolution + 1
                        NomWay = NomWay+1
                NomAnt=NomAnt+1
            
            # Переход к следующей итерации
            if pg.PG.typeProbability==1:
                wayPg.pg.NormPheromon()
            Ant.DelAllAgent()
            NomIteration=NomIteration+1

        
        
        Stat.EndStatistik(NomIteration, wayPg.pg.NomSolution)
        Stat.SaveTimeIteration((GoTime.DeltStartTime()).total_seconds())
        NomStatIteration=NomStatIteration+1
        St.JSONFile.SaveIterJSONFile(Stat,NomStatIteration,Par)

        print(GoTime.now(),' END ',(GoTime.DeltStartTime())*(Setting.KolStatIteration-NomStatIteration),' typeParametr=',Setting.typeParametr,Par,' NomStatIteration ',NomStatIteration,"{:8.3f}".format(Stat.MIterationAntZero/NomStatIteration),' Duration: {} '.format(GoTime.DeltStartTime()),' OptimPath ',OptimPath,version)
           
    
    St.JSONFile.RemoveJSONFile()
    Stat.SaveStatisticsExcel(NameFileRes,GoTime.DeltStartTime(),NomStatIteration,OptimPath,Par)
    if Setting.GoSaveMap2==1:
        SaveMap.PrintElMap2(os.getcwd()+'/'+'MapFile.xlsx')
    Par=Par+Setting.shagParametr
    Setting.EndTypeParametr(Setting.typeParametr,Par)



