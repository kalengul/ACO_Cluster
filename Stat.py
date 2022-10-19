# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 19:14:48 2022

@author: Юрий
"""



import win32com.client #Для загрузки из Excel

MOFI =[]
DOFI =[]
MOFS =[]
DOFS =[]
ProcIS =[]
EndIS =[]
MEndIs =[]
OFProc = []
KolEndIs =[]
NomElGraphTree =[]
ArrTime = []
DArrTime=[]

lenProcIS = 24
KolTimeDelEl = 10

MSolution =0
DSolution = 0
MIter = 0
DIter = 0

MIterAllAntZero = 0
DIterAllAntZero = 0
MSltnAllAntZero = 0
DSltnAllAntZero = 0
EndAllAntZero = 0
KolAllAntZero = 0
KolAntZero = 0
ProcAntZero =0
SumProcAntZero = 0
MTime = 0
DTime = 0

MIterationAntZero = 0
DIterationAntZero = 0

BestOF=0
LowOF = 0


def SaveStatisticsExcel(NameFile,time,koliter,OptimPath,P):
    Excel = win32com.client.Dispatch("Excel.Application")
    wb = Excel.Workbooks.Open(NameFile)
    sheet = wb.ActiveSheet
    NomR=sheet.Cells(1,1).value
    sheet.Cells(NomR,1).value = P
    sheet.Cells(NomR,2).value = MSolution/koliter
    sheet.Cells(NomR,3).value = DSolution/koliter
    sheet.Cells(NomR,11).value = MIter/koliter
    sheet.Cells(NomR,12).value = DIter/koliter
    sheet.Cells(NomR,14).value = MIterationAntZero/koliter
    sheet.Cells(NomR,15).value = DIterationAntZero/koliter
    sheet.Cells(NomR,16).value = MIterAllAntZero/koliter
    sheet.Cells(NomR,17).value = DIterAllAntZero/koliter
    sheet.Cells(NomR,24).value = KolAllAntZero/koliter
    sheet.Cells(NomR,25).value = KolAntZero/koliter
    sheet.Cells(NomR,26).value = MSltnAllAntZero/koliter
    sheet.Cells(NomR,27).value = DSltnAllAntZero/koliter
    sheet.Cells(NomR,32).value = SumProcAntZero/koliter
    sheet.Cells(NomR,33).value = str(time)

    i=0
    while i<lenProcIS:
       if KolEndIs[i]!=0:  
           sheet.Cells(NomR,34+i*2).value = MOFI[i]/KolEndIs[i]
           sheet.Cells(NomR,34+i*2+1).value = DOFI[i]/KolEndIs[i]
           sheet.Cells(NomR,34+i*2+2*lenProcIS+4).value = MOFS[i]/KolEndIs[i]
           sheet.Cells(NomR,34+i*2+1+2*lenProcIS+4).value = DOFS[i]/KolEndIs[i]
           sheet.Cells(NomR,34+i+4*lenProcIS+8).value = OFProc[i]/KolEndIs[i]
           sheet.Cells(NomR,34+i+5*lenProcIS+9).value =KolEndIs[i]
           sheet.Cells(NomR,34+i+6*lenProcIS+10).value = MEndIs[i]/KolEndIs[i]
       i=i+1
    i=0
    while i<len(NomElGraphTree): 
        sheet.Cells(NomR,34+i+7*lenProcIS+11).value = NomElGraphTree[i]/koliter
        i=i+1


    sheet.Cells(NomR,34+7*lenProcIS+len(NomElGraphTree)+12).value = OptimPath
    sheet.Cells(NomR,34+7*lenProcIS+len(NomElGraphTree)+13).value = MTime/koliter
    sheet.Cells(NomR,34+7*lenProcIS+len(NomElGraphTree)+14).value = DTime/koliter

    i=0
    while i<len(ArrTime): 
        sheet.Cells(NomR,34+i*2+7*lenProcIS+len(NomElGraphTree)+16).value =ArrTime[i]/koliter
        sheet.Cells(NomR,34+i*2+1+7*lenProcIS+len(NomElGraphTree)+16).value =DArrTime[i]/koliter
        i=i+1
    
    sheet.Cells(1,1).value=NomR+1
    #сохраняем рабочую книгу
    wb.Save()
    #закрываем ее
    wb.Close()
    #закрываем COM объект
    Excel.Quit()

def SaveProcBestOF (OF,Proc):
    if (BestOF-LowOF)*Proc+LowOF<=OF:
       return 1
    else:
       return 0

def SaveTime(Nom,timeDuration):
   Nom=int(Nom)-1
   ArrTime[Nom]= ArrTime[Nom]+timeDuration 
   DArrTime[Nom]= DArrTime[Nom]+timeDuration*timeDuration 
   return 0 

def SaveTimeIteration(time1):
    global MTime
    global DTime
    MTime=MTime+time1
    DTime=DTime+time1*time1
    #print(MTime)


def StatIterationAntZero(NomIteration):
   global MIterationAntZero
   global DIterationAntZero
   MIterationAntZero=MIterationAntZero+NomIteration 
   DIterationAntZero=DIterationAntZero+NomIteration*NomIteration
   
def StatIterationAntZeroGraphTree(KolGraphTree):
   i=0
   while i<len(NomElGraphTree): 
     NomElGraphTree[i]=NomElGraphTree[i]+KolGraphTree[i] 
     i=i+1
  # print(NomElGraphTree,KolGraphTree)
 #  print(MIterationAntZero)


def StatAllAntZero(NomIteration,NomSolution):
    global MIterAllAntZero
    global DIterAllAntZero
    global MSltnAllAntZero
    global DSltnAllAntZero
    global EndAllAntZero
    if EndAllAntZero==0:
        MIterAllAntZero=MIterAllAntZero+NomIteration
        DIterAllAntZero=DIterAllAntZero+NomIteration*NomIteration
        MSltnAllAntZero=MSltnAllAntZero+NomSolution
        DSltnAllAntZero=DSltnAllAntZero+NomSolution*NomSolution
        EndAllAntZero= 1

def EndStatistik(NomIteration,NomSolution):
    global MSolution
    global DSolution
    global MIter
    global DIter
    global KolAllAntZero
    global KolAntZero
    global ProcAntZero
    global SumProcAntZero
    MSolution=MSolution+NomSolution
    DSolution=DSolution+NomSolution*NomSolution
    MIter=MIter+NomIteration
    DIter=DIter+NomIteration*NomIteration
#    KolAllAntZero=KolAllAntZero/NomIteration
    SumProcAntZero=SumProcAntZero+ProcAntZero/NomIteration
    i=0
    while i<lenProcIS:
        MEndIs[i]=MEndIs[i]+EndIS[i]
        i=i+1
    
def ProcBestOF(OF,NomIteration,NomSolution):
    i=0
    while i<lenProcIS:
        if (BestOF-LowOF)*ProcIS[i]+LowOF<=OF and EndIS[i]==0:
            MOFI[i]=MOFI[i]+NomIteration
            DOFI[i]=DOFI[i]+NomIteration*NomIteration
            MOFS[i]=MOFS[i]+NomSolution
            DOFS[i]=DOFS[i]+NomSolution*NomSolution
            OFProc[i]=OFProc[i]+OF
            KolEndIs[i]=KolEndIs[i]+1
        if (BestOF-LowOF)*ProcIS[i]+LowOF<=OF:
            EndIS[i]=EndIS[i]+1 
        i=i+1
    
def SbrosStatistic():
   global EndAllAntZero
   EndIS.clear()
   EndAllAntZero = 0
   i=0
   while i<lenProcIS:
       EndIS.append(0)
       i=i+1

def StartStatisticGrahTree(KolEl):
    NomElGraphTree.clear()
    i=0
    while i<KolEl:
        NomElGraphTree.append(0)
        i=i+1

def StartStatistic():
   global  EndAllAntZero
   global  EndAllAntZero
   global MSolution
   global DSolution
   global MIter
   global DIter
   global MIterAllAntZero
   global DIterAllAntZero
   global MSltnAllAntZero
   global DSltnAllAntZero
   global KolAllAntZero
   global KolAntZero
   global ProcAntZero
   global SumProcAntZero
   global MIterationAntZero
   global DIterationAntZero
   global MTime
   global DTime
   ProcIS.clear()
   ProcIS.append(0.5)
   ProcIS.append(0.75)
   ProcIS.append(0.80)
   ProcIS.append(0.81)
   ProcIS.append(0.82)
   ProcIS.append(0.83)
   ProcIS.append(0.84)
   ProcIS.append(0.85)
   ProcIS.append(0.86)
   ProcIS.append(0.87)
   ProcIS.append(0.88)
   ProcIS.append(0.89)
   ProcIS.append(0.90)
   ProcIS.append(0.91)
   ProcIS.append(0.92)
   ProcIS.append(0.93)
   ProcIS.append(0.94)
   ProcIS.append(0.95)
   ProcIS.append(0.96)
   ProcIS.append(0.97)
   ProcIS.append(0.98)
   ProcIS.append(0.99)
   ProcIS.append(0.9999)
   ProcIS.append(1)
   
   MSolution=0
   DSolution=0
   MIter=0
   DIter=0
   MIterAllAntZero=0
   DIterAllAntZero=0
   MSltnAllAntZero=0
   DSltnAllAntZero=0
   KolAllAntZero = 0
   KolAntZero = 0
   ProcAntZero=0
   SumProcAntZero = 0
   MIterationAntZero = 0
   DIterationAntZero = 0
   MTime = 0
   DTime = 0
   EndIS.clear()
   MOFI.clear()
   DOFI.clear()
   MOFS.clear()
   DOFS.clear()
   OFProc.clear()
   KolEndIs.clear()
   ArrTime.clear()
   EndAllAntZero = 0
   i=0
   while i<lenProcIS:
       EndIS.append(0)
       MOFI.append(0)
       DOFI.append(0)
       MOFS.append(0)
       DOFS.append(0)
       OFProc.append(0)
       KolEndIs.append(0)
       MEndIs.append(0)
       i=i+1
   i=0
   while i<KolTimeDelEl:
       ArrTime.append(0.0)
       DArrTime.append(0.0)
       i=i+1
        
        
def SaveParametr(version,NameFile,N,Ro,Q,alf1,alf2,koef1,koef2,typeProbability,NameFileXL,AddFeromonAntZero,SbrosGraphAllAntZero,goNewIterationAntZero,goGraphTree,SortPheromon,KolIteration,KolStatIteration,MaxkolIterationAntZero):
    Excel = win32com.client.Dispatch("Excel.Application")
    wb = Excel.Workbooks.Open(NameFile)
    sheet = wb.ActiveSheet 
    NomR=sheet.Cells(1,1).value
    
    a='Version - '+version
    sheet.Cells(NomR,5).value = a
    a='NameFilePar= '+NameFileXL
    sheet.Cells(NomR,6).value = a
    a='N='+str(N)
    sheet.Cells(NomR,7).value = a
    a='Ro='+str(Ro)
    sheet.Cells(NomR,8).value = a
    a='Q='+str(Q)
    sheet.Cells(NomR,9).value = a
    a='alf1='+str(alf1)
    sheet.Cells(NomR,10).value = a
    a='alf2='+str(alf2)
    sheet.Cells(NomR,11).value = a
    a='koef1='+str(koef1)
    sheet.Cells(NomR,12).value = a
    a='koef2='+str(koef2)
    sheet.Cells(NomR,13).value = a
    a='typeProbability='+str(typeProbability)
    sheet.Cells(NomR,14).value = a
    a='AddFeromonAntZero='+str(AddFeromonAntZero)
    sheet.Cells(NomR,15).value = a
    a='SbrosGraphAllAntZero='+str(SbrosGraphAllAntZero)
    sheet.Cells(NomR,16).value = a
    a='goNewIterationAntZero='+str(goNewIterationAntZero)
    sheet.Cells(NomR,17).value = a
    a='goGraphTree='+str(goGraphTree)
    sheet.Cells(NomR,18).value = a
    a='SortPheromon='+str(SortPheromon)
    sheet.Cells(NomR,19).value = a
    a='KolIteration='+str(KolIteration)
    sheet.Cells(NomR,20).value = a
    a='KolStatIteration='+str(KolStatIteration)
    sheet.Cells(NomR,21).value = a
    a='MaxkolIterationAntZero='+str(MaxkolIterationAntZero)
    sheet.Cells(NomR,22).value = a
    
    sheet.Cells(1,1).value=NomR+1
    #сохраняем рабочую книгу
    wb.Save()
    #закрываем ее
    wb.Close()
    #закрываем COM объект
    Excel.Quit()        