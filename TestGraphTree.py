# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 22:37:23 2022

@author: Юрий
"""
import os
import LoadSettingsIniFile as Setting
import ParametricGraph as pg
import GraphTree as gt
import Hash

print(' Start Program ')    
if os.path.exists('setting.ini'):
    Setting.readSetting('setting.ini')
print('Go Parametric Graph')
# Создание параметрического графа
NameFile=os.getcwd()+'/ParametricGraph/'+Setting.NameFileGraph
print(NameFile)
pg.ReadParametrGraphExcelFile(NameFile)
wayGT = gt.GraphWay()
StartWay=[]
i=0
while i<len(pg.ParametricGraph):
    StartWay.append(0)
    i=i+1
gt.StartWayGraphTree=StartWay
for way in wayGT:
    print(way)
    PathWay=Hash.goPathStr(way)
    Hash.addPath(PathWay,10)