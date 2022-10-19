# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 09:28:44 2022

@author: Юрий
"""

import random

AntArr =[]
N = 5  #20
Q = 2  #2
Ro = 0.9  #0.9
alf1 = 1  #1
alf2 = 1  #1
koef1 = 1 #1
koef2 = 1 #1
typeProbability = 1


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

       
def GoAntNextNode(ant,ArrayNode):
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
    ant.way.append(i)
    return ArrayNode[i]
       
    
