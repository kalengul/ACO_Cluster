# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 09:28:44 2022

@author: Юрий
"""
AntArr =[]
ElitAntArr = []
N = 5  #20
Q = 2  #2
Ro = 0.9  #0.9
KolElitAgent = 0 #0

class Ant:
   def __init__(self):
       self.way = []
       self.pheromon = 0
       
def DelAllAgent():
    NomAnt=0
    while NomAnt<len(AntArr):
        AntArr[NomAnt].way.clear()
        NomAnt=NomAnt+1
    AntArr.clear()

def CreateAntArray(n):
    i=1
    while i<n:
        ant=Ant()
        AntArr.append(ant)  
        i=i+1
       
def EndIteration():
    end=1
    return end

def createElitAgent():
    global ElitAntArr
    i=0
    while i<KolElitAgent:
        ant=Ant()
        ant.pheromon=0
        ElitAntArr.append(ant)
        i=i+1

def addElitAgent(ant):
    global ElitAntArr
    newAnt=Ant()
    newAnt.pheromon=ant.pheromon
    newAnt.way = ant.way[:]
    ElitAntArr.append(newAnt)
    ElitAntArr.sort(key=lambda x: x.pheromon, reverse=True)
#    nom=0
#    while nom<len(ElitAntArr):
#        print(nom,ElitAntArr[nom].pheromon,ElitAntArr[nom].way)
#        nom=nom+1
#    print()
    
    if len(ElitAntArr) > KolElitAgent:
        ElitAntArr = ElitAntArr[:KolElitAgent]


    
