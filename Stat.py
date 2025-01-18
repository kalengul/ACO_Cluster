# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 19:14:48 2022

@author: Юрий
"""
import sys

import win32com.client  # Для загрузки из Excel
import json
import os

import GoTime
import LoadSettingsIniFile


class JSONDataAdapter:
    @staticmethod
    def to_json(o):
        if isinstance(o, stat):
            result = o.__dict__
            result["className"] = o.__class__.__name__
            return result


class JSONFile:
    folderJSON = ''
    NameFile = 'currentiter.json'

    def SaveIterJSONFile(Stat, NomStatIteration, Par):
        Stat_json_string = JSONDataAdapter.to_json(Stat)
        json_string = json.dumps([NomStatIteration, Par, Stat_json_string])
        # print(json_string)
        with open(JSONFile.folderJSON + '/' + JSONFile.NameFile, 'w') as f:
            f.write(json_string)

    def LoadIterJSONFileIfExist(Stat, Par):
        if os.path.exists(JSONFile.folderJSON + '/' + JSONFile.NameFile):
            with open(JSONFile.folderJSON + '/' + JSONFile.NameFile, 'r') as f:
                json_string = json.loads(f.read())
                NomStatIteration = json_string[0]
                Par = json_string[1]
                for NameAtr in json_string[2]:
                    Stat.__dict__[NameAtr] = json_string[2][NameAtr]
                return NomStatIteration, Par
        else:
            return 0, Par

    def RemoveJSONFile():
        os.remove(JSONFile.folderJSON + '/' + JSONFile.NameFile)


class stat:

    def __init__(self,KolStatIteration,KolPareto):
        self.MOFI = []
        self.DOFI = []
        self.MOFS = []
        self.DOFS = []
        self.ProcIS = []
        self.EndIS = []
        self.MEndIs = []
        self.OFProc = []
        self.KolEndIs = []
        self.ArrEndIS= []
        self.ArrMOFI= []
        self.ArrDOFI= []
        self.ArrMOFS= []
        self.ArrDOFS= []
        self.ArrOFProc= []
        self.ArrKolEndIs= []
        self.ArrMEndIs = []
        self.NomElGraphTree = []
        #self.ArrTime = []
        #self.DArrTime = []

        self.lenProcIS = 8
        self.KolTimeDelEl = 10

        self.MSolution = []
        self.DSolution = []
        self.MIter = []
        self.DIter = []

        self.OFIter = []
        self.MOFIter = []
        self.DOFIter=[]
        self.MaxOFIter = []
        self.MinOFIter = []

        self.MIterAllAntZero = []
        self.DIterAllAntZero = []
        self.MSltnAllAntZero = []
        self.DSltnAllAntZero = []
        #self.EndAllAntZero = []
        self.KolAllAntZero = []
        self.KolAntZero = []
        self.ProcAntZero = []
        #self.SumProcAntZero = [0]
        self.MTime = []
        self.DTime = []
        self.MSocketTime = []
        self.DSocketTime = []
        self.MClusterTime = []
        self.DClusterTime = []

        self.MIterationAntZero = []
        self.DIterationAntZero = []

        self.MkolParetto = []
        self.MkolParettoElement = []
        self.MkolCurrentParettoSearch = []
        self.DkolCurrentParettoSearch = []
        self.MkolCurrentParettoElement = []
        self.MkolComparisonParetoSet = []
        self.DkolComparisonParetoSet = []

        self.BestOF = []
        self.LowOF = []
        self.ArrBestOF = []
        self.ArrLowOF = []
        self.ArrBestOF.clear()
        self.ArrLowOF.clear()
        j = 0
        while j < KolPareto:
            self.ArrBestOF.append(-sys.maxsize)
            self.ArrLowOF.append(sys.maxsize)
            j = j + 1
        self.StartStatistic(KolStatIteration,KolPareto,1)

    def StartStatistic(self, KolStatIteration, KolPareto, MaxOptimization):
            self.MSolution.clear()
            self.DSolution.clear()
            self.MIter.clear()
            self.DIter.clear()
            self.MIterAllAntZero.clear()
            self.DIterAllAntZero.clear()
            self.MSltnAllAntZero.clear()
            self.DSltnAllAntZero.clear()
            self.KolAllAntZero.clear()
            self.KolAntZero.clear()
            self.ProcAntZero.clear()
            # self.SumProcAntZero = [0]
            self.MIterationAntZero.clear()
            self.DIterationAntZero.clear()
            self.MTime.clear()
            self.DTime.clear()
            self.MkolParetto.clear()
            self.MkolParettoElement.clear()
            self.MkolCurrentParettoSearch.clear()
            self.DkolCurrentParettoSearch.clear()
            self.MkolCurrentParettoElement.clear()
            self.MkolComparisonParetoSet.clear()
            self.DkolComparisonParetoSet.clear()
            self.OFIter.clear()
            self.MOFIter.clear()
            self.DOFIter.clear()
            self.MaxOFIter.clear()
            self.MinOFIter.clear()
            self.MOFI.clear()
            self.DOFI.clear()
            self.MOFS.clear()
            self.DOFS.clear()
            #self.ProcIS.clear()
            self.EndIS.clear()
            self.MEndIs.clear()
            self.OFProc.clear()
            self.KolEndIs.clear()
            self.ArrEndIS.clear()
            self.ArrMOFI.clear()
            self.ArrDOFI.clear()
            self.ArrMOFS.clear()
            self.ArrDOFS.clear()
            self.ArrOFProc.clear()
            self.ArrKolEndIs.clear()
            self.ArrMEndIs.clear()
            self.NomElGraphTree.clear()
            print('KolStatIteration=', KolStatIteration,'BestOF=', self.BestOF,'LowOF=',self.LowOF)
            NomIteration = 0
            while NomIteration < KolStatIteration:
                self.EndIS.append([])
                self.MOFI.append([])
                self.DOFI.append([])
                self.MOFS.append([])
                self.DOFS.append([])
                self.OFProc.append([])
                self.KolEndIs.append([])
                self.ArrEndIS.append([])
                self.ArrMOFI.append([])
                self.ArrDOFI.append([])
                self.ArrMOFS.append([])
                self.ArrDOFS.append([])
                self.ArrOFProc.append([])
                self.ArrKolEndIs.append([])
                # self.ArrTime.append([])
                self.ArrMEndIs.append([])
                self.MEndIs.append([])
                self.OFIter.append([])
                self.MaxOFIter.append([])
                self.MinOFIter.append([])
                self.MOFIter.append([])
                self.DOFIter.append([])
                self.MSolution.append(0)
                self.DSolution.append(0)
                self.MIter.append(0)
                self.DIter.append(0)
                self.MIterAllAntZero.append(0)
                self.DIterAllAntZero.append(0)
                self.MSltnAllAntZero.append(0)
                self.DSltnAllAntZero.append(0)
                self.KolAllAntZero.append(0)
                self.KolAntZero.append(0)
                self.ProcAntZero.append(0)
                # self.SumProcAntZero = [0]
                self.MIterationAntZero.append(0)
                self.DIterationAntZero.append(0)
                self.MTime.append(0)
                self.DTime.append(0)
                self.MkolParetto.append(0)
                self.MkolParettoElement.append(0)
                self.MkolCurrentParettoSearch.append(0)
                self.DkolCurrentParettoSearch.append(0)
                self.MkolCurrentParettoElement.append(0)
                self.MkolComparisonParetoSet.append(0)
                self.DkolComparisonParetoSet.append(0)
                # print(self.EndIS)
                j = 0
                while j < KolPareto:
                    if MaxOptimization == 1:
                        self.OFIter[NomIteration].append(-sys.maxsize)
                    else:
                        self.OFIter[NomIteration].append(sys.maxsize)
                    self.MaxOFIter[NomIteration].append(-sys.maxsize)
                    self.MinOFIter[NomIteration].append(sys.maxsize)
                    self.MOFIter[NomIteration].append(0)
                    self.DOFIter[NomIteration].append(0)
                    j = j + 1

                # self.EndAllAntZero.append(0)
                i = 0
                while i < self.lenProcIS:
                    self.EndIS[NomIteration].append(0)
                    self.MOFI[NomIteration].append(0)
                    self.DOFI[NomIteration].append(0)
                    self.MOFS[NomIteration].append(0)
                    self.DOFS[NomIteration].append(0)
                    self.OFProc[NomIteration].append(0)
                    # print(self.KolEndIs,self.MEndIs,NomIteration)
                    self.KolEndIs[NomIteration].append(0)
                    self.MEndIs[NomIteration].append(0)
                    self.ArrEndIS[NomIteration].append([])
                    self.ArrMOFI[NomIteration].append([])
                    self.ArrDOFI[NomIteration].append([])
                    self.ArrMOFS[NomIteration].append([])
                    self.ArrDOFS[NomIteration].append([])
                    self.ArrOFProc[NomIteration].append([])
                    self.ArrKolEndIs[NomIteration].append([])
                    self.ArrMEndIs[NomIteration].append([])
                    j = 0
                    while j < KolPareto:
                        self.ArrEndIS[NomIteration][i].append(0)
                        self.ArrMOFI[NomIteration][i].append(0)
                        self.ArrDOFI[NomIteration][i].append(0)
                        self.ArrMOFS[NomIteration][i].append(0)
                        self.ArrDOFS[NomIteration][i].append(0)
                        self.ArrOFProc[NomIteration][i].append(0)
                        self.ArrKolEndIs[NomIteration][i].append(0)
                        self.ArrMEndIs[NomIteration][i].append(0)
                        j = j + 1
                    i = i + 1
                # i = 0
                # while i < self.KolTimeDelEl:
                #    self.ArrTime.append(0.0)
                #    self.DArrTime.append(0.0)
                #    i = i + 1
                NomIteration = NomIteration + 1
            #print('KolStatIteration=', KolStatIteration, 'KolPareto=', KolStatIteration, self.MOFIter)

    def load_pareto_set_excel(self,NameFile,KolPareto):
        AllParetoSet = []
        pathArrParetoSet = []
        AllSolution = 0
        NomParetoSet = 0
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(NameFile)
        sheet = wb.ActiveSheet
        j = 0
        while j < len(self.ArrBestOF):
            self.ArrBestOF[j]=sheet.Cells(1, 8 + j).value
            self.ArrLowOF[j]=sheet.Cells(1, 8 + j + 1 + len(self.ArrBestOF)).value
            j = j + 1
        print('ArrBestOF=',self.ArrBestOF,'ArrLowOF=',self.ArrLowOF)
        st=sheet.Cells(2+NomParetoSet, 1).value
        while st!=None:
            ElParetoSet=[]
            NomEl=0
            while NomEl<KolPareto:
                st = sheet.Cells(2 + NomParetoSet, 1+NomEl).value
                ElParetoSet.append(float(st))
                NomEl=NomEl+1
            AllParetoSet.append(ElParetoSet)
            ElpathArrParetoSet=[]
            NomEl = 0
            while st!=None:
                st = sheet.Cells(2 + NomParetoSet, 1 + len(ElParetoSet) + 1 + NomEl).value
                if st!=None:
                    ElpathArrParetoSet.append(float(st))
                NomEl = NomEl + 1
            pathArrParetoSet.append(ElpathArrParetoSet)
            #print(NomParetoSet, ElParetoSet, ElpathArrParetoSet)
            NomParetoSet=NomParetoSet+1
            st = sheet.Cells(2 + NomParetoSet, 1).value
        # сохраняем рабочую книгу
        wb.Save()
        # закрываем ее
        wb.Close()
        # закрываем COM объект
        Excel.Quit()
        AllSolution=len(AllParetoSet)
        print(GoTime.now(), 'load_pareto_set_excel', NameFile,AllSolution)
        return AllParetoSet, pathArrParetoSet, AllSolution

    def save_pareto_set_excel(self, NameFile, TimeParetoSet, AllParetoSet, pathArrParetoSet, AllSolution):
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(NameFile)
        sheet = wb.ActiveSheet
        sheet.Cells(1, 1).value = 'TimeParetoSet'
        sheet.Cells(1, 2).value = (TimeParetoSet).total_seconds()
        sheet.Cells(1, 3).value = 'AllParetoSet'
        sheet.Cells(1, 4).value = len(AllParetoSet)
        sheet.Cells(1, 5).value = 'AllSolution'
        sheet.Cells(1, 6).value = AllSolution
        j=0
        while j<len(self.ArrBestOF):
            sheet.Cells(1, 8+j).value = self.ArrBestOF[j]
            sheet.Cells(1, 8+j+1+len(self.ArrBestOF)).value = self.ArrLowOF[j]
            j=j+1
        print('start_save', NameFile)
        NomParetoSet = 0
        if len(AllParetoSet) > 0:
            while NomParetoSet < len(AllParetoSet):
                ElNomParetoSet = 0
                while ElNomParetoSet < len(AllParetoSet[NomParetoSet]):
                    sheet.Cells(2 + NomParetoSet, 1 + ElNomParetoSet).value = AllParetoSet[NomParetoSet][ElNomParetoSet]
                    ElNomParetoSet = ElNomParetoSet + 1
                ElNomParetoSet = 0
                if len(pathArrParetoSet) > 0:
                    while ElNomParetoSet < len(pathArrParetoSet[NomParetoSet]):
                        sheet.Cells(2 + NomParetoSet, 1 + len(AllParetoSet[NomParetoSet]) + 1 + ElNomParetoSet).value = \
                        pathArrParetoSet[NomParetoSet][ElNomParetoSet]
                        ElNomParetoSet = ElNomParetoSet + 1
                NomParetoSet = NomParetoSet + 1
                if NomParetoSet%1000==0:
                    print('save ',NomParetoSet)
        # сохраняем рабочую книгу
        wb.Save()
        # закрываем ее
        wb.Close()
        # закрываем COM объект
        Excel.Quit()
        input()


    def SaveStatisticsExcelParetto(self, NameFile, KolStatistics, koliter, NomC):
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(NameFile)
        sheet = wb.ActiveSheet
        NomR = sheet.Cells(1, 1).value-KolStatistics+1
        NomStatistics = 0
        while NomStatistics < KolStatistics:
            sheet.Cells(NomR - 1, NomC).value = self.MkolParetto[NomStatistics]
            sheet.Cells(NomR - 1, NomC + 1).value = self.MkolParettoElement[NomStatistics]
            sheet.Cells(NomR - 1, NomC + 2).value = self.MkolCurrentParettoSearch[NomStatistics] / koliter
            sheet.Cells(NomR - 1, NomC + 3).value = self.DkolCurrentParettoSearch[NomStatistics] / koliter
            sheet.Cells(NomR - 1, NomC + 4).value = self.MkolCurrentParettoElement[NomStatistics]
            sheet.Cells(NomR - 1, NomC + 5).value = self.MkolComparisonParetoSet[NomStatistics] / koliter
            sheet.Cells(NomR - 1, NomC + 6).value = self.DkolComparisonParetoSet[NomStatistics] / koliter
            NomStatistics=NomStatistics+1
            NomR=NomR+1
        # сохраняем рабочую книгу
        wb.Save()
        # закрываем ее
        wb.Close()
        # закрываем COM объект
        Excel.Quit()

    def SaveStatisticsExcel(self, NameFile, KolIterationEnd,KolStatistics, KolAnt, KolPareto, time, koliter, OptimPath, P):
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(NameFile)
        sheet = wb.ActiveSheet
        NomR = int(sheet.Cells(1, 1).value)
        NomStatistics=0
        while NomStatistics<KolStatistics:
            sheet.Cells(NomR, 1).value = KolIterationEnd // KolStatistics * NomStatistics
            sheet.Cells(NomR, 2).value = koliter
            sheet.Cells(NomR, 3).value = KolAnt

            sheet.Cells(NomR, 4).value = OptimPath
            sheet.Cells(NomR, 5).value = self.MTime[NomStatistics] / koliter
            sheet.Cells(NomR, 6).value = self.DTime[NomStatistics] / koliter
            sheet.Cells(NomR, 7).value = '=F'+str(NomR)+'-E'+str(NomR)+'*E'+str(NomR)  #=E5-D5*D5
            sheet.Cells(NomR, 8).value = '=E' + str(NomR) + '-SQRT(G' + str(NomR) + ')/SQRT(B' + str(NomR)+')*$B$1' #=D5-SQRT(F5)/SQRT(B5)*B1
            sheet.Cells(NomR, 9).value = '=E' + str(NomR) + '+SQRT(G' + str(NomR) + ')/SQRT(B' + str(NomR)+')*$B$1' #=D5+SQRT(F5)/SQRT(B5)*B1
            sheet.Cells(NomR, 10).value = '=E' + str(NomR) + '/(A' + str(NomR) + '*C' + str(NomR)+')' #=D5/(A5*C5)
            sheet.Cells(NomR, 11).value = '=J' + str(NomR) + '-SQRT(G' + str(NomR) + ')/SQRT(B' + str(NomR)+')*$B$1' #=I5-SQRT(F5)/SQRT(B5)*$B$1
            sheet.Cells(NomR, 12).value = '=J' + str(NomR) + '+SQRT(G' + str(NomR) + ')/SQRT(B' + str(NomR)+')*$B$1' #=I5+SQRT(F5)/SQRT(B5)*$B$1
            sheet.Cells(NomR, 13).value = self.KolAllAntZero[NomStatistics] / koliter
            sheet.Cells(NomR, 14).value = self.KolAntZero[NomStatistics] / koliter
            sheet.Cells(NomR, 15).value = self.MIterationAntZero[NomStatistics] / koliter
            sheet.Cells(NomR, 16).value = self.DIterationAntZero[NomStatistics] / koliter
            sheet.Cells(NomR, 17).value = '=P' + str(NomR) + '-O' + str(NomR) + '*O' + str(NomR)  # =E5-D5*D5
            sheet.Cells(NomR, 18).value = '=O' + str(NomR) + '-SQRT(Q' + str(NomR) + ')/SQRT(B' + str(
                NomR) + ')*$B$1'  # =D5-SQRT(F5)/SQRT(B5)*B1
            sheet.Cells(NomR, 19).value = '=O' + str(NomR) + '+SQRT(Q' + str(NomR) + ')/SQRT(B' + str(
                NomR) + ')*$B$1'  # =D5+SQRT(F5)/SQRT(B5)*B1
            sheet.Cells(NomR, 20).value = self.MSolution[NomStatistics] / koliter
            sheet.Cells(NomR, 21).value = self.DSolution[NomStatistics] / koliter
            sheet.Cells(NomR, 22).value = '=U'+str(NomR)+'-T'+str(NomR)+'*T'+str(NomR)  #=E5-D5*D5
            sheet.Cells(NomR, 23).value = '=T' + str(NomR) + '-SQRT(V' + str(NomR) + ')/SQRT(B' + str(NomR)+')*$B$1' #=D5-SQRT(F5)/SQRT(B5)*B1
            sheet.Cells(NomR, 24).value = '=T' + str(NomR) + '+SQRT(V' + str(NomR) + ')/SQRT(B' + str(NomR)+')*$B$1' #=D5+SQRT(F5)/SQRT(B5)*B1
            sheet.Cells(NomR, 25).value = '=T' + str(NomR) + '/(A' + str(NomR) + '*C' + str(NomR)+')' #=D5/(A5*C5)
            sheet.Cells(NomR, 26).value = '=Y' + str(NomR) + '-SQRT(V' + str(NomR) + ')/SQRT(B' + str(NomR)+')*$B$1' #=I5-SQRT(F5)/SQRT(B5)*$B$1
            sheet.Cells(NomR, 27).value = '=Y' + str(NomR) + '+SQRT(V' + str(NomR) + ')/SQRT(B' + str(NomR)+')*$B$1' #=I5+SQRT(F5)/SQRT(B5)*$B$1
            sheet.Cells(NomR, 28).value = self.MIter[NomStatistics] / koliter
            sheet.Cells(NomR, 29).value = self.DIter[NomStatistics] / koliter

            NomC=40
            #sheet.Cells(NomR, 23).value = self.MIterAllAntZero / koliter
            #sheet.Cells(NomR, 24).value = self.DIterAllAntZero / koliter

            #sheet.Cells(NomR, 30).value = self.SumProcAntZero / koliter
            #sheet.Cells(NomR, 31).value = str(time)

            #sheet.Cells(NomR, 34).value = self.MSltnAllAntZero / koliter
            #sheet.Cells(NomR, 35).value = self.DSltnAllAntZero / koliter
            i = 0
            while i<KolPareto:
                j = 0
                while j < self.lenProcIS:
                    if self.ArrKolEndIs[NomStatistics][j][i] != 0:
                        sheet.Cells(NomR, NomC + j * 2).value = self.ArrMOFI[NomStatistics][j][i] / self.ArrKolEndIs[NomStatistics][j][i]
                        sheet.Cells(NomR, NomC + j * 2 + 1).value = self.ArrDOFI[NomStatistics][j][i] / self.ArrKolEndIs[NomStatistics][j][i]
                        sheet.Cells(NomR, NomC + j * 2 + 2 * self.lenProcIS + 4).value = self.ArrMOFS[NomStatistics][j][i] / self.ArrKolEndIs[NomStatistics][j][i]
                        sheet.Cells(NomR, NomC + j * 2 + 1 + 2 * self.lenProcIS + 4).value = self.ArrDOFS[NomStatistics][j][i] / self.ArrKolEndIs[NomStatistics][j][i]
                        sheet.Cells(NomR, NomC + j + 4 * self.lenProcIS + 9).value = self.ArrKolEndIs[NomStatistics][j][i] / koliter
                        sheet.Cells(NomR, NomC + j + 5 * self.lenProcIS + 10).value = self.ArrOFProc[NomStatistics][j][i] / self.ArrKolEndIs[NomStatistics][j][i]
                        sheet.Cells(NomR, NomC + j + 6 * self.lenProcIS + 11).value = self.ArrMEndIs[NomStatistics][j][i] / self.ArrKolEndIs[NomStatistics][j][i]
                    j = j + 1
                    sheet.Cells(NomR, NomC + 4 * self.lenProcIS + 4).value = '=BO' + str(NomR) + '-BN' + str(NomR) + '*BN' + str(NomR)  # =E5-D5*D5
                    sheet.Cells(NomR, NomC + 4 * self.lenProcIS + 5).value = '=BN' + str(NomR) + '-SQRT(BP' + str(NomR) + ')/SQRT(B' + str(
                        NomR) + ')*$B$1'  # =D5-SQRT(F5)/SQRT(B5)*B1
                    sheet.Cells(NomR, NomC + 4 * self.lenProcIS + 6).value = '=BN' + str(NomR) + '+SQRT(BP' + str(NomR) + ')/SQRT(B' + str(
                        NomR) + ')*$B$1'  # =D5+SQRT(F5)/SQRT(B5)*B1
                sheet.Cells(NomR, NomC  + 7 * self.lenProcIS+12).value = self.MOFIter[NomStatistics][i]/ koliter
                sheet.Cells(NomR, NomC + 7 * self.lenProcIS + 13).value = self.DOFIter[NomStatistics][i] / koliter
                sheet.Cells(NomR, NomC + 7 * self.lenProcIS + 14).value = self.MinOFIter[NomStatistics][i]
                sheet.Cells(NomR, NomC + 7 * self.lenProcIS + 15).value = self.MaxOFIter[NomStatistics][i]
                NomC = NomC  + 7 * self.lenProcIS + 18
                i = i + 1
            #i = 0
            #while i < len(self.NomElGraphTree):
            #    sheet.Cells(NomR, 34 + i + 7 * self.lenProcIS + 11).value = self.NomElGraphTree[i] / koliter
            #    i = i + 1



            #i = 0
            #while i < len(self.ArrTime):
            #    sheet.Cells(NomR, 34 + i * 2 + 7 * self.lenProcIS + len(self.NomElGraphTree) + 16).value = self.ArrTime[
            #                                                                                                   i] / koliter
            #    sheet.Cells(NomR, 34 + i * 2 + 1 + 7 * self.lenProcIS + len(self.NomElGraphTree) + 16).value = \
            #        self.DArrTime[i] / koliter
            #    i = i + 1
            NomStatistics=NomStatistics+1
            NomR=NomR+1
        sheet.Cells(1, 1).value = NomR
        # сохраняем рабочую книгу
        wb.Save()
        # закрываем ее
        wb.Close()
        # закрываем COM объект
        Excel.Quit()

    def SaveTimeIteration(self,NomStatistics, time1):
        #print('time=', self.MTime, self.DTime,time1, NomStatistics)
        self.MTime[NomStatistics] = self.MTime[NomStatistics] + time1
        self.DTime[NomStatistics] = self.DTime[NomStatistics] + time1 * time1

    def StatIterationAntZero(self, NomStatistics,NomIteration):
        #print('IterationAntZero=',self.MIterationAntZero,self.DIterationAntZero,NomIteration,NomStatistics)
        self.MIterationAntZero[NomStatistics] = self.MIterationAntZero[NomStatistics] + NomIteration
        self.DIterationAntZero[NomStatistics] = self.DIterationAntZero[NomStatistics] + NomIteration*NomIteration

    def StatIncAllAntZero(self,NomStatistics):
        print('StatIncAllAntZero=',self.KolAllAntZero,self.MIterAllAntZero,self.DIterAllAntZero,NomIteration,NomSolution,NomStatistics)
        self.KolAllAntZero[NomStatistics] = self.KolAllAntZero[NomStatistics] + 1

    def StatIncAntZero(self,NomStatistics):
        #print('StatIncAllAntZero=',self.KolAllAntZero,self.MIterAllAntZero,self.DIterAllAntZero,NomIteration,NomSolution,NomStatistics)
        self.KolAntZero[NomStatistics] = self.KolAntZero[NomStatistics] + 1

    def StatParettoSet(self, NomStatistics, KolArrayPareto, kolParetto, kolParettoElement, CurrentParettoSearch, kolCurrentParettoElement,
                       ComparisonParetoSet):
        #print('StatParettoSet=',self.MkolCurrentParettoSearch,self.MkolCurrentParettoElement,self.MkolParetto,CurrentParettoSearch,kolCurrentParettoElement,NomStatistics)
        self.MkolParetto[NomStatistics] = kolParetto
        self.MkolParettoElement[NomStatistics] = kolParettoElement
        self.MkolCurrentParettoSearch[NomStatistics] = self.MkolCurrentParettoSearch[NomStatistics] + CurrentParettoSearch
        self.DkolCurrentParettoSearch[NomStatistics] = self.DkolCurrentParettoSearch[NomStatistics] + CurrentParettoSearch * CurrentParettoSearch
        self.MkolCurrentParettoElement[NomStatistics] = kolCurrentParettoElement
        self.MkolComparisonParetoSet[NomStatistics] = self.MkolComparisonParetoSet[NomStatistics] + len(ComparisonParetoSet)
        self.DkolComparisonParetoSet[NomStatistics] = self.DkolComparisonParetoSet[NomStatistics] + len(ComparisonParetoSet) * len(
            ComparisonParetoSet)
        #print('OFIter=', KolArrayPareto, NomStatistics, self.OFIter,NomStatistics, self.MinOFIter, self.MaxOFIter)
        NomPareto=0
        while NomPareto<KolArrayPareto:
            if (self.OFIter[NomStatistics][NomPareto] != sys.maxsize) and (self.OFIter[NomStatistics][NomPareto] != -sys.maxsize):
                self.MOFIter[NomStatistics][NomPareto] = self.MOFIter[NomStatistics] [NomPareto]+ self.OFIter[NomStatistics][NomPareto]
                self.DOFIter[NomStatistics][NomPareto] = self.DOFIter[NomStatistics][NomPareto] + self.OFIter[NomStatistics][NomPareto]*self.OFIter[NomStatistics][NomPareto]
                if self.OFIter[NomStatistics][NomPareto]<self.MinOFIter[NomStatistics][NomPareto]:
                    self.MinOFIter[NomStatistics][NomPareto]= self.OFIter[NomStatistics][NomPareto]
                if self.OFIter[NomStatistics][NomPareto]>self.MaxOFIter[NomStatistics][NomPareto]:
                    self.MaxOFIter[NomStatistics][NomPareto] = self.OFIter[NomStatistics][NomPareto]
            NomPareto=NomPareto+1

    def EndStatistik(self, NomStatistics, NomIteration, NomSolution):
        #print('Solution=', self.MSolution, self.DSolution,NomSolution,'iter=', self.MIter, self.DIter,NomIteration, NomStatistics, self.lenProcIS,self.MEndIs)
        #print('Solution=', NomIteration, NomStatistics, self.lenProcIS, self.MEndIs, self.EndIS)
        self.MSolution[NomStatistics] = self.MSolution[NomStatistics] + NomSolution
        self.DSolution[NomStatistics] = self.DSolution[NomStatistics] + NomSolution * NomSolution
        self.MIter[NomStatistics] = self.MIter[NomStatistics] + NomIteration
        self.DIter[NomStatistics] = self.DIter[NomStatistics] + NomIteration * NomIteration
        #self.SumProcAntZero[NomStatistics] = self.SumProcAntZero[NomStatistics] + self.ProcAntZero / NomIteration
        i = 0
        while i < self.lenProcIS:
            self.MEndIs[NomStatistics][i] = self.MEndIs[NomStatistics][i] + self.EndIS[NomStatistics][i]
            i = i + 1


    def ProcBestOFArray(self, NomStatistics, OF, NomArr, MaxOptimization, NomIteration, NomSolution):
        if (OF != sys.maxsize) and (OF != -sys.maxsize):
            i = 0
            #print('ProcBestOFArray',NomStatistics,NomArr,OF,self.OFIter,self.ArrBestOF,self.ArrLowOF,self.ProcIS, self.ArrEndIS)
            while i < self.lenProcIS:
                if MaxOptimization == 1:
                    if OF>self.OFIter[NomStatistics][NomArr]:
                        self.OFIter[NomStatistics][NomArr]=OF
                    #print(OF,NomArr,(self.ArrBestOF[NomArr] - self.ArrLowOF[NomArr]) * self.ProcIS[i] + self.ArrLowOF[NomArr],self.ArrEndIS[NomStatistics][i][NomArr])
                    if (self.ArrBestOF[NomArr] - self.ArrLowOF[NomArr]) * self.ProcIS[i] + self.ArrLowOF[NomArr] <= OF and \
                            self.ArrEndIS[NomStatistics][i][NomArr]== 0:
                        self.ArrMOFI[NomStatistics][i][NomArr] = self.ArrMOFI[NomStatistics][i][NomArr] + NomIteration
                        self.ArrDOFI[NomStatistics][i][NomArr] = self.ArrDOFI[NomStatistics][i][NomArr] + NomIteration * NomIteration
                        self.ArrMOFS[NomStatistics][i][NomArr] = self.ArrMOFS[NomStatistics][i][NomArr] + NomSolution
                        self.ArrDOFS[NomStatistics][i][NomArr] = self.ArrDOFS[NomStatistics][i][NomArr] + NomSolution * NomSolution
                        self.ArrOFProc[NomStatistics][i][NomArr] = self.ArrOFProc[NomStatistics][i][NomArr] + OF
                        self.ArrKolEndIs[NomStatistics][i][NomArr] = self.ArrKolEndIs[NomStatistics][i][NomArr] + 1
                    if (self.ArrBestOF[NomArr] - self.ArrLowOF[NomArr]) * self.ProcIS[i] + self.ArrLowOF[NomArr] <= OF:
                        self.ArrEndIS[NomStatistics][i][NomArr] = self.ArrEndIS[NomStatistics][i][NomArr] + 1
                        self.ArrMEndIs[NomStatistics][i][NomArr] = self.ArrMEndIs[NomStatistics][i][NomArr] + 1
                else:
                    if OF<self.OFIter[NomStatistics][NomArr]:
                        self.OFIter[NomStatistics][NomArr]=OF
                    if self.ArrBestOF[NomArr] - (self.ArrBestOF[NomArr] - self.ArrLowOF[NomArr]) * self.ProcIS[i] >= OF and self.ArrEndIS[NomStatistics][i][NomArr] == 0:
                        self.ArrMOFI[NomStatistics][i][NomArr] = self.ArrMOFI[NomStatistics][i][NomArr] + NomIteration
                        self.ArrDOFI[NomStatistics][i][NomArr] = self.ArrDOFI[NomStatistics][i][NomArr] + NomIteration * NomIteration
                        self.ArrMOFS[NomStatistics][i][NomArr] = self.ArrMOFS[NomStatistics][i][NomArr] + NomSolution
                        self.ArrDOFS[NomStatistics][i][NomArr] = self.ArrDOFS[NomStatistics][i][NomArr] + NomSolution * NomSolution
                        self.ArrOFProc[NomStatistics][i][NomArr] = self.ArrOFProc[NomStatistics][i][NomArr] + OF
                        self.ArrKolEndIs[NomStatistics][i][NomArr] = self.ArrKolEndIs[NomStatistics][i][NomArr] + 1
                    if self.ArrBestOF[NomArr] - (self.ArrBestOF[NomArr] - self.ArrLowOF[NomArr]) * self.ProcIS[i] >= OF:
                        self.ArrEndIS[NomStatistics][i][NomArr] = self.ArrEndIS[NomStatistics][i][NomArr] + 1
                        self.ArrMEndIs[NomStatistics][i][NomArr] = self.ArrMEndIs[NomStatistics][i][NomArr] + 1
                i = i + 1


    def SbrosStatistic(self,KolStatistics,KolPareto):
        NomStatistics=0
        while NomStatistics<KolStatistics:
            self.EndIS[NomStatistics].clear()
            self.ArrEndIS[NomStatistics].clear()
            #self.EndAllAntZero[NomStatistics] = 0
            i = 0
            while i < self.lenProcIS:
                self.EndIS[NomStatistics].append(0)
                self.ArrEndIS[NomStatistics].append([])
                j = 0
                while j < KolPareto:
                    self.ArrEndIS[NomStatistics][i].append(0)
                    j=j+1
                i = i + 1
            NomStatistics=NomStatistics+1

    def StartStatisticGrahTree(self, KolEl):
        self.NomElGraphTree.clear()
        i = 0
        while i < KolEl:
            self.NomElGraphTree.append(0)
            i = i + 1

    def SaveParametr(self, version, NameFile, N, Ro, Q, KolElitAgent, DeltZeroPheromon, alf1, alf2, alf3, koef1, koef2,
                     koef3, typeProbability, EndAllSolution, NameFileXL, AddFeromonAntZero, SbrosGraphAllAntZero,
                     goNewIterationAntZero, goGraphTree, SortPheromon, KolIteration, KolStatIteration,
                     MaxkolIterationAntZero, typeParametr, GoParallelAnt, KolParallelAnt, KolElNomElGraphTree, KoefLineSummPareto,
                     KolPareto, Best, Low):

        self.BestOF = Best
        self.LowOF = Low
        self.ProcIS.clear()
        self.ProcIS.append(0.5)
        self.ProcIS.append(0.75)
        self.ProcIS.append(0.90)
        self.ProcIS.append(0.95)
        self.ProcIS.append(0.99)
        self.ProcIS.append(0.999)
        self.ProcIS.append(0.9999)
        self.ProcIS.append(1)

        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(NameFile)
        sheet = wb.ActiveSheet
        NomR = sheet.Cells(1, 1).value

        a = 'Version - ' + version
        sheet.Cells(NomR, 5).value = a
        a = 'NameFilePar= ' + NameFileXL
        sheet.Cells(NomR, 6).value = a
        a = 'N=' + str(N)
        sheet.Cells(NomR, 7).value = a
        a = 'Ro=' + str(Ro)
        sheet.Cells(NomR, 8).value = a
        a = 'Q=' + str(Q)
        sheet.Cells(NomR, 9).value = a
        a = 'alf1=' + str(alf1)
        sheet.Cells(NomR, 10).value = a
        a = 'alf2=' + str(alf2)
        sheet.Cells(NomR, 11).value = a
        a = 'alf3=' + str(alf3)
        sheet.Cells(NomR, 12).value = a
        a = 'koef1=' + str(koef1)
        sheet.Cells(NomR, 13).value = a
        a = 'koef2=' + str(koef2)
        sheet.Cells(NomR, 14).value = a
        a = 'koef3=' + str(koef3)
        sheet.Cells(NomR, 15).value = a
        a = 'typeProbability=' + str(typeProbability)
        sheet.Cells(NomR, 16).value = a
        a = 'EndAllSolution=' + str(EndAllSolution)
        sheet.Cells(NomR, 17).value = a
        a = 'AddFeromonAntZero=' + str(AddFeromonAntZero)
        sheet.Cells(NomR, 18).value = a
        a = 'SbrosGraphAllAntZero=' + str(SbrosGraphAllAntZero)
        sheet.Cells(NomR, 19).value = a
        a = 'goNewIterationAntZero=' + str(goNewIterationAntZero)
        sheet.Cells(NomR, 20).value = a
        a = 'goGraphTree=' + str(goGraphTree)
        sheet.Cells(NomR, 21).value = a
        a = 'SortPheromon=' + str(SortPheromon)
        sheet.Cells(NomR, 22).value = a
        a = 'KolIteration=' + str(KolIteration)
        sheet.Cells(NomR, 23).value = a
        a = 'KolStatIteration=' + str(KolStatIteration)
        sheet.Cells(NomR, 24).value = a
        a = 'MaxkolIterationAntZero=' + str(MaxkolIterationAntZero)
        sheet.Cells(NomR, 25).value = a
        a = 'KolElitAgent=' + str(KolElitAgent)
        sheet.Cells(NomR, 26).value = a
        a = 'DeltZeroPheromon=' + str(DeltZeroPheromon)
        sheet.Cells(NomR, 27).value = a
        a = 'GoParallelAnt=' + str(GoParallelAnt)
        sheet.Cells(NomR, 28).value = a
        a = 'KolParallelAnt=' + str(KolParallelAnt)
        sheet.Cells(NomR, 29).value = a
        a = 'KoefLineSummPareto =' + str(KoefLineSummPareto)
        sheet.Cells(NomR, 30).value = a
        a = 'KolPareto =' + str(KolPareto)
        sheet.Cells(NomR, 31).value = a

        NomR = NomR + 1
        if typeParametr == 1:
            sheet.Cells(NomR, 1).value = 'KolAnt'
        elif typeParametr == 2:
            sheet.Cells(NomR, 1).value = 'Ro'
        elif typeParametr == 3:
            sheet.Cells(NomR, 1).value = 'Q'
        elif typeParametr == 4:
            sheet.Cells(NomR, 1).value = 'alf1'
        elif typeParametr == 5:
            sheet.Cells(NomR, 1).value = 'alf2'
        elif typeParametr == 6:
            sheet.Cells(NomR, 1).value = 'koef1'
        elif typeParametr == 7:
            sheet.Cells(NomR, 1).value = 'koef2'
        elif typeParametr == 8:
            sheet.Cells(NomR, 1).value = 'KolIter'
        elif typeParametr == 9:
            sheet.Cells(NomR, 1).value = 'KolIterZero'
        sheet.Cells(NomR, 2).value = 'Kol Stat'
        sheet.Cells(NomR, 3).value = 'Kol Ant'
        sheet.Cells(NomR, 4).value = 'OptimPath'
        sheet.Cells(NomR, 5).value = 'M All Time'
        sheet.Cells(NomR, 6).value = 'La2 All Time'
        sheet.Cells(NomR, 7).value = 'D All Time'
        sheet.Cells(NomR, 8).value = 'I(-M)'
        sheet.Cells(NomR, 9).value = 'I(+M)'
        sheet.Cells(NomR, 10).value = 'Norm All Time'
        sheet.Cells(NomR, 11).value = 'Norm I(-M)'
        sheet.Cells(NomR, 12).value = 'Norm I(+M)'
        sheet.Cells(NomR, 13).value = 'KolZeroIteration'
        sheet.Cells(NomR, 14).value = 'KolZeroAnt'
        sheet.Cells(NomR, 15).value = 'M DopIterAntZero'
        sheet.Cells(NomR, 16).value = 'La2 DopIterAntZero'
        sheet.Cells(NomR, 17).value = 'D DopIterAntZero'
        sheet.Cells(NomR, 18).value = 'I(-M)'
        sheet.Cells(NomR, 19).value = 'I(+M)'
        sheet.Cells(NomR, 20).value = 'M Solution'
        sheet.Cells(NomR, 21).value = 'La2 Solution'
        sheet.Cells(NomR, 22).value = 'D Solution'
        sheet.Cells(NomR, 23).value = 'I(-M)'
        sheet.Cells(NomR, 24).value = 'I(+M)'
        sheet.Cells(NomR, 25).value = 'Norm Solution'
        sheet.Cells(NomR, 26).value = 'Norm I(-M)'
        sheet.Cells(NomR, 27).value = 'Norm I(+M)'
        sheet.Cells(NomR, 28).value = 'M Iteration'
        sheet.Cells(NomR, 29).value = 'La2 Iteration'

        NomC = 40


        j = 0
        while j < KolPareto:
            i = 0
            while i < self.lenProcIS:
                sheet.Cells(NomR, NomC + i * 2).value = 'MIter '+str(j) +' '+ str(self.ProcIS[i])
                sheet.Cells(NomR, NomC + i * 2 + 1).value = 'La2Iter '+str(j)  +' '+ str(self.ProcIS[i])
                sheet.Cells(NomR, NomC + i * 2 + 2 * self.lenProcIS + 4).value = 'MSol '+str(j) +' ' + str(self.ProcIS[i])
                sheet.Cells(NomR, NomC + i * 2 + 1 + 2 * self.lenProcIS + 4).value = 'La2Sol '+str(j) +' ' + str(self.ProcIS[i])
                sheet.Cells(NomR, NomC + i + 4 * self.lenProcIS + 9).value = 'IterZn '+str(j) +' ' + str(self.ProcIS[i])
                sheet.Cells(NomR, NomC + i + 5 * self.lenProcIS + 10).value = 'OptZn '+str(j) +' ' + str(self.ProcIS[i])
                sheet.Cells(NomR, NomC + i + 6 * self.lenProcIS + 11).value = 'KolZn '+str(j) +' ' + str(self.ProcIS[i])
                i = i + 1
            sheet.Cells(NomR, NomC + 7 * self.lenProcIS + 12).value = 'MOpt'
            sheet.Cells(NomR, NomC + 7 * self.lenProcIS + 13).value = 'La2Opt'
            sheet.Cells(NomR, NomC + 7 * self.lenProcIS + 14).value = 'MinOpt'
            sheet.Cells(NomR, NomC + 7 * self.lenProcIS + 15).value = 'MaxOpt'
            NomC = NomC + 7 * self.lenProcIS + 18
            j = j + 1
        #i = 0
        #while i < KolElNomElGraphTree:
        #    sheet.Cells(NomR, 34 + i + 7 * self.lenProcIS + 11).value = 'LevelGT ' + str(i)
        #    i = i + 1



        #i = 0
        #while i < self.KolTimeDelEl:
            #sheet.Cells(NomR, 34 + i * 2 + 7 * self.lenProcIS + KolElNomElGraphTree + 16).value = 'M Time ' + str(i)
            #sheet.Cells(NomR, 34 + i * 2 + 1 + 7 * self.lenProcIS + KolElNomElGraphTree + 16).value = 'La2 Time ' + str(
            #    i)
            #i = i + 1

        sheet.Cells(1, 1).value = NomR + 1
        # сохраняем рабочую книгу
        wb.Save()
        # закрываем ее
        wb.Close()
        # закрываем COM объект
        Excel.Quit()

    def SaveTime(self, NomStatistics,Nom, timeDuration):
        Nom = int(int(Nom) - 1)
        self.ArrTime[NomStatistics][Nom] = self.ArrTime[NomStatistics][Nom] + timeDuration
        self.DArrTime[NomStatistics][Nom] = self.DArrTime[NomStatistics][Nom] + timeDuration * timeDuration
        return 0

    def StatIterationAntZeroGraphTree(self, KolGraphTree):
        i = 0
        while i < len(self.NomElGraphTree):
            self.NomElGraphTree[i] = self.NomElGraphTree[i] + KolGraphTree[i]
            i = i + 1

    def StatAllAntZero(self, NomStatistics,NomIteration, NomSolution):
        #print('StatAllAntZero=',self.EndAllAntZero,self.MIterAllAntZero,self.DIterAllAntZero,NomIteration,NomSolution,NomStatistics)
        if self.EndAllAntZero[NomStatistics] == 0:
            self.MIterAllAntZero[NomStatistics] = self.MIterAllAntZero[NomStatistics] + NomIteration
            self.DIterAllAntZero[NomStatistics] = self.DIterAllAntZero[NomStatistics] + NomIteration * NomIteration
            self.MSltnAllAntZero[NomStatistics] = self.MSltnAllAntZero[NomStatistics] + NomSolution
            self.DSltnAllAntZero[NomStatistics] = self.DSltnAllAntZero[NomStatistics] + NomSolution * NomSolution
            self.EndAllAntZero[NomStatistics] = 1

    def SaveTimeSocket(self, time1):
        self.MSocketTime = self.MSocketTime + time1
        self.DSocketTime = self.DSocketTime + time1 * time1
        print(self.MSocketTime)
        print('Cluster', self.MClusterTime)

    def SaveTimeCluster(self, time1):
        self.MClusterTime = self.MClusterTime + time1
        self.DClusterTime = self.DClusterTime + time1 * time1

    def ProcBestOF(self, NomStatistics, OF, MaxOptimization, NomIteration, NomSolution):
        if (OF != sys.maxsize) and (OF != -sys.maxsize):
            i = 0
            # print('ProcBestOF', NomStatistics, OF, self.ProcIS, NomIteration, NomSolution, self.KolEndIs, self.OFProc, self.EndIS)
            while i < self.lenProcIS:
                if MaxOptimization == 1:
                    if (self.BestOF - self.LowOF) * self.ProcIS[i] + self.LowOF <= OF and self.EndIS[NomStatistics][
                        i] == 0:
                        self.MOFI[NomStatistics][i] = self.MOFI[NomStatistics][i] + NomIteration
                        self.DOFI[NomStatistics][i] = self.DOFI[NomStatistics][i] + NomIteration * NomIteration
                        self.MOFS[NomStatistics][i] = self.MOFS[NomStatistics][i] + NomSolution
                        self.DOFS[NomStatistics][i] = self.DOFS[NomStatistics][i] + NomSolution * NomSolution
                        self.OFProc[NomStatistics][i] = self.OFProc[NomStatistics][i] + OF
                        self.KolEndIs[NomStatistics][i] = self.KolEndIs[NomStatistics][i] + 1
                    if (self.BestOF - self.LowOF) * self.ProcIS[i] + self.LowOF <= OF:
                        self.EndIS[NomStatistics][i] = self.EndIS[NomStatistics][i] + 1
                else:
                    if self.BestOF - (self.BestOF - self.LowOF) * self.ProcIS[i] >= OF and self.EndIS[NomStatistics][
                        i] == 0:
                        self.MOFI[NomStatistics][i] = self.MOFI[NomStatistics][i] + NomIteration
                        self.DOFI[NomStatistics][i] = self.DOFI[NomStatistics][i] + NomIteration * NomIteration
                        self.MOFS[NomStatistics][i] = self.MOFS[NomStatistics][i] + NomSolution
                        self.DOFS[NomStatistics][i] = self.DOFS[NomStatistics][i] + NomSolution * NomSolution
                        self.OFProc[NomStatistics][i] = self.OFProc[NomStatistics][i] + OF
                        self.KolEndIs[NomStatistics][i] = self.KolEndIs[NomStatistics][i] + 1
                    if self.BestOF - (self.BestOF - self.LowOF) * self.ProcIS[i] >= OF:
                        self.EndIS[NomStatistics][i] = self.EndIS[NomStatistics][i] + 1
                i = i + 1

    def SaveProcBestOF(self, OF, Proc):
        if (self.BestOF - self.LowOF) * Proc + self.LowOF <= OF:
            return 1
        else:
            return 0