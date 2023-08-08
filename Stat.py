# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 19:14:48 2022

@author: Юрий
"""



import win32com.client #Для загрузки из Excel
import json
import os


class JSONDataAdapter:
    @staticmethod
    def to_json(o):
        if isinstance(o, stat):
              result = o.__dict__
              result["className"] = o.__class__.__name__
              return result
 
class JSONFile:
    folderJSON=''
    NameFile='currentiter.json'
    def SaveIterJSONFile(Stat,NomStatIteration,Par):
        Stat_json_string=JSONDataAdapter.to_json(Stat)
        json_string=json.dumps([NomStatIteration,Par,Stat_json_string])
        #print(json_string)
        with open(JSONFile.folderJSON+'/'+JSONFile.NameFile, 'w') as f:
            f.write(json_string)
    
    def LoadIterJSONFileIfExist(Stat,Par):
       if os.path.exists(JSONFile.folderJSON+'/'+JSONFile.NameFile): 
           with open(JSONFile.folderJSON+'/'+JSONFile.NameFile, 'r') as f: 
               json_string=json.loads(f.read())
               NomStatIteration=json_string[0]
               Par=json_string[1]
               for NameAtr in json_string[2]:
                   Stat.__dict__[NameAtr]=json_string[2][NameAtr]
               return NomStatIteration,Par
       else:
           return 0,Par
       
    def RemoveJSONFile():
        os.remove(JSONFile.folderJSON+'/'+JSONFile.NameFile)
             

class stat:

    
    def __init__(self):
        self.MOFI =[]
        self.DOFI =[]
        self.MOFS =[]
        self.DOFS =[]
        self.ProcIS =[]
        self.EndIS =[]
        self.MEndIs =[]
        self.OFProc = []
        self.KolEndIs =[]
        self.NomElGraphTree =[]
        self.ArrTime = []
        self.DArrTime=[]

        self.lenProcIS = 24
        self.KolTimeDelEl = 10

        self.MSolution =0
        self.DSolution = 0
        self.MIter = 0
        self.DIter = 0

        self.MIterAllAntZero = 0
        self.DIterAllAntZero = 0
        self.MSltnAllAntZero = 0
        self.DSltnAllAntZero = 0
        self.EndAllAntZero = 0
        self.KolAllAntZero = 0
        self.KolAntZero = 0
        self.ProcAntZero =0
        self.SumProcAntZero = 0
        self.MTime = 0
        self.DTime = 0
        self.MSocketTime = 0
        self.DSocketTime = 0
        self.MClusterTime = 0
        self.DClusterTime = 0

        self.MIterationAntZero = 0
        self.DIterationAntZero = 0

        self.BestOF=0
        self.LowOF = 0  
        self.StartStatistic()  
    
    def SaveStatisticsExcel(self,NameFile,time,koliter,OptimPath,P):
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(NameFile)
        sheet = wb.ActiveSheet
        NomR=sheet.Cells(1,1).value
        sheet.Cells(NomR,1).value = P
        sheet.Cells(NomR,2).value = self.MSolution/koliter
        sheet.Cells(NomR,3).value =self. DSolution/koliter
        sheet.Cells(NomR,11).value = self.MIter/koliter
        sheet.Cells(NomR,12).value = self.DIter/koliter
        sheet.Cells(NomR,13).value = self.MIterAllAntZero/koliter
        sheet.Cells(NomR,14).value = self.DIterAllAntZero/koliter
        sheet.Cells(NomR,18).value = self.KolAllAntZero/koliter
        sheet.Cells(NomR,19).value = self.KolAntZero/koliter
        sheet.Cells(NomR,20).value = self.SumProcAntZero/koliter
        sheet.Cells(NomR,21).value = str(time)
        sheet.Cells(NomR,23).value = self.MIterationAntZero/koliter
        sheet.Cells(NomR,24).value = self.DIterationAntZero/koliter
        sheet.Cells(NomR,28).value = self.MSltnAllAntZero/koliter
        sheet.Cells(NomR,29).value = self.DSltnAllAntZero/koliter
    
        i=0
        while i<self.lenProcIS:
           if self.KolEndIs[i]!=0:  
               sheet.Cells(NomR,34+i*2).value = self.MOFI[i]/self.KolEndIs[i]
               sheet.Cells(NomR,34+i*2+1).value = self.DOFI[i]/self.KolEndIs[i]
               sheet.Cells(NomR,34+i*2+2*self.lenProcIS+4).value = self.MOFS[i]/self.KolEndIs[i]
               sheet.Cells(NomR,34+i*2+1+2*self.lenProcIS+4).value = self.DOFS[i]/self.KolEndIs[i]
               sheet.Cells(NomR,34+i+4*self.lenProcIS+8).value = self.OFProc[i]/self.KolEndIs[i]
               sheet.Cells(NomR,34+i+5*self.lenProcIS+9).value =self.KolEndIs[i]
               sheet.Cells(NomR,34+i+6*self.lenProcIS+10).value = self.MEndIs[i]/self.KolEndIs[i]
           i=i+1
        i=0
        while i<len(self.NomElGraphTree): 
            sheet.Cells(NomR,34+i+7*self.lenProcIS+11).value =self.NomElGraphTree[i]/koliter
            i=i+1
    
    
        sheet.Cells(NomR,34+7*self.lenProcIS+len(self.NomElGraphTree)+12).value = OptimPath
        sheet.Cells(NomR,34+7*self.lenProcIS+len(self.NomElGraphTree)+13).value = self.MTime/koliter
        sheet.Cells(NomR,34+7*self.lenProcIS+len(self.NomElGraphTree)+14).value = self.DTime/koliter
    
        i=0
        while i<len(self.ArrTime): 
            sheet.Cells(NomR,34+i*2+7*self.lenProcIS+len(self.NomElGraphTree)+16).value =self.ArrTime[i]/koliter
            sheet.Cells(NomR,34+i*2+1+7*self.lenProcIS+len(self.NomElGraphTree)+16).value =self.DArrTime[i]/koliter
            i=i+1
        
        sheet.Cells(1,1).value=NomR+1
        #сохраняем рабочую книгу
        wb.Save()
        #закрываем ее
        wb.Close()
        #закрываем COM объект
        Excel.Quit()
        
    
    def SaveProcBestOF (self,OF,Proc):
        if (self.BestOF-self.LowOF)*Proc+self.LowOF<=OF:
           return 1
        else:
           return 0
    
    def SaveTime(self,Nom,timeDuration):
       Nom=int(Nom)-1
       self.ArrTime[Nom]= self.ArrTime[Nom]+timeDuration 
       self.DArrTime[Nom]= self.DArrTime[Nom]+timeDuration*timeDuration 
       return 0 
    
    def SaveTimeIteration(self,time1):
        self.MTime=self.MTime+time1
        self.DTime=self.DTime+time1*time1
        
    def SaveTimeSocket(self,time1):
        self.MSocketTime=self.MSocketTime+time1
        self.DSocketTime=self.DSocketTime+time1*time1
        print(self.MSocketTime)
        print('Cluster',self.MClusterTime)

    def SaveTimeCluster(self,time1):
        self.MClusterTime=self.MClusterTime+time1
        self.DClusterTime=self.DClusterTime+time1*time1
    
    
    def StatIterationAntZero(self,NomIteration):
      #NomIteration=NomIteration+1
      self.MIterationAntZero=self.MIterationAntZero+NomIteration 
      self.DIterationAntZero=self.DIterationAntZero+NomIteration*NomIteration
       
    def StatIterationAntZeroGraphTree(self,KolGraphTree):
       i=0
       while i<len(self.NomElGraphTree): 
         self.NomElGraphTree[i]=self.NomElGraphTree[i]+KolGraphTree[i] 
         i=i+1
    
    
    def StatAllAntZero(self,NomIteration,NomSolution):
        if self.EndAllAntZero==0:
            self.MIterAllAntZero=self.MIterAllAntZero+NomIteration
            self.DIterAllAntZero=self.DIterAllAntZero+NomIteration*NomIteration
            self.MSltnAllAntZero=self.MSltnAllAntZero+NomSolution
            self.DSltnAllAntZero=self.DSltnAllAntZero+NomSolution*NomSolution
            self.EndAllAntZero= 1
    
    def EndStatistik(self,NomIteration,NomSolution):
        self.MSolution=self.MSolution+NomSolution
        self.DSolution=self.DSolution+NomSolution*NomSolution
        self.MIter=self.MIter+NomIteration
        self.DIter=self.DIter+NomIteration*NomIteration
    #    KolAllAntZero=KolAllAntZero/NomIteration
        self.SumProcAntZero=self.SumProcAntZero+self.ProcAntZero/NomIteration
        i=0
        while i<self.lenProcIS:
            self.MEndIs[i]=self.MEndIs[i]+self.EndIS[i]
            i=i+1
        
    def ProcBestOF(self,OF,MaxOptimization,NomIteration,NomSolution):
        i=0
        while i<self.lenProcIS:
            if MaxOptimization==1:
                if (self.BestOF-self.LowOF)*self.ProcIS[i]+self.LowOF<=OF and self.EndIS[i]==0:
                    self.MOFI[i]=self.MOFI[i]+NomIteration
                    self.DOFI[i]=self.DOFI[i]+NomIteration*NomIteration
                    self.MOFS[i]=self.MOFS[i]+NomSolution
                    self.DOFS[i]=self.DOFS[i]+NomSolution*NomSolution
                    self.OFProc[i]=self.OFProc[i]+OF
                    self.KolEndIs[i]=self.KolEndIs[i]+1
                if (self.BestOF-self.LowOF)*self.ProcIS[i]+self.LowOF<=OF:
                    self.EndIS[i]=self.EndIS[i]+1 
            else:
                if self.BestOF-(self.BestOF-self.LowOF)*self.ProcIS[i]>=OF and self.EndIS[i]==0:
                    self.MOFI[i]=self.MOFI[i]+NomIteration
                    self.DOFI[i]=self.DOFI[i]+NomIteration*NomIteration
                    self.MOFS[i]=self.MOFS[i]+NomSolution
                    self.DOFS[i]=self.DOFS[i]+NomSolution*NomSolution
                    self.OFProc[i]=self.OFProc[i]+OF
                    self.KolEndIs[i]=self.KolEndIs[i]+1
                if self.BestOF-(self.BestOF-self.LowOF)*self.ProcIS[i]>=OF:
                    self.EndIS[i]=self.EndIS[i]+1 
            i=i+1
        
    def SbrosStatistic(self):
       self.EndIS.clear()
       self.EndAllAntZero = 0
       i=0
       while i<self.lenProcIS:
           self.EndIS.append(0)
           i=i+1
    
    def StartStatisticGrahTree(self,KolEl):
        self.NomElGraphTree.clear()
        i=0
        while i<KolEl:
            self.NomElGraphTree.append(0)
            i=i+1
    
    def StartStatistic(self):
       
       self.MSolution=0
       self.DSolution=0
       self.MIter=0
       self.DIter=0
       self.MIterAllAntZero=0
       self.DIterAllAntZero=0
       self.MSltnAllAntZero=0
       self.DSltnAllAntZero=0
       self.KolAllAntZero = 0
       self.KolAntZero = 0
       self.ProcAntZero=0
       self.SumProcAntZero = 0
       self.MIterationAntZero = 0
       self.DIterationAntZero = 0
       self.MTime = 0
       self.DTime = 0
       self.EndIS.clear()
       self.MOFI.clear()
       self.DOFI.clear()
       self.MOFS.clear()
       self.DOFS.clear()
       self.OFProc.clear()
       self.KolEndIs.clear()
       self.ArrTime.clear()
       self.EndAllAntZero = 0
       i=0
       while i<self.lenProcIS:
           self.EndIS.append(0)
           self.MOFI.append(0)
           self.DOFI.append(0)
           self.MOFS.append(0)
           self.DOFS.append(0)
           self.OFProc.append(0)
           self.KolEndIs.append(0)
           self.MEndIs.append(0)
           i=i+1
       i=0
       while i<self.KolTimeDelEl:
           self.ArrTime.append(0.0)
           self.DArrTime.append(0.0)
           i=i+1
            
            
    def SaveParametr(self,version,NameFile,N,Ro,Q,alf1,alf2,alf3,koef1,koef2,koef3,typeProbability,EndAllSolution,NameFileXL,AddFeromonAntZero,SbrosGraphAllAntZero,goNewIterationAntZero,goGraphTree,SortPheromon,KolIteration,KolStatIteration,MaxkolIterationAntZero,typeParametr,KolElNomElGraphTree,Best,Low):

        self.BestOF=Best
        self.LowOF=Low
        self.ProcIS.clear()
        self.ProcIS.append(0.5)
        self.ProcIS.append(0.75)
        self.ProcIS.append(0.80)
        self.ProcIS.append(0.81)
        self.ProcIS.append(0.82)
        self.ProcIS.append(0.83)
        self.ProcIS.append(0.84)
        self.ProcIS.append(0.85)
        self.ProcIS.append(0.86)
        self.ProcIS.append(0.87)
        self.ProcIS.append(0.88)
        self.ProcIS.append(0.89)
        self.ProcIS.append(0.90)
        self.ProcIS.append(0.91)
        self.ProcIS.append(0.92)
        self.ProcIS.append(0.93)
        self.ProcIS.append(0.94)
        self.ProcIS.append(0.95)
        self.ProcIS.append(0.96)
        self.ProcIS.append(0.97)
        self.ProcIS.append(0.98)
        self.ProcIS.append(0.99)
        self.ProcIS.append(0.9999)
        self.ProcIS.append(1)
        
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
        a='alf3='+str(alf3)
        sheet.Cells(NomR,12).value = a
        a='koef1='+str(koef1)
        sheet.Cells(NomR,13).value = a
        a='koef2='+str(koef2)
        sheet.Cells(NomR,14).value = a
        a='koef3='+str(koef3)
        sheet.Cells(NomR,15).value = a
        a='typeProbability='+str(typeProbability)
        sheet.Cells(NomR,16).value = a
        a='EndAllSolution='+str(EndAllSolution)
        sheet.Cells(NomR,17).value = a
        a='AddFeromonAntZero='+str(AddFeromonAntZero)
        sheet.Cells(NomR,18).value = a
        a='SbrosGraphAllAntZero='+str(SbrosGraphAllAntZero)
        sheet.Cells(NomR,19).value = a
        a='goNewIterationAntZero='+str(goNewIterationAntZero)
        sheet.Cells(NomR,20).value = a
        a='goGraphTree='+str(goGraphTree)
        sheet.Cells(NomR,21).value = a
        a='SortPheromon='+str(SortPheromon)
        sheet.Cells(NomR,22).value = a
        a='KolIteration='+str(KolIteration)
        sheet.Cells(NomR,23).value = a
        a='KolStatIteration='+str(KolStatIteration)
        sheet.Cells(NomR,24).value = a
        a='MaxkolIterationAntZero='+str(MaxkolIterationAntZero)
        sheet.Cells(NomR,25).value = a
        
        NomR=NomR+1
        if typeParametr==1:
          sheet.Cells(NomR,1).value = 'KolAnt' 
        elif typeParametr==2:
          sheet.Cells(NomR,1).value = 'Ro'  
        elif typeParametr==3:
          sheet.Cells(NomR,1).value = 'Q' 
        elif typeParametr==4:
          sheet.Cells(NomR,1).value = 'alf1' 
        elif typeParametr==5:
          sheet.Cells(NomR,1).value = 'alf2'  
        elif typeParametr==6:
          sheet.Cells(NomR,1).value = 'koef1'      
        elif typeParametr==7:
          sheet.Cells(NomR,1).value = 'koef2'  
        elif typeParametr==8:
          sheet.Cells(NomR,1).value = 'KolIter' 
        elif typeParametr==9:
          sheet.Cells(NomR,1).value = 'KolIterZero' 
        sheet.Cells(NomR,2).value = 'M Solution'
        sheet.Cells(NomR,3).value = 'La2 Solution'
        sheet.Cells(NomR,4).value = 'D Solution'
        sheet.Cells(NomR,5).value = 'I(-M)'
        sheet.Cells(NomR,6).value = 'I(+M)'
        sheet.Cells(NomR,7).value = 'Norm Solution'
        sheet.Cells(NomR,8).value = 'Norm I(-M)'
        sheet.Cells(NomR,9).value = 'Norm I(+M)'    
        
        sheet.Cells(NomR,11).value = 'M Iteration'
        sheet.Cells(NomR,12).value = 'La2 Iteration'
        sheet.Cells(NomR,13).value = 'M KolIterAntGoZero'
        sheet.Cells(NomR,14).value = 'La2 KolIterAntGoZero'
        sheet.Cells(NomR,15).value = 'D KolIterAntGoZero'
        sheet.Cells(NomR,16).value = 'I(-M)'
        sheet.Cells(NomR,17).value = 'I(+M)'
        sheet.Cells(NomR,18).value = 'KolAllAntZero'
        sheet.Cells(NomR,19).value = 'KolAntZero'
        sheet.Cells(NomR,20).value = 'SumProcAntZero'
        sheet.Cells(NomR,21).value = 'Time'
        sheet.Cells(NomR,23).value = 'M IterAllAntZero'
        sheet.Cells(NomR,24).value = 'La2 IterAllAntZero'
        sheet.Cells(NomR,25).value = 'D IterAllAntZero'
        sheet.Cells(NomR,26).value = 'I(-M)'
        sheet.Cells(NomR,27).value = 'I(+M)'  
        sheet.Cells(NomR,28).value = 'M SolutionAllAntZero'
        sheet.Cells(NomR,29).value = 'La2 SolutionAllAntZero'
        sheet.Cells(NomR,30).value = 'D SolutionAllAntZero'
        sheet.Cells(NomR,31).value = 'I(-M)'
        sheet.Cells(NomR,32).value = 'I(+M)' 
        
        i=0
        while i<self.lenProcIS:
            sheet.Cells(NomR,34+i*2).value = 'MIter '+str(self.ProcIS[i])
            sheet.Cells(NomR,34+i*2+1).value = 'La2Iter '+str(self.ProcIS[i])
            sheet.Cells(NomR,34+i*2+2*self.lenProcIS+4).value = 'MSol '+str(self.ProcIS[i])
            sheet.Cells(NomR,34+i*2+1+2*self.lenProcIS+4).value = 'La2Sol '+str(self.ProcIS[i])
            sheet.Cells(NomR,34+i+4*self.lenProcIS+8).value = 'OptZn '+str(self.ProcIS[i])
            sheet.Cells(NomR,34+i+5*self.lenProcIS+9).value ='IterZn '+str(self.ProcIS[i])
            sheet.Cells(NomR,34+i+6*self.lenProcIS+10).value = 'KolZn '+str(self.ProcIS[i])
            i=i+1
        i=0
        while i<KolElNomElGraphTree: 
            sheet.Cells(NomR,34+i+7*self.lenProcIS+11).value = 'LevelGT '+str(i)
            i=i+1
    
    
        sheet.Cells(NomR,34+7*self.lenProcIS+KolElNomElGraphTree+12).value = 'OptimPath'
        sheet.Cells(NomR,34+7*self.lenProcIS+KolElNomElGraphTree+13).value = 'M All Time'
        sheet.Cells(NomR,34+7*self.lenProcIS+KolElNomElGraphTree+14).value = 'La2 All Time'
    
        i=0
        while i<self.KolTimeDelEl: 
            sheet.Cells(NomR,34+i*2+7*self.lenProcIS+KolElNomElGraphTree+16).value ='M Time '+str(i)
            sheet.Cells(NomR,34+i*2+1+7*self.lenProcIS+KolElNomElGraphTree+16).value ='La2 Time '+str(i)
            i=i+1
    
    
        
        sheet.Cells(1,1).value=NomR+1
        #сохраняем рабочую книгу
        wb.Save()
        #закрываем ее
        wb.Close()
        #закрываем COM объект
        Excel.Quit()        
        
