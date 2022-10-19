# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 15:57:32 2022

@author: Юрий
"""
import configparser  # импортируем библиотеку
import os
from datetime import datetime

import ParametricGraph as pg
import Ant
import VirtualKlaster as Klaster
import Hash
import Stat
import GraphTree as gt

version='1.3.7'
OptimPath=''
maxHashWay=-100000000

def GiveAntPheromonAndHash(PathWay,NomAnt,NomSolution):
    global OptimPath 
    global maxHashWay
    # Получение нового пути в графе
    # Получения значения целевой функции
    Ant.AntArr[NomAnt].pheromon = Klaster.GetObjectivFunction(pg.GetWayGraphValue(Ant.AntArr[NomAnt].way))
    # Добавление нового ключа в Хэш-таблицу
    Hash.addPath(PathWay,Ant.AntArr[NomAnt].pheromon)
    if Ant.AntArr[NomAnt].pheromon>maxHashWay:
        maxHashWay=Ant.AntArr[NomAnt].pheromon
        OptimPath=PathWay
    Stat.ProcBestOF(Ant.AntArr[NomAnt].pheromon,NomIteration,NomSolution)

print(datetime.now(),' Start Program ')
endprint = 0                        # Статистика. Вывод в конце прогона на экран
AddFeromonAntZero = 0               # Муравьи Zero берут количество феромона из Хэш-таблицы
SbrosGraphAllAntZero = 1            # Сброс графа решений при выполнении AllAntZero
goNewIterationAntZero = 0           # Муравей Zero ищет путь, пока не найдет уникальный
goGraphTree = 1                     # Муравей Zero перемещается по дереву

KolIteration=10000 #10 000
KolStatIteration = 5 # 500
MaxkolIterationAntZero = 10

NameFileGraph='test1.xlsx'

def readSetting(NameFile):
    global endprint
    global AddFeromonAntZero
    global SbrosGraphAllAntZero
    global SbrosGraphAllAntZero
    global goNewIterationAntZero
    global goGraphTree
    global KolIteration
    global KolStatIteration
    global MaxkolIterationAntZero
    global KolTimeDelEl
    global NameFileGraph
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read(NameFile)  # читаем конфиг
    endprint=int(config["setting_global"]["endprint"])  
    AddFeromonAntZero=int(config["setting_global"]["AddFeromonAntZero"])    
    SbrosGraphAllAntZero=int(config["setting_global"]["SbrosGraphAllAntZero"])   
    goNewIterationAntZero=int(config["setting_global"]["goNewIterationAntZero"])   
    goGraphTree=int(config["setting_global"]["goGraphTree"])   
    KolIteration=int(config["setting_global"]["KolIteration"])   
    KolStatIteration=int(config["setting_global"]["KolStatIteration"])   
    MaxkolIterationAntZero=int(config["setting_global"]["MaxkolIterationAntZero"]) 
    KolTimeDelEl=int(config["setting_global"]["KolTimeDelEl"]) 
    NameFileGraph=config["setting_global"]["NameFileGraph"]
    
    Ant.N=float(config["ant"]["N"]) 
    Ant.Q=float(config["ant"]["Q"]) 
    Ant.Ro=float(config["ant"]["Ro"]) 
    Ant.alf1=float(config["ant"]["alf1"]) 
    Ant.alf2=float(config["ant"]["alf2"]) 
    Ant.koef1=float(config["ant"]["koef1"])
    Ant.koef2=float(config["ant"]["koef2"] )
    Ant.typeProbability=int(config["ant"]["typeProbability"]) 
    
    gt.SortPheromon=int(config["graph_tree"]["SortPheromon"]) 
if os.path.exists('setting.ini'):
    readSetting('setting.ini')

print('Go Parametric Graph')
# Создание параметрического графа
NameFile=os.getcwd()+'/'+'test1no.xlsx'
print(NameFile)
Klaster.TypeKlaster,MaxIter,Stat.BestOF,Stat.LowOF = pg.ReadParametrGraphExcelFile(NameFile)
KolAnt = Ant.N
Ro = Ant.Ro

NameFileRes = os.getcwd()+'/'+'res.xlsx'
Stat.SaveParametr(version,NameFileRes,Ant.N,Ant.Ro,Ant.Q,Ant.alf1,Ant.alf2,Ant.koef1,Ant.koef2,Ant.typeProbability,NameFile,AddFeromonAntZero,SbrosGraphAllAntZero,goNewIterationAntZero,goGraphTree,gt.SortPheromon,KolIteration,KolStatIteration,MaxkolIterationAntZero)

print('Go')
while KolAnt<=100:
    Stat.StartStatistic()
    Stat.StartStatisticGrahTree(len(pg.ParametricGraph))
    NomStatIteration = 0
    
    while NomStatIteration<KolStatIteration:
        pg.ClearPheromon()
        Hash.HashPath.clear()
        Hash.MaxPath.clear()
        Stat.SbrosStatistic()
        NomIteration = 1
        NomSolution = 0
        KolAntZero=0
        OptimPath=''
        maxHashWay=-100000000
        StartTime = datetime.now()
        KolAntEnd=KolAnt
        KolIterationEnd=KolIteration
        TimeIteration = datetime.now() 
        NomIterationTime=KolIteration/Stat.KolTimeDelEl
        while NomIteration<KolIterationEnd:
           # print(NomIteration)
            # Вывод текущего параметрического графа
            #pg.PrintParametricGraph(1)
            #Сохранение времени в файл
            if (NomIteration == NomIterationTime):
                Stat.SaveTime(NomIteration/KolIteration*Stat.KolTimeDelEl,(datetime.now()-TimeIteration).total_seconds())
               # print(NomIterationTime,datetime.now()-TimeIteration)
                TimeIteration = datetime.now() 
                NomIterationTime=NomIterationTime+KolIteration/Stat.KolTimeDelEl
            
            #Создание агентов
            Ant.CreateAntArray(KolAnt+1)
            NomAnt=0
            KolAntZero = 0
            # Проход по сем агентам
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
                    if AddFeromonAntZero==0:
                        Ant.AntArr[NomAnt].pheromon=0
                    else:
                        Ant.AntArr[NomAnt].pheromon=HashWay
                    Stat.KolAntZero = Stat.KolAntZero+1
                    KolAntZero = KolAntZero+1
                    
                    if goNewIterationAntZero==1:
                        #Если путь не найден, то продолжать генерацию маршрутов, пока не найдется уникальный
                        kolIterationAntZero=0
                        while HashWay!=0 and kolIterationAntZero<MaxkolIterationAntZero:
                            Ant.AntArr[NomAnt].way.clear()
                            NomParametr=0
                            while NomParametr<len(pg.ParametricGraph):
                                node=Ant.GoAntNextNode(Ant.AntArr[NomAnt],pg.ParametricGraph[NomParametr].node)
                                NomParametr = Ant.NextNode(NomParametr)
                            PathWay=Hash.goPathStr(Ant.AntArr[NomAnt].way)
                            HashWay = Hash.getPath(PathWay)
                            kolIterationAntZero = kolIterationAntZero+1
                        if kolIterationAntZero<MaxkolIterationAntZero:
                            NomSolution = NomSolution+1
                            GiveAntPheromonAndHash(PathWay,NomAnt,NomSolution)
                        Stat.StatIterationAntZero(kolIterationAntZero)
                    
                    #Если путь не найден, то обход графа в виде дерева 
                    if goGraphTree==1:
                      Ant.AntArr[NomAnt].way=gt.GoPathGraphTree(Ant.AntArr[NomAnt].way)
                      if Ant.AntArr[NomAnt].way==[]:
                          KolAntEnd=NomAnt 
                          KolIterationEnd=NomIteration
                          print(KolAntEnd,KolIterationEnd)
                      else:
                          PathWay=Hash.goPathStr(Ant.AntArr[NomAnt].way)
                          NomSolution = NomSolution+1
                          GiveAntPheromonAndHash(PathWay,NomAnt,NomSolution)
                          Stat.StatIterationAntZero(gt.KolIterWay) 
                          Stat.StatIterationAntZeroGraphTree(gt.NomElKolIterWay)
                # Переход к следующему агенту
                NomAnt=NomAnt+1
            
            Stat.ProcAntZero = Stat.ProcAntZero+KolAntZero/KolAnt
            if KolAntZero==KolAnt:
                #Все агенты не нашли новых путей в графе
                if SbrosGraphAllAntZero==1:
                  pg.ClearPheromon()  
                Stat.KolAllAntZero = Stat.KolAllAntZero+1
                Stat.StatAllAntZero(NomIteration, NomSolution)
                
            # Испарение феромона
            pg.DecreasePheromon(Ant.Ro)
                
            # Добавление феромона
            NomAnt=0
            while NomAnt<KolAntEnd:
                NomWay = 0
                while NomWay<len(Ant.AntArr[NomAnt].way):
                    pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].pheromon = pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].pheromon + (1-Ant.Ro)*Ant.AntArr[NomAnt].pheromon
                    if Ant.AntArr[NomAnt].pheromon!=0:
                        pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].KolSolution = pg.ParametricGraph[NomWay].node[Ant.AntArr[NomAnt].way[NomWay]].KolSolution + 1
                    NomWay = NomWay+1
                NomAnt=NomAnt+1
            # Переход к следующей итерации
            if Ant.typeProbability==1:
                pg.NormPheromon()
            Ant.DelAllAgent()
            NomIteration=NomIteration+1
        
        Stat.EndStatistik(NomIteration, NomSolution)
        Stat.SaveTimeIteration((datetime.now() - StartTime).total_seconds()) #Ошибка времени
        NomStatIteration=NomStatIteration+1
        print(datetime.now(),' END ',(datetime.now() - StartTime)*(KolStatIteration-NomStatIteration),' KolAnt ',KolAnt,' NomStatIteration ',NomStatIteration,Stat.MIterationAntZero/NomStatIteration,' Duration: {} '.format(datetime.now() - StartTime),' OptimPath ',OptimPath)
        if endprint==1:  
            print('KolIteration ',NomIteration,' NomSolution ',NomSolution)
            print(Hash.GetMaxPath())
            
            print('MOFI ',Stat.MOFI)
            print('MOFS ',Stat.MOFS)
            print('MIterAllAntZero ',Stat.MIterAllAntZero)
            print('MSltnAllAntZero ',Stat.MSltnAllAntZero)
            print('MIter ',Stat.MIter)
            print('MSolution ',Stat.MSolution)
            print('KolEndIs ',Stat.KolEndIs)
        
        
        
        
    Stat.SaveStatisticsExcel(NameFileRes,datetime.now() - StartTime,NomStatIteration,OptimPath,KolAnt)
    KolAnt=KolAnt+5
    Ant.Ro=Ro
    Ant.N = KolAnt


