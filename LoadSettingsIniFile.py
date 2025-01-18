# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 15:32:14 2022

@author: Юрий
"""
import configparser  

import ParametricGraph
import Ant
import VirtualKlaster
import Stat
import GraphTree


endprint = 0                        # Статистика. Вывод в конце прогона на экран
AddFeromonAntZero = 0               # Муравьи Zero берут количество феромона из Хэш-таблицы
SbrosGraphAllAntZero = 1            # Сброс графа решений при выполнении AllAntZero
goNewIterationAntZero = 0           # Муравей Zero ищет путь, пока не найдет уникальный
goGraphTree = 1                     # Муравей Zero перемещается по дереву
KolIteration=10000 #10 000
KolStatIteration = 5 # 500
MaxkolIterationAntZero = 10
endParametr = 100
shagParametr = 5
typeParametr = 1
GoSaveMap2=0
GoParallelAnt=0
KolParallelAnt=0
NameFileGraph='test1.xlsx'
SocketKolCluster=0
SocketIp='127.0.0.1'
SocketPort=8080
SocketClusterTime=0
KolParetto = 2
GoLoadParetto = 0
KolSborStatIteration= 20
ShagIterationStatistics = 100

def readSetting(NameFile):
    global endprint
    global AddFeromonAntZero
    global SbrosGraphAllAntZero
    global goNewIterationAntZero
    global goGraphTree
    global KolIteration
    global KolStatIteration
    global MaxkolIterationAntZero
    global endParametr
    global shagParametr
    global typeParametr
    global NameFileGraph
    global KolTimeDelEl
    global GoSaveMap2
    global GoParallelAnt
    global KolParallelAnt
    global KolParetto
    global GoLoadParetto
    global KolSborStatIteration
    global ShagIterationStatistics

    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read(NameFile)  # читаем конфиг
    endprint=int(config["setting_global"]["endprint"])  
    endParametr=float(config["setting_global"]["endParametr"]) 
    typeParametr=int(config["setting_global"]["typeParametr"])   
    shagParametr=float(config["setting_global"]["shagParametr"]) 
    AddFeromonAntZero=int(config["setting_global"]["AddFeromonAntZero"])    
    SbrosGraphAllAntZero=int(config["setting_global"]["SbrosGraphAllAntZero"])   
    goNewIterationAntZero=int(config["setting_global"]["goNewIterationAntZero"])   
    goGraphTree=int(config["setting_global"]["goGraphTree"])   
    KolIteration=int(config["setting_global"]["KolIteration"])   
    KolStatIteration=int(config["setting_global"]["KolStatIteration"])   
    MaxkolIterationAntZero=int(config["setting_global"]["MaxkolIterationAntZero"]) 
    KolTimeDelEl=int(config["setting_global"]["KolTimeDelEl"]) 
    NameFileGraph=config["setting_global"]["NameFileGraph"]
    GoSaveMap2=int(config["setting_global"]["GoSaveMap2"])
    GoParallelAnt = int(config["setting_global"]["GoParallelAnt"])
    KolParallelAnt = int(config["setting_global"]["KolParallelAnt"])
    KolParetto = int(config["setting_global"]["KolParetto"])
    GoLoadParetto = int(config["setting_global"]["GoLoadParetto"])
    KolSborStatIteration = int(config["setting_global"]["KolSborStatIteration"])
    ShagIterationStatistics = KolIteration // KolSborStatIteration

    Ant.N=float(config["ant"]["N"]) 
    Ant.Q=float(config["ant"]["Q"]) 
    Ant.Ro=float(config["ant"]["Ro"]) 
    Ant.KolElitAgent=int(config["ant"]["KolElitAgent"]) 
    Ant.DeltZeroPheromon=int(config["ant"]["DeltZeroPheromon"])
    
    ParametricGraph.PG.alf1=float(config["ParametricGraph"]["alf1"]) 
    ParametricGraph.PG.alf2=float(config["ParametricGraph"]["alf2"]) 
    ParametricGraph.PG.alf3=float(config["ParametricGraph"]["alf3"]) 
    ParametricGraph.PG.koef1=float(config["ParametricGraph"]["koef1"])
    ParametricGraph.PG.koef2=float(config["ParametricGraph"]["koef2"] )
    ParametricGraph.PG.koef3=float(config["ParametricGraph"]["koef3"] )
    ParametricGraph.PG.typeProbability=int(config["ParametricGraph"]["typeProbability"]) 
    ParametricGraph.PG.EndAllSolution=int(config["ParametricGraph"]["EndAllSolution"])
    ParametricGraph.PG.KoefLineSummPareto = float(config["ParametricGraph"]["KoefLineSummPareto"])

    GraphTree.SortPheromon=int(config["graph_tree"]["SortPheromon"]) 
    GraphTree.HorizontalTree=int(config["graph_tree"]["HorizontalTree"])
    
    VirtualKlaster.VivodKlasterExcel=int(config["VirtualKlaster"]["VivodKlasterExcel"]) 
    Stat.lenProcIS=int(config["Stat"]["lenProcIS"]) 
    Stat.KolTimeDelEl=int(config["Stat"]["KolTimeDelEl"])


def readSettingVirtualClaster(NameFile):    
    global SocketKolCluster
    global SocketIp
    global SocketPort
    global SocketClusterTime
    
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read(NameFile)  # читаем конфиг
 
    SocketKolCluster=int(config["Cluster"]["SocketKolCluster"]) 
    SocketIp=config["Cluster"]["SocketIp"]
    SocketPort=int(config["Cluster"]["SocketPort"]) 
    SocketClusterTime=float(config["Cluster"]["SocketClusterTime"])
    print(SocketIp,SocketPort)

def GoNZTypeParametr(typeParametr):
    global KolIteration
    global MaxkolIterationAntZero
    global KolParallelAnt
    if typeParametr==1:
      return Ant.N  
    elif typeParametr==2:
      return Ant.Ro 
    elif typeParametr==3:
      return Ant.Q 
    elif typeParametr==4:
      return ParametricGraph.PG.alf1  
    elif typeParametr==5:
      return ParametricGraph.PG.alf2 
    elif typeParametr==6:
      return ParametricGraph.PG.koef1     
    elif typeParametr==7:
      return ParametricGraph.PG.koef2 
    elif typeParametr==8:
      return KolIteration
    elif typeParametr==9:
      return MaxkolIterationAntZero  
    elif typeParametr==10:
      return ParametricGraph.PG.alf3  
    elif typeParametr==11:
      return ParametricGraph.PG.koef3
    elif typeParametr == 12:
      return KolParallelAnt
    
def EndTypeParametr(typeParametr,Par):
    global KolIteration
    global MaxkolIterationAntZero
    global KolParallelAnt
    if typeParametr==1:
      Ant.N=Par   
    elif typeParametr==2:
      Ant.Ro=Par  
    elif typeParametr==3:
      Ant.Q=Par  
    elif typeParametr==4:
      ParametricGraph.PG.alf1=Par   
    elif typeParametr==5:
      ParametricGraph.PG.alf2=Par  
    elif typeParametr==6:
      ParametricGraph.PG.koef1=Par      
    elif typeParametr==7:
      ParametricGraph.PG.koef2=Par  
    elif typeParametr==8:
      KolIteration=Par 
    elif typeParametr==9:
      MaxkolIterationAntZero=Par  
    elif typeParametr==10:
      ParametricGraph.PG.alf3=Par 
    elif typeParametr==11:
      ParametricGraph.PG.koef3=Par
    elif typeParametr==12:
      KolParallelAnt=Par
      
