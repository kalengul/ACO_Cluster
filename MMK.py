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
import Stat
import GraphTree as gt
import SaveMap
import GoTime

version='1.4.0'
dateversion='05.12.2022'

def clearOptimPath():
    global OptimPath
    global maxHashWay
    OptimPath=''
    maxHashWay=-100000000
    
def clearStartIteration():
    global NomIteration
    global NomSolution
    global KolAntZero
    global KolAntEnd
    global KolIterationEnd
    global NomIterationTime
    pg.ClearPheromon()
    Hash.HashPath.clear()
    Hash.MaxPath.clear()
    Stat.SbrosStatistic()
    NomIteration = 1
    NomSolution = 0
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

def GiveAntPheromonAndHash(PathWay,NomAnt,NomSolution):
    global OptimPath 
    global maxHashWay
    # Получение нового пути в графе
    # Получения значения целевой функции
    Ant.AntArr[NomAnt].pheromon = Klaster.GetObjectivFunction(pg.GetWayGraphValue(Ant.AntArr[NomAnt].way))
    # Добавление нового ключа в Хэш-таблицу
    Hash.addPath(PathWay,Ant.AntArr[NomAnt].pheromon)
    if Setting.GoSaveMap2==1:
        SaveMap.AddElMap2(Ant.AntArr[NomAnt].way[0], Ant.AntArr[NomAnt].way[1], NomSolution)
    if Ant.AntArr[NomAnt].pheromon>maxHashWay:
        maxHashWay=Ant.AntArr[NomAnt].pheromon
        OptimPath=PathWay
    Stat.ProcBestOF(Ant.AntArr[NomAnt].pheromon,NomIteration,NomSolution)

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
print(NameFile)
Klaster.TypeKlaster,MaxIter,Stat.BestOF,Stat.LowOF = pg.ReadParametrGraphExcelFile(NameFile)
Par=Setting.GoNZTypeParametr(Setting.typeParametr)
NameFileRes = os.getcwd()+'/'+'res.xlsx'
Stat.SaveParametr(version,NameFileRes,Ant.N,Ant.Ro,Ant.Q,Ant.alf1,Ant.alf2,Ant.koef1,Ant.koef2,Ant.typeProbability,NameFile,Setting.AddFeromonAntZero,Setting.SbrosGraphAllAntZero,Setting.goNewIterationAntZero,Setting.goGraphTree,gt.SortPheromon,Setting.KolIteration,Setting.KolStatIteration,Setting.MaxkolIterationAntZero,Setting.typeParametr,len(pg.ParametricGraph))
print('Go')
while Par<=Setting.endParametr:
    Stat.StartStatistic()
    Stat.StartStatisticGrahTree(len(pg.ParametricGraph))
    if Setting.GoSaveMap2==1:
        SaveMap.CreateElMap2(len(pg.ParametricGraph[0].node), len(pg.ParametricGraph[1].node))
    NomStatIteration = 0
    while NomStatIteration<Setting.KolStatIteration:
        GoTime.setPrintTime()
        clearStartIteration()
        while NomIteration<KolIterationEnd:
            SaveTimeFromFile()
            #Создание агентов
            Ant.CreateAntArray(Ant.N+1)
            NomAnt=0
            KolAntZero=0
            # Проход по всем агентам
            while NomAnt<KolAntEnd:
                #Выбор первого слоя параметров
                NomParametr=0
                # Окончание движения агента
                while NomParametr<len(pg.ParametricGraph):
                    # Получение вершины из слоя
                    node=Ant.GoAntNextNode(Ant.AntArr[NomAnt],pg.ParametricGraph[NomParametr].node)
                    # Выбор следующего слоя
                    NomParametr = Ant.NextNode(NomParametr)
                # Проверка полученного пути в Хэш-Таблице
                PathWay=Hash.goPathStr(Ant.AntArr[NomAnt].way)
                HashWay = Hash.getPath(PathWay)
                if HashWay==0:   
                    NomSolution = NomSolution+1
                    GiveAntPheromonAndHash(PathWay,NomAnt,NomSolution)
                else:
                    # Такой путь уже есть в Хэш-таблице
                    if Setting.AddFeromonAntZero==0:
                        Ant.AntArr[NomAnt].pheromon=0
                    else:
                        Ant.AntArr[NomAnt].pheromon=HashWay
                    Stat.KolAntZero = Stat.KolAntZero+1
                    KolAntZero = KolAntZero+1
                    
                    if Setting.goNewIterationAntZero==1:
                        #Если путь не найден, то продолжать генерацию маршрутов, пока не найдется уникальный
                        kolIterationAntZero=0
                        while HashWay!=0 and kolIterationAntZero<Setting.MaxkolIterationAntZero:
                            Ant.AntArr[NomAnt].way.clear()
                            NomParametr=0
                            while NomParametr<len(pg.ParametricGraph):
                                node=Ant.GoAntNextNode(Ant.AntArr[NomAnt],pg.ParametricGraph[NomParametr].node)
                                NomParametr = Ant.NextNode(NomParametr)
                            PathWay=Hash.goPathStr(Ant.AntArr[NomAnt].way)
                            HashWay = Hash.getPath(PathWay)
                            kolIterationAntZero = kolIterationAntZero+1
                        if kolIterationAntZero<Setting.MaxkolIterationAntZero:
                            NomSolution = NomSolution+1
                            GiveAntPheromonAndHash(PathWay,NomAnt,NomSolution)
                        Stat.StatIterationAntZero(kolIterationAntZero)
                    
                    #Если путь не найден, то обход графа в виде дерева 
                    if Setting.goGraphTree==1:
                      Ant.AntArr[NomAnt].way=gt.GoPathGraphTree(Ant.AntArr[NomAnt].way)
                      if Ant.AntArr[NomAnt].way==[]:
                          KolAntEnd,KolIterationEnd=EndSolution(NomAnt,NomIteration)
                      else:
                          PathWay=Hash.goPathStr(Ant.AntArr[NomAnt].way)
                          NomSolution = NomSolution+1
                          GiveAntPheromonAndHash(PathWay,NomAnt,NomSolution)
                          Stat.StatIterationAntZero(gt.KolIterWay) 
                          Stat.StatIterationAntZeroGraphTree(gt.NomElKolIterWay)
                # Переход к следующему агенту
                NomAnt=NomAnt+1
                
            #Все агенты не нашли новых путей в графе
            Stat.ProcAntZero = Stat.ProcAntZero+KolAntZero/Ant.N
            if KolAntZero==Ant.N:
                if Setting.SbrosGraphAllAntZero==1:
                  pg.ClearPheromon()  
                Stat.KolAllAntZero = Stat.KolAllAntZero+1
                Stat.StatAllAntZero(NomIteration, NomSolution)
    
            # Испарение феромона
            pg.DecreasePheromon(Ant.Ro)
                
            # Добавление феромона
            NomAnt=0
            while NomAnt<KolAntEnd:
                if Ant.AntArr[NomAnt].pheromon!=0:
                    NomWay = 0
                    while NomWay<len(Ant.AntArr[NomAnt].way):
                        pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].pheromon = pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].pheromon + (1-Ant.Ro)*Ant.AntArr[NomAnt].pheromon
                        pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].KolSolution = pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].KolSolution + 1
                        NomWay = NomWay+1
                NomAnt=NomAnt+1
            
            #Проверить сколько решений осталось
            if Hash.KolHash()==pg.AllSolution:
                KolAntEnd,KolIterationEnd=EndSolution(NomAnt,NomIteration)
            
            # Переход к следующей итерации
            if Ant.typeProbability==1:
                pg.NormPheromon()
            Ant.DelAllAgent()
            NomIteration=NomIteration+1
            

        Stat.EndStatistik(NomIteration, NomSolution)
        Stat.SaveTimeIteration((GoTime.DeltStartTime()).total_seconds())
        NomStatIteration=NomStatIteration+1
        print(GoTime.now(),' END ',(GoTime.DeltStartTime())*(Setting.KolStatIteration-NomStatIteration),' typeParametr=',Setting.typeParametr,Par,' NomStatIteration ',NomStatIteration,"{:8.3f}".format(Stat.MIterationAntZero/NomStatIteration),' Duration: {} '.format(GoTime.DeltStartTime()),' OptimPath ',OptimPath,version)
           
        
    Stat.SaveStatisticsExcel(NameFileRes,GoTime.DeltStartTime(),NomStatIteration,OptimPath,Par)
    if Setting.GoSaveMap2==1:
        SaveMap.PrintElMap2(os.getcwd()+'/'+'MapFile.xlsx')
    Par=Par+Setting.shagParametr
    Setting.EndTypeParametr(Setting.typeParametr,Par)



