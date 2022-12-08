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

PGArray=[]

ParametricGraph=[] #Параметрический граф
AllSolution = 1    #Общее количество решений в параметрическом графе
alf1 = 1  #1
alf2 = 1  #1
koef1 = 1 #1
koef2 = 1 #1
typeProbability = 1
NomSolution=0
NameFilePg=''

class Node:  #Узел графа
    def __init__(self,value):
        self.pheromon = 1
        self.KolSolution = 0
        self.pheromonNorm = 1
        self.KolSolutionNorm = 1
        self.val = value
        
class Parametr:
   def __init__(self,value):
       self.name = value 
       self.node=[]

class ProbabilityWay:
    def __init__(self,NameFile):
        global NameFilePg
        if NameFile!=NameFilePg:
            if NameFilePg=='':
                ReadParametrGraphExcelFile(NameFile)
            NameFilePg=NameFile
        
    def __iter__(self):
        return self

    def __next__(self):
        # Здесь мы обновляем значение и возвращаем результат
        #Выбор первого слоя параметров
        if NomSolution<AllSolution:
            way=[]
            NomParametr=0
            # Окончание движения агента
            while NomParametr<len(ParametricGraph):
                # Получение вершины из слоя
                way.append(GoAntNextNode(ParametricGraph[NomParametr].node))
                # Выбор следующего слоя
                NomParametr = NextNode(NomParametr)
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
       
def ReadParametrGraphExcelFile(NameFile):
    global AllSolution
    global ParametricGraph
    Excel = win32com.client.Dispatch("Excel.Application")
    wb = Excel.Workbooks.Open(NameFile)
    sheet = wb.ActiveSheet
    # Настройки графа
    ParametricFunction = sheet.Cells(2,1).value
    KolSolution = sheet.Cells(2,2).value
    OF = sheet.Cells(1,11).value
    MinOF = sheet.Cells(1,12).value
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
        ParametricGraph.append(new_parametr)
        i=i+1
        val = sheet.Cells(4,i).value
    AllSolution=GiveAllSolutionPG(ParametricGraph)
    wb.Close()
    Excel.Quit()
    return ParametricFunction,KolSolution,OF,MinOF
           
def CreateParametrShag (start,end,shag=1):
    parametr_array=[]
    current=start
    while current<end:
        new_node=Node(current)
        parametr_array.append(new_node)
        current=current+shag
    return parametr_array

def PrintParametr(Par:Parametr,VivodPheromon):
    for elem in Par.node:
        if VivodPheromon==0:
            print(elem.val, end=' ')
        else:
            print(elem.val,'(',elem.pheromon,')', end=' ')
        
def PrintParametricGraph(VivodPheromon):
    for elem in ParametricGraph:
        print("Node name - ",elem.name)
        PrintParametr(elem,VivodPheromon)
        print( );
    
def NormPheromon():
    NomPar=0
    while NomPar<len(ParametricGraph):
        MaxP=0
        MaxK=0
        NomEl=0
        while NomEl<len(ParametricGraph[NomPar].node):
            if ParametricGraph[NomPar].node[NomEl].pheromon==0:
                ParametricGraph[NomPar].node[NomEl].pheromon=0.00000001
            if ParametricGraph[NomPar].node[NomEl].pheromon>MaxP:
                MaxP=ParametricGraph[NomPar].node[NomEl].pheromon
            if ParametricGraph[NomPar].node[NomEl].KolSolution>MaxK:
                MaxK=ParametricGraph[NomPar].node[NomEl].KolSolution
            NomEl=NomEl+1
        NomEl=0
        while NomEl<len(ParametricGraph[NomPar].node):
            if MaxP!=0:
                ParametricGraph[NomPar].node[NomEl].pheromonNorm=ParametricGraph[NomPar].node[NomEl].pheromon/MaxP
            if MaxK!=0:
                ParametricGraph[NomPar].node[NomEl].KolSolutionNorm=ParametricGraph[NomPar].node[NomEl].KolSolution/MaxK
            NomEl=NomEl+1
        NomPar=NomPar+1        

def ClearPheromon():
    NomPar=0
    while NomPar<len(ParametricGraph):
        NomEl=0
        while NomEl<len(ParametricGraph[NomPar].node):
            ParametricGraph[NomPar].node[NomEl].pheromon=1
            ParametricGraph[NomPar].node[NomEl].KolSolution=0
            ParametricGraph[NomPar].node[NomEl].pheromonNorm = 1
            ParametricGraph[NomPar].node[NomEl].KolSolutionNorm = 1
            NomEl=NomEl+1
        NomPar=NomPar+1    
    
def DecreasePheromon(par):
    NomPar=0
    while NomPar<len(ParametricGraph):
        NomEl=0
        while NomEl<len(ParametricGraph[NomPar].node):
            ParametricGraph[NomPar].node[NomEl].pheromon=ParametricGraph[NomPar].node[NomEl].pheromon*par
            NomEl=NomEl+1
        NomPar=NomPar+1
        
def GetWayGraphValue(path):
    way =[]
    i=0 
    while i<len(path):
        way.append(ParametricGraph[i].node[path[i]].val)
        i=i+1
    return way

def NextNode(nom):
    nom=nom+1
    return nom

def ProbabilityNode(Node):
    kolSolution= Node.KolSolution
    if kolSolution==0:
        kolSolution=0.5
    if typeProbability==0:
        Probability=koef1*(Node.pheromon**alf1)+koef2*(1/(kolSolution))**alf2 
    if typeProbability==1:
        Probability=koef1*(Node.pheromonNorm**alf1)+koef2*(1/(kolSolution))**alf2 
    if typeProbability==2:
        Probability=(Node.pheromon**alf1)*(1/(kolSolution**alf2))
    if Probability==0:
        Probability=0.00000001
    return Probability

       
def GoAntNextNode(ArrayNode):
    probability = []
    sum=0
    i=0
    while i<len(ArrayNode):
       sum=sum + ProbabilityNode(ArrayNode[i])
       probability.append(sum)
       i=i+1
    rnd=random.random()
    i=0
    while rnd>probability[i]/sum:
        i=i+1
    return i