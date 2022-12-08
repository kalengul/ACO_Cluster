# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 09:28:44 2022

@author: Юрий
"""

AntArr =[]
N = 5  #20
Q = 2  #2
Ro = 0.9  #0.9

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


       
    
