# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 21:47:29 2023

@author: Юрий
"""

import MMK
import configparser
import os
import GoTime

def SaveSetting(NameFile,typeconfig,subtypeconfig,parametr):
    config = configparser.ConfigParser()
    config.read(NameFile)  # читаем конфиг
    config[typeconfig][subtypeconfig] = parametr
    with open(NameFile, 'w') as configfile:
        config.write(configfile)
    
    
def SaveParametr(folder,NomProc,typeconfig,subtypeconfig,parametr):
    if os.path.exists(folder+'/setting.ini'):
        print(GoTime.now(),NomProc,' Save  '+folder+'/setting.ini','[',typeconfig,'][',subtypeconfig,']=',parametr)  
        SaveSetting(folder+'/setting.ini',typeconfig,subtypeconfig,parametr)

def run_script(NomProc,folder,folderPg,lock_excel):
    ArrayParametr=[]
    ArrayParametr.append('0.5')
    ArrayParametr.append('1')
    ArrayParametr.append('2')
    ArrayParametr.append('10')
    ArrayParametr2=[]
    ArrayParametr2.append('0.5')
    ArrayParametr2.append('1')
    ArrayParametr2.append('2')
    ArrayParametr2.append('10')
    typeconfig='ParametricGraph'
    subtypeconfig='koef1'
    typeconfig2='ParametricGraph'
    subtypeconfig2='koef2'
    j=0
    while j<len(ArrayParametr2): 
        SaveParametr(folder,NomProc,typeconfig2,subtypeconfig2,ArrayParametr2[j])
        TextPrint2='koef2='+ArrayParametr2[j]
        i=0
        while i<len(ArrayParametr):
            SaveParametr(folder,NomProc,typeconfig,subtypeconfig,ArrayParametr[i])
            TextPrint=TextPrint2+' koef1='+ArrayParametr[i]
            MMK.run_script(TextPrint,NomProc,folder,folderPg,lock_excel)
            i=i+1
        j=j+1