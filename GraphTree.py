# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 22:22:17 2022

@author: Юрий
"""

import ParametricGraph as pg
import Hash

ArrNomWay = []
KolIterWay =0
NomElKolIterWay = []
NomArrEl = []
SortPheromon = 0
HorizontalTree = 0
StartWayGraphTree = []

class GraphWay:
    def __init__(self):
        # Здесь хранится промежуточное значение
        pass
        
    def __iter__(self):
        return self

    def __next__(self):
        # Здесь мы обновляем значение и возвращаем результат
        if HorizontalTree==1:
            way=GoPathGraphTreeHorizontal(StartWayGraphTree)
        else:
            way=GoPathGraphTreeNode(StartWayGraphTree)
        if way!=[]:
            return way
        else:
            raise StopIteration

def NextWay(way,nomWay):
  global KolIterWay
  KolIterWay=KolIterWay+1
  NomElKolIterWay[nomWay]=NomElKolIterWay[nomWay]+1
  NomArrEl[nomWay]=NomArrEl[nomWay]+1
  if NomArrEl[nomWay]>=len(pg.ParametricGraph[nomWay].node):  
      NomArrEl[nomWay]=0
  way[nomWay]=ArrNomWay[NomArrEl[nomWay]]
  
def NextHorizontalWay(way,nomWay):
    
   NomElKolIterWay[nomWay]=NomElKolIterWay[nomWay]+1 


def CreateArrayNomWay(way,nomWay):
    ArrNomWay.clear()
    ArrEl=way[nomWay]
    KolEl=0
    while KolEl<len(pg.ParametricGraph[nomWay].node):
       ArrNomWay.append(ArrEl)  
       ArrEl=ArrEl+1  
       KolEl=KolEl+1
       if ArrEl>=len(pg.ParametricGraph[nomWay].node):  
            ArrEl=0
    if SortPheromon==1:
        SortArrayNomWay(nomWay)

            
def SortArrayNomWay(nomWay):
    KolEl=1
    while KolEl<len(pg.ParametricGraph[nomWay].node):
       MinEl=KolEl
       NomMin=MinEl
       while MinEl<len(pg.ParametricGraph[nomWay].node):
           if (pg.ParametricGraph[nomWay].node[ArrNomWay[NomMin]].pheromon<=pg.ParametricGraph[nomWay].node[ArrNomWay[MinEl]].pheromon) or ((pg.ParametricGraph[nomWay].node[ArrNomWay[NomMin]].pheromon==pg.ParametricGraph[nomWay].node[ArrNomWay[MinEl]].pheromon) and (NomMin<MinEl)):
             NomMin=MinEl
           MinEl=MinEl+1 
       p=ArrNomWay[KolEl]
       ArrNomWay[KolEl]=ArrNomWay[NomMin]
       ArrNomWay[NomMin]=p
       KolEl=KolEl+1 

def GoPathGraphTree(StartWay):
    if HorizontalTree==1:
        return GoPathGraphTreeHorizontal(StartWay)
    else:
        return GoPathGraphTreeNode(StartWay)
    
def GoPathGraphTreeNode(StartWay):
    global KolIterWay
    NomArrEl.clear()
    NomElKolIterWay.clear()
    way=[]
    i=0
    KolIterWay=0
    while i<len(StartWay):
        way.append(StartWay[i])
        NomArrEl.append(0)
        NomElKolIterWay.append(0)
        i=i+1
    PathWay=Hash.goPathStr(way)
    HashWay = Hash.getPath(PathWay)
    nomWay=0
    CreateArr=1
    while nomWay<len(StartWay) and HashWay!=0:
        if CreateArr==1:
            CreateArrayNomWay(StartWay,nomWay)
            CreateArr=0
        NextWay(way,nomWay)
        if nomWay<len(StartWay) and way[nomWay]==StartWay[nomWay]:
            while nomWay<len(StartWay) and way[nomWay]==StartWay[nomWay] :
              nomWay=nomWay+1
              if nomWay<len(StartWay):
                  CreateArrayNomWay(StartWay,nomWay)
                  NextWay(way,nomWay)
            if nomWay<len(StartWay):
                CreateArr=1
                nomWay=0
        PathWay=Hash.goPathStr(way)
        HashWay = Hash.getPath(PathWay)
    if nomWay>=len(StartWay):
        way.clear()
    return way

def GoPathGraphTreeHorizontal(StartWay):
    global KolIterWay
    NomArrEl.clear()
    NomElKolIterWay.clear()
    way=[]
    i=0
    KolIterWay=0
    while i<len(StartWay):
        way.append(StartWay[i])
        NomArrEl.append(0)
        NomElKolIterWay.append(0)
        i=i+1
    PathWay=Hash.goPathStr(way)
    HashWay = Hash.getPath(PathWay)
    nomWay=0
    CreateArr=1
    while nomWay<len(StartWay) and HashWay!=0:
        
        PathWay=Hash.goPathStr(way)
        HashWay = Hash.getPath(PathWay)
    if nomWay>=len(StartWay):
        way.clear()
    return way

    