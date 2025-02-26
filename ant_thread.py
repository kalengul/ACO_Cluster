# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:13:31 2024

@author: Юрий
"""
import LoadSettingsIniFile as Setting
import VirtualKlaster as Klaster
import GraphTree as gt
import Hash
import Ant

def AddDeltZeroPheromon(pg,delt):
        #Пройти во всем слоям параметрического графа
        NomParametr=0
        while NomParametr<len(pg.ParametricGraph):
            NomNode=0
            #Пройти по всем вершинам слоя параметрического графа
            while NomNode<len(pg.ParametricGraph[NomParametr].node):
                #Пройти по всем элементам массива итераций
                NomSolution=0
                while NomSolution<len(pg.ParametricGraph[NomParametr].node[NomNode].KolSolutionIteration):
                    pg.ParametricGraph[NomParametr].node[NomNode].pheromon=pg.ParametricGraph[NomParametr].node[NomNode].pheromon+((1-Ant.Ro)*Ant.Q)**(len(pg.ParametricGraph[NomParametr].node[NomNode].KolSolutionIteration)-NomSolution)*delt*pg.ParametricGraph[NomParametr].node[NomNode].KolSolutionIteration[NomSolution]
                    NomSolution=NomSolution+1
                NomNode=NomNode+1
            NomParametr=NomParametr+1

def GiveAntPheromonAndHash(pg,PathWay,ant):
        # Получение нового пути в графе
        # Получения значения целевой функции
        if Setting.SocketKolCluster==0:
           ant.OF = Klaster.GetObjectivFunction(pg.GetWayGraphValue(ant.way),pg.TypeKlaster,Setting.SocketClusterTime)
        #elif Setting.SocketCluster==1:
        #    Ant.AntArr[NomAnt].OF = ClientSocket.SocketSendOF(Stat,pg.GetWayGraphValue(Ant.AntArr[NomAnt].way),pg.TypeKlaster)
        # Добавление нового ключа в Хэш-таблицу
        Hash.addPath(PathWay,ant.OF)
        #Проверка на отрицательный феромон
        if Ant.DeltZeroPheromon != 0:
            if ant.OF+pg.difZero<0:
                #Учет смещения в каждой вершине параметрического графа
                AddDeltZeroPheromon(pg,abs(pg.difZero+ant.OF))
                #Установка нового значения смещения
                pg.difZero=abs(ant.OF)
        return 0
    
def GoPathWayHash(pg,ant):
        PathWay=Hash.goPathStr(ant.way)
        FindHash, HashWay = Hash.getPath(PathWay)
        if FindHash==False:             
            pg.NomSolution = pg.NomSolution+1
            GiveAntPheromonAndHash(pg,PathWay,ant)
        return HashWay,FindHash

def go_ant(wayPg,wayGT,ant):
     AllSolutionAgent=False
     try:
         ant.way=next(wayPg)
     except StopIteration:
         AllSolutionAgent=True
     else:
         # Проверка полученного пути в Хэш-Таблице
         HashWay,FindHash=GoPathWayHash(wayPg.pg,ant)
         if FindHash!=False:
             ant.ZeroAnt=1;
             #Общие переменные
             #Stat.KolAntZero = Stat.KolAntZero+1
             #KolAntZero = KolAntZero+1
             # Такой путь уже есть в Хэш-таблице
             if Setting.AddFeromonAntZero==0:
                 ant.OF=0
                 ant.ignore=1
             else:
                 ant.OF=HashWay
             #Если включены повторные итерации алгоритма
             if Setting.goNewIterationAntZero==1:
                 #Если путь не найден, то продолжать генерацию маршрутов, пока не найдется уникальный
                 ant.ignore=0
                 kolIterationAntZero=0
                 while FindHash!=False and kolIterationAntZero<Setting.MaxkolIterationAntZero:
                     kolIterationAntZero = kolIterationAntZero+1
                     try:
                         ant.way=next(wayPg)
                     except StopIteration:
                         AllSolutionAgent=True
                         FindHash=False
                     else:
                         HashWay,FindHash=GoPathWayHash(wayPg.pg,ant)
                 if kolIterationAntZero==Setting.MaxkolIterationAntZero:
                     ant.ignore=1
                 ant.kolIterationAntZero=kolIterationAntZero
            
             #Если путь не найден, то обход графа в виде дерева 
             if Setting.goGraphTree==1:
               ant.ignore=0
               try:
                   gt.StartWayGraphTree=ant.way 
                   ant.way=next(wayGT)
               except StopIteration:
                   AllSolutionAgent=True 
               else:
                   HashWay,FindHash=GoPathWayHash(wayPg.pg,ant)
     return AllSolutionAgent