# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 09:28:44 2022

@author: Юрий
"""

import sys #для максимального отрицательного числа

AntArr =[]
ElitAntArr = []
N = 5  #20
Q = 2  #2
Ro = 0.9  #0.9
KolElitAgent = 0 #0
DeltZeroPheromon = 0

class Ant:
   def __init__(self):
       self.way = []
       self.OF = 0
       self.ignore = 0
       self.ZeroAnt = 0
       self.kolIterationAntZero = 0
       
def DelAllAgent():
    NomAnt=0
    while NomAnt<len(AntArr):
        AntArr[NomAnt].way.clear()
        NomAnt=NomAnt+1
    AntArr.clear()

def AddAntArray():
    ant=Ant()
    AntArr.append(ant)
    return len(AntArr)

def CreateAntArray(n):
    i=1
    while i<n:
        ant=Ant()
        AntArr.append(ant)  
        i=i+1
       
def EndIteration():
    end=1
    return end

def createElitAgent(optMax = True):
    global ElitAntArr
    i=0
    while i<KolElitAgent:
        ant=Ant()
        if optMax:
            ant.OF=-sys.maxsize - 1
        else:
            ant.OF=+sys.maxsize - 1
        ElitAntArr.append(ant)
        i=i+1

def addElitAgent(ant,reversemax=True):
    global ElitAntArr
    newAnt=Ant()
    newAnt.OF=ant.OF
    newAnt.way = ant.way[:]
    ElitAntArr.append(newAnt)
    ElitAntArr.sort(key=lambda x: x.OF, reverse=reversemax)
#    nom=0
#    while nom<len(ElitAntArr):
#        print(nom,ElitAntArr[nom].OF,ElitAntArr[nom].way)
#        nom=nom+1
#    print()
    
    if len(ElitAntArr) > KolElitAgent:
        ElitAntArr = ElitAntArr[:KolElitAgent]


    
