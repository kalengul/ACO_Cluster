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
    difZero=0
    KoefLineSummPareto=0
    ArrDifZero=[]
    typeProbability = 3
    EndAllSolution = 0
    NomCurrentPG=0
    def __init__(self,NameFile,KolDifZero):
        self.ParametricGraph=[] #Параметрический граф
        self.AllSolution = 1    #Общее количество решений в параметрическом графе
        self.NomSolution=0
        self.NameFilePg=NameFile
        self.TypeKlaster=1
        self.MaxIter=0
        self.BestOF=0
        self.LowOF=0
        self.MaxOptimization=1
        nomDifZer=0
        while nomDifZer<KolDifZero:
            self.ArrDifZero.append(0)
            nomDifZer=nomDifZer+1

        
    def ReadParametrGraphExcelFile(self):
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(self.NameFilePg)
        sheet = wb.ActiveSheet
        # Настройки графа
        self.TypeKlaster = sheet.Cells(2,1).value
        self.KolSolution = sheet.Cells(2,2).value
        self.MaxOptimization = sheet.Cells(2,3).value
        KolOF = sheet.Cells(2, 4).value
        if KolOF==None:
            KolOF=0
        else:
            KolOF=int(KolOF)
        self.OF = sheet.Cells(1,11).value
        self.MinOF = sheet.Cells(1,12).value
        # Загрузка самого графа
        i=1
        val = sheet.Cells(4,1).value
        while val != None :
            new_parametr=Parametr(val)
            parametr_array=[]
            j=5
            val = sheet.Cells(j,i).value
            while val != None :
                new_node=Node(val,KolOF)
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
            MaxPArr=[]
            nomDifZer = 0
            while nomDifZer < len(self.ParametricGraph[NomPar].node[0].ArrPheromon):
                MaxPArr.append(0)
                nomDifZer = nomDifZer + 1
            MaxK=0
            NomEl=0
            while NomEl<len(self.ParametricGraph[NomPar].node):
                #print(self.ParametricGraph[NomPar].node[NomEl].ArrPheromon,self.ParametricGraph[NomPar].node[NomEl].ArrPheromonNorm)
                if self.ParametricGraph[NomPar].node[NomEl].pheromon==0:
                    self.ParametricGraph[NomPar].node[NomEl].pheromon=0.00000001
                if self.ParametricGraph[NomPar].node[NomEl].pheromon>MaxP:
                    MaxP=self.ParametricGraph[NomPar].node[NomEl].pheromon
                if self.ParametricGraph[NomPar].node[NomEl].KolSolution>MaxK:
                    MaxK=self.ParametricGraph[NomPar].node[NomEl].KolSolution
                NomArr = 0
                while NomArr < len(MaxPArr):
                    if self.ParametricGraph[NomPar].node[NomEl].ArrPheromon[NomArr] == 0:
                        self.ParametricGraph[NomPar].node[NomEl].ArrPheromon[NomArr] = 0.00000001
                    if self.ParametricGraph[NomPar].node[NomEl].ArrPheromon[NomArr]>MaxPArr[NomArr]:
                        MaxPArr[NomArr]=self.ParametricGraph[NomPar].node[NomEl].ArrPheromon[NomArr]
                    NomArr = NomArr + 1
                NomEl=NomEl+1
            NomEl=0
            while NomEl<len(self.ParametricGraph[NomPar].node):
                NomArr = 0
                while NomArr < len(MaxPArr):
                    if MaxPArr[NomArr]!=0:
                        self.ParametricGraph[NomPar].node[NomEl].ArrPheromonNorm[NomArr] = self.ParametricGraph[NomPar].node[NomEl].ArrPheromon[NomArr]/MaxPArr[NomArr]
                    NomArr = NomArr + 1
                if MaxP!=0:
                    self.ParametricGraph[NomPar].node[NomEl].pheromonNorm=self.ParametricGraph[NomPar].node[NomEl].pheromon/MaxP
                if MaxK!=0:
                    self.ParametricGraph[NomPar].node[NomEl].KolSolutionNorm=self.ParametricGraph[NomPar].node[NomEl].KolSolution/MaxK
                #print('1 ',self.ParametricGraph[NomPar].node[NomEl].ArrPheromon,self.ParametricGraph[NomPar].node[NomEl].ArrPheromonNorm)
                NomEl=NomEl+1
            NomPar=NomPar+1        

    def ClearPheromon(self,allClear):
        self.NomSolution = 0
        self.difZero = 0
        nomDifZer = 0
        while nomDifZer < len(self.ArrDifZero):
            self.ArrDifZero[nomDifZer]=0
            nomDifZer = nomDifZer + 1
        NomPar=0
        while NomPar<len(self.ParametricGraph):
            self.ParametricGraph[NomPar].ClearAllNode(allClear)
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

    def AddIterationLayerKolSolution(self):
        #print('AddIterationLayerKolSolution')
        NomPar=0
        while NomPar<len(self.ParametricGraph):
            self.ParametricGraph[NomPar].AddIterationLayerKolSolution()
            NomPar=NomPar+1    

class Node:  #Узел графа
    def __init__(self,value,KolOF):
        self.ArrPheromon=[]
        self.ArrPheromonNorm = []
        nomDifZer = 0
        while nomDifZer < KolOF:
            self.ArrPheromon.append(1)
            self.ArrPheromonNorm.append(1)
            nomDifZer = nomDifZer + 1
        self.clear(1)
        self.val = value
        
    def clear(self,allClear):
        self.pheromon=1
        self.KolSolution=0
        self.pheromonNorm = 1
        self.KolSolutionNorm = 1
        nomDifZer = 0
        while nomDifZer < len(self.ArrPheromon):
            self.ArrPheromon[nomDifZer] = 1
            self.ArrPheromonNorm[nomDifZer] = 1
            nomDifZer = nomDifZer + 1
        if allClear==1:
            self.KolSolutionAll=0
            self.KolSolutionIteration = []
        
    def DecreasePheromon(self,par):
        self.pheromon=self.pheromon*par
        nomDifZer = 0
        while nomDifZer < len(self.ArrPheromon):
            self.ArrPheromon[nomDifZer] = self.ArrPheromon[nomDifZer]*par
            nomDifZer = nomDifZer + 1
        
class Parametr:
   def __init__(self,value):
       self.name = value 
       self.node=[]
       
   def ClearAllNode(self,allClear):
       NomEl=0
       while NomEl<len(self.node):
           self.node[NomEl].clear(allClear)
           NomEl=NomEl+1
           
   def DecreasePheromon(self,par):
       NomEl=0
       while NomEl<len(self.node):
           self.node[NomEl].DecreasePheromon(par)
           NomEl=NomEl+1
                          
   def AddIterationLayerKolSolution(self):
       NomEl=0
       while NomEl<len(self.node):
           self.node[NomEl].KolSolutionIteration.append(0)
           NomEl=NomEl+1
            
class ProbabilityWay:
    def __init__(self,NameFile,KolDifZero):
        global NomCurrentPG
        self.pg,NomCurrentPG=SearchPGName(NameFile)
        if self.pg==False:
            self.pg=PG(NameFile,KolDifZero)
            self.pg.ReadParametrGraphExcelFile()
#            print(self.pg.NameFilePg)
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
            print(elem.val,'(',elem.pheromon,elem.KolSolution,')', end=' ')


def NextNode(nom):
    nom=nom+1
    return nom

def ProbabilityNode(AllSolution,Node):
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
        Probability=PG.koef1*(Node.pheromonNorm**PG.alf1)+PG.koef2*(1/(kolSolution))**PG.alf2+PG.koef3*(Node.KolSolutionAll/(AllSolution))**PG.alf3
    elif (PG.typeProbability>=30) and (PG.typeProbability<35):
        Probability = PG.koef1 * (Node.ArrPheromonNorm[PG.typeProbability-30] ** PG.alf1) + PG.koef2 * (1 / (kolSolution)) ** PG.alf2 + PG.koef3 * (Node.KolSolutionAll / (AllSolution)) ** PG.alf3
        #print(Node.pheromonNorm,Node.ArrPheromonNorm,PG.typeProbability-30,Probability)
    elif (PG.typeProbability ==36):
        Probability = PG.koef1 * ((Node.ArrPheromonNorm[0]*(PG.KoefLineSummPareto)+Node.ArrPheromonNorm[1]*(1-PG.KoefLineSummPareto)) ** PG.alf1) + PG.koef2 * (1 / (kolSolution)) ** PG.alf2 + PG.koef3 * (Node.KolSolutionAll / (AllSolution)) ** PG.alf3
    if Probability==0:
        Probability=0.00000001
    return Probability
       
def GoAntNextNode(ParametricGraph,ArrayNode):
    probability = []
    sum=0
    i=0
    while i<len(ArrayNode):
       if (PG.EndAllSolution==0) or (ParametricGraph.AllSolution/len(ArrayNode)>ArrayNode[i].KolSolutionAll): 
           sum=sum + ProbabilityNode(ParametricGraph.AllSolution/len(ArrayNode),ArrayNode[i])
       probability.append(sum)
       i=i+1
    rnd=random.random()
    i=0
    while rnd>probability[i]/sum:
        i=i+1
    #print(probability,sum,rnd,i)
    return i