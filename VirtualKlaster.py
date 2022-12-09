# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:22:49 2022

@author: Юрий
"""

import math
import SIRVD
import os
import win32com.client #Для загрузки из Excel

VivodKlasterExcel = 0

def SavePathExcel(NameFile,path,OF,TypeKlaster):
    Excel = win32com.client.Dispatch("Excel.Application")
    wb = Excel.Workbooks.Open(NameFile)
    sheet = wb.ActiveSheet
    NomR=sheet.Cells(1,1).value
    sheet.Cells(1,2).value=TypeKlaster
    i=1;
    while i<len(path):
      sheet.Cells(NomR,i).value = path[i-1]
      i=i+1
    sheet.Cells(NomR,i).value = OF  
    wb.Save()
    #закрываем ее
    wb.Close()
    #закрываем COM объект
    Excel.Quit()

def Klaster1(path):
    OF = 0
    if path[0]>3: 
        OF=OF+10
    if path[2]==0: 
        OF=OF*5
    if path[4]==0:
        OF=OF+3  
    return OF

def Klaster2(path):
    OF = 0
    OF=OF+path[0]-path[1]+2*path[2]+path[3]+2*path[4]
    OF=OF+0.5*path[5]-0.12*path[6]-path[7]+80*path[8]+0.00001*path[9]
    if path[10]=='Сильное':
        OF=OF+20
    return OF

def Klaster2o(path):
    OF = 0
    OF=OF+path[4]-path[12]+2*path[2]+path[3]+2*path[5]
    OF=OF+0.5*path[7]-0.12*path[10]-path[11]+80*path[0]+0.00001*path[6]
    if path[1]=='Сильное':
        OF=OF+20
    return OF

def Klaster2no(path):
    OF = 0
    OF=OF+path[8]-path[0]+2*path[10]+path[9]+2*path[7]
    OF=OF+0.5*path[5]-0.12*path[2]-path[1]+80*path[12]+0.00001*path[6]
    if path[11]=='Сильное':
        OF=OF+20
    return OF

def Klaster2so(path):
    OF = 0
    OF=OF+path[5]-path[4]+2*path[7]+path[12]+2*path[3]
    OF=OF+0.5*path[9]-0.12*path[6]-path[8]+80*path[10]+0.00001*path[11]
    if path[1]=='Сильное':
        OF=OF+20
    return OF

def Klaster2nso(path):
    OF = 0
    OF=OF+path[12-5]-path[12-4]+2*path[12-7]+path[12-12]+2*path[12-3]
    OF=OF+0.5*path[12-9]-0.12*path[12-6]-path[12-8]+80*path[12-10]+0.00001*path[12-11]
    if path[12-1]=='Сильное':
        OF=OF+20
    return OF

def Klaster3(path):
    OF = 0
    OF=OF+(path[0]-4)*(path[0]-4)+math.cos(path[1])+math.cos(math.exp(path[2]))+(path[3]-10)*(path[3]-10)+2*path[4]
    OF=OF+0.5*path[5]-0.12*path[6]-path[7]+80*path[8]+0.00001*path[9]
    OF=OF*15
    if path[10]=='Сильное':
        OF=OF+20
    return OF

def Bench4(path):
    a1=path[0]**2
    a2=path[1]**2
    a=1-(a1+a2)**0.5/math.pi
    OF=(math.cos(path[0])*math.cos(path[1])*math.exp((math.fabs(a))))**2
    return OF

def Bench4x(path):
    p0=path[0]+path[1]+path[2]+path[3]
    p1=path[4]+path[5]+path[6]+path[7]
    a1=p0**2
    a2=p1**2
    a=1-(a1+a2)**0.5/math.pi
    OF=(math.cos(p0)*math.cos(p1)*math.exp((math.fabs(a))))**2
    return OF

def Bench4x1(path):
    p0=path[0]+path[1]
    p1=path[2]+path[3]
    a1=p0**2
    a2=p1**2
    a=1-(a1+a2)**0.5/math.pi
    OF=(math.cos(p0)*math.cos(p1)*math.exp((math.fabs(a))))**2
    return OF

def Bench4x2(path):
    p0=path[0]*(path[1]+path[2])
    p1=path[3]*(path[4]+path[5])
    a1=p0**2
    a2=p1**2
    a=1-(a1+a2)**0.5/math.pi
    OF=(math.cos(p0)*math.cos(p1)*math.exp((math.fabs(a))))**2
    return OF

def Bench4x22(path):
    p0=path[0]*(path[1]+path[2]+path[3])
    p1=path[4]*(path[5]+path[6]+path[7])
    a1=p0**2
    a2=p1**2
    a=1-(a1+a2)**0.5/math.pi
    OF=(math.cos(p0)*math.cos(p1)*math.exp((math.fabs(a))))**2
    return OF

def Bench4x222(path):
    p0=path[0]*(path[1]+path[2]+path[3]+path[4])
    p1=path[5]*(path[6]+path[7]+path[8]+path[9])
    a1=p0**2
    a2=p1**2
    a=1-(a1+a2)**0.5/math.pi
    OF=(math.cos(p0)*math.cos(p1)*math.exp((math.fabs(a))))**2
    return OF

def Bench4x2222(path):
    p0=path[0]*(path[1]+path[2]+path[3]+path[4]+path[5])
    p1=path[6]*(path[7]+path[8]+path[9]+path[10]+path[11])
    a1=p0**2
    a2=p1**2
    a=1-(a1+a2)**0.5/math.pi
    OF=(math.cos(p0)*math.cos(p1)*math.exp((math.fabs(a))))**2
    return OF

def Bench4xo2222(path):
    p0=path[10]*(path[8]+path[6]+path[4]+path[2]+path[0])
    p1=path[11]*(path[9]+path[7]+path[5]+path[3]+path[1])
    a1=p0**2
    a2=p1**2
    a=1-(a1+a2)**0.5/math.pi
    OF=(math.cos(p0)*math.cos(p1)*math.exp((math.fabs(a))))**2
    return OF

def Bench1(path):
    a1=path[0]**2
    a2=path[1]**2
    a=(a1+a2)/200
    OF=4*math.fabs(math.sin(path[0])*math.cos(path[1])*math.exp(math.fabs(math.cos(a))))
    return OF

def Bench10(path):
    a1=math.sin(path[0])*math.exp((1-math.cos(path[1]))**2)
    a2=math.cos(path[1])*math.exp((1-math.sin(path[0]))**2)
    a=a1+a2
    OF=a+(path[0]-path[1])**2
    return OF

def SIRVD1(path):
    SIRVD.Susceptible = 107137780
    SIRVD.Infected = 3609122
    SIRVD.Recovered = 9192702
    SIRVD.Vaccinated = 25132827
    SIRVD.Dead = 30313
    SIRVD.beta = path[0]
    SIRVD.gamma = path[1]
    SIRVD.alpha = path[2]
    SIRVD.sigma = path[3]
    SIRVD.delta = path[4]
    i=0
    OF=0
    while i<=5:
        SIRVD.start_next()
        OF=OF+SIRVD.go_OF_Excel_File(os.getcwd()+'/'+'SIRVD.xlsx',i)
        i=i+1
    OF=((10000000000-OF)/1000000000-9.9)*10
    #print(OF)
    return OF

def SIRVD2(path):
    SIRVD.Susceptible = path[0]
    SIRVD.Infected = path[1]
    SIRVD.Recovered = path[2]
    SIRVD.Vaccinated = path[3]
    SIRVD.Dead = path[4]
    SIRVD.beta = path[5]
    SIRVD.gamma = path[6]
    SIRVD.alpha = path[7]
    SIRVD.sigma = path[8]
    SIRVD.delta = path[9]
    i=0
    OF=0
    while i<=5:
        SIRVD.start_next()
        OF=OF+SIRVD.go_OF_Excel_File(os.getcwd()+'/'+'SIRVD.xlsx',i)
        i=i+1
    OF=((10000000000-OF)/1000000000-9.9)*10
    return OF

def GetObjectivFunction(path,TypeKlaster):
    OF=0
    if TypeKlaster==1:
       OF=Klaster1(path)
    elif TypeKlaster==2:
       OF=Klaster2(path) 
    elif TypeKlaster==2001:
       OF=Klaster2o(path)
    elif TypeKlaster==2002:
       OF=Klaster2no(path)
    elif TypeKlaster==2003:
       OF=Klaster2so(path)
    elif TypeKlaster==2004:
       OF=Klaster2nso(path)
    elif TypeKlaster==3:
       OF=Klaster3(path) 
    elif TypeKlaster==401:
       OF=Bench1(path) 
    elif TypeKlaster==404:
       OF=Bench4(path) 
    elif TypeKlaster==4040:
       OF=Bench4x(path) 
    elif TypeKlaster==4041:
       OF=Bench4x1(path) 
    elif TypeKlaster==4042:
       OF=Bench4x2(path) 
    elif TypeKlaster==4043:
       OF=Bench4x22(path) 
    elif TypeKlaster==4044:
       OF=Bench4x222(path)
    elif TypeKlaster==4045:
       OF=Bench4x2222(path)
    elif TypeKlaster==40451:
       OF=Bench4xo2222(path)
    elif TypeKlaster==410:
       OF=Bench10(path) 
    elif TypeKlaster==990:
       OF=SIRVD1(path) 
    elif TypeKlaster==991:
       OF=SIRVD2(path) 
#    print(OF, path,TypeKlaster)
    if VivodKlasterExcel==1:
      SavePathExcel('Cluster.xlsx',path,OF,TypeKlaster)  
    return OF
