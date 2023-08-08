# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 22:32:02 2022

@author: Юрий
"""

from datetime import datetime

StartTime = datetime.now()
TimeIteration = datetime.now()
PrintTimeEl = datetime.now()
SocketTime = datetime.now()
ClusterTime = datetime.now()

def now():
    return datetime.now()

def setStartTime():
    global StartTime
    StartTime = datetime.now()
    
def setTimeIteration():
    global TimeIteration
    TimeIteration = datetime.now()
    
def setSocketTime():
    global SocketTime
    SocketTime = datetime.now()
    
def setClusterTime():
    global ClusterTime
    ClusterTime = datetime.now()    
    
def DeltTimeIteration():
    global TimeIteration
    return datetime.now()-TimeIteration

def DeltStartTime():
    global StartTime
    return datetime.now()-StartTime

def DeltSocketTime():
    global SocketTime
    return datetime.now()-SocketTime

def DeltClusterTime():
    global ClusterTime
    return datetime.now()-ClusterTime

def setPrintTime():
    global PrintTimeEl
    PrintTimeEl = datetime.now()    
    
def PrintTime(Name):
    global PrintTimeEl
    if (datetime.now()-PrintTimeEl).total_seconds() !=0:
        print(Name,(datetime.now()-PrintTimeEl).total_seconds())
    PrintTimeEl = datetime.now()     