# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 13:05:50 2022

Module on a parametric graph.
This module is designed to store the parametric graph itself. The module defines the structure of a two-dimensional array.
The procedures for creating a parametric graph are described.
Each vertex of a parametric graph is a class. This class has a parameter value. Pheromone is supposed to be added in other modules.

@author: Юрий
"""

import win32com.client #Для загрузки из Excel
import random

def SearchPGName(NameFile):
    i=0
    while i<len(PG.ArrayAllPG) and PG.ArrayAllPG[i].NameFilePg!=NameFile:
        i=i+1
    if i<len(PG.ArrayAllPG):
        return PG.ArrayAllPG[i],i
    else:
        return False,0

class PG:
    ArrayAllPG=[]
    alf1 = 1  #1
    alf2 = 1  #1
    alf3 = 1
    koef1 = 1 #1
    koef2 = 1 #1
    koef3 = 0
    typeProbability = 3
    EndAllSolution = 0
    NomCurrentPG=0
    def __init__(self,NameFile):
        self.ParametricGraph=[] #Параметрический граф
        self.AllSolution = 1    #Общее количество решений в параметрическом графе
        self.NomSolution=0
        self.NameFilePg=NameFile
        self.TypeKlaster=1
        self.MaxIter=0
        self.BestOF=0
        self.LowOF=0
        
    def ReadParametrGraphExcelFile(self):
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(self.NameFilePg)
        sheet = wb.ActiveSheet
        # Настройки графа
        self.TypeKlaster = sheet.Cells(2,1).value
        self.KolSolution = sheet.Cells(2,2).value
        self.OF = sheet.Cells(1,11).value
        self.MinOF = sheet.Cells(1,12).value
        # Загрузка самого граа
        i=1
        val = sheet.Cells(4,1).value
        while val != None :
            new_parametr=Parametr(val)
            parametr_array=[]
            j=5
            val = sheet.Cells(j,i).value
            while val != None :
                new_node=Node(val)
                parametr_array.append(new_node)
                j=j+1
                val = sheet.Cells(j,i).value
            new_parametr.node=parametr_array
            self.ParametricGraph.append(new_parametr)
            i=i+1
            val = sheet.Cells(4,i).value
        self.AllSolution=GiveAllSolutionPG(self.ParametricGraph)
        wb.Close()
        Excel.Quit()
        return self.TypeKlaster,self.KolSolution,self.OF,self.MinOF

    def PrintParametricGraph(self,VivodPheromon):
        for elem in self.ParametricGraph:
            print("Node name - ",elem.name)
            PrintParametr(elem,VivodPheromon)
            print( );
    
    def NormPheromon(self):
        NomPar=0
        while NomPar<len(self.ParametricGraph):
            MaxP=0
            MaxK=0
            NomEl=0
            while NomEl<len(self.ParametricGraph[NomPar].node):
                if self.ParametricGraph[NomPar].node[NomEl].pheromon==0:
                    self.ParametricGraph[NomPar].node[NomEl].pheromon=0.00000001
                if self.ParametricGraph[NomPar].node[NomEl].pheromon>MaxP:
                    MaxP=self.ParametricGraph[NomPar].node[NomEl].pheromon
                if self.ParametricGraph[NomPar].node[NomEl].KolSolution>MaxK:
                    MaxK=self.ParametricGraph[NomPar].node[NomEl].KolSolution
                NomEl=NomEl+1
            NomEl=0
            while NomEl<len(self.ParametricGraph[NomPar].node):
                if MaxP!=0:
                    self.ParametricGraph[NomPar].node[NomEl].pheromonNorm=self.ParametricGraph[NomPar].node[NomEl].pheromon/MaxP
                if MaxK!=0:
                    self.ParametricGraph[NomPar].node[NomEl].KolSolutionNorm=self.ParametricGraph[NomPar].node[NomEl].KolSolution/MaxK
                NomEl=NomEl+1
            NomPar=NomPar+1        

    def ClearPheromon(self):
        NomPar=0
        while NomPar<len(self.ParametricGraph):
            self.ParametricGraph[NomPar].ClearAllNode()
            NomPar=NomPar+1    

    def DecreasePheromon(self,par):
        NomPar=0
        while NomPar<len(self.ParametricGraph):
            self.ParametricGraph[NomPar].DecreasePheromon(par)
            NomPar=NomPar+1

    def GetWayGraphValue(self,path):
        way =[]
        i=0 
        while i<len(path):
            way.append(self.ParametricGraph[i].node[path[i]].val)
            i=i+1
        return way

class Node:  #Узел графа
    def __init__(self,value):
        self.clear()
        self.val = value
        
    def clear(self):
        self.pheromon=1
        self.KolSolution=0
        self.pheromonNorm = 1
        self.KolSolutionNorm = 1 
        
    def DecreasePheromon(self,par):
        self.pheromon=self.pheromon*par
        
class Parametr:
   def __init__(self,value):
       self.name = value 
       self.node=[]
       
   def ClearAllNode(self):
       NomEl=0
       while NomEl<len(self.node):
           self.node[NomEl].clear()
           NomEl=NomEl+1
           
   def DecreasePheromon(self,par):
       NomEl=0
       while NomEl<len(self.node):
           self.node[NomEl].DecreasePheromon(par)
           NomEl=NomEl+1
                                
class ProbabilityWay:
    def __init__(self,NameFile):  
        global NomCurrentPG
        self.pg,NomCurrentPG=SearchPGName(NameFile)
        if self.pg==False:
            self.pg=PG(NameFile)
            self.pg.ReadParametrGraphExcelFile()
            print(self.pg.NameFilePg)
            NomCurrentPG=len(PG.ArrayAllPG)
            PG.ArrayAllPG.append(self.pg)
            
        
    def __iter__(self):
        return self

    def __next__(self):
        # Здесь мы обновляем значение и возвращаем результат
        #Выбор первого слоя параметров
        if self.pg.NomSolution<self.pg.AllSolution:
            way=[]
            NomParametr=0
            # Окончание движения агента
            while NomParametr<len(self.pg.ParametricGraph):
                # Получение вершины из слоя
                way.append(GoAntNextNode(self.pg,self.pg.ParametricGraph[NomParametr].node))
                # Выбор следующего слоя
                NomParametr = NextNode(NomParametr)
            #print(way)
            return way
        else:
            raise StopIteration
        

def GiveAllSolutionPG(PG):
    Nom=0
    AllSolution = 1
    while Nom<len(PG):
        AllSolution=AllSolution*len(PG[Nom].node)
        Nom=Nom+1
    return AllSolution
       
def PrintParametr(Par:Parametr,VivodPheromon):
    for elem in Par.node:
        if VivodPheromon==0:
            print(elem.val, end=' ')
        else:
            print(elem.val,'(',elem.pheromon,')', end=' ')


def NextNode(nom):
    nom=nom+1
    return nom

def ProbabilityNode(ParametricGraph,Node):
    kolSolution= Node.KolSolution
    if kolSolution==0:
        kolSolution=0.5
    if PG.typeProbability==0:
        Probability=PG.koef1*(Node.pheromon**PG.alf1)+PG.koef2*(1/(kolSolution))**PG.alf2 
    elif PG.typeProbability==1:
        Probability=PG.koef1*(Node.pheromonNorm**PG.alf1)+PG.koef2*(1/(kolSolution))**PG.alf2 
    elif PG.typeProbability==2:
        Probability=(Node.pheromon**PG.alf1)*(1/(kolSolution**PG.alf2))
    elif PG.typeProbability==3:
        Probability=PG.koef1*(Node.pheromonNorm**PG.alf1)+PG.koef2*(1/(kolSolution))**PG.alf2+PG.koef3*(kolSolution/(ParametricGraph.AllSolution))**PG.alf3
    if Probability==0:
        Probability=0.00000001
    return Probability
       
def GoAntNextNode(ParametricGraph,ArrayNode):
    probability = []
    sum=0
    i=0
    while i<len(ArrayNode):
       if (PG.EndAllSolution==0) or (ParametricGraph.AllSolution!=ArrayNode[i].KolSolution): 
           sum=sum + ProbabilityNode(ParametricGraph,ArrayNode[i])
       probability.append(sum)
       i=i+1
    rnd=random.random()
    i=0
    while rnd>probability[i]/sum:
        i=i+1
    return i