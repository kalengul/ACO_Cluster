# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 19:14:48 2022

@author: Юрий
"""
import sys

import win32com.client  # Для загрузки из Excel
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

    def __init__(self,KolPareto):
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
        self.ArrTime = []
        self.DArrTime = []

        self.lenProcIS = 8
        self.KolTimeDelEl = 10

        self.MSolution = 0
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
        self.ProcAntZero = 0
        self.SumProcAntZero = 0
        self.MTime = 0
        self.DTime = 0
        self.MSocketTime = 0
        self.DSocketTime = 0
        self.MClusterTime = 0
        self.DClusterTime = 0

        self.MIterationAntZero = 0
        self.DIterationAntZero = 0

        self.MkolParetto = 0
        self.MkolParettoElement = 0
        self.MkolCurrentParettoSearch = 0
        self.DkolCurrentParettoSearch = 0
        self.MkolCurrentParettoElement = 0
        self.MkolComparisonParetoSet = 0
        self.DkolComparisonParetoSet = 0

        self.BestOF = 0
        self.LowOF = 0
        self.ArrBestOF = []
        self.ArrLowOF = []
        j = 0
        while j < KolPareto:
            self.ArrBestOF.append(-sys.maxsize)
            self.ArrLowOF.append(sys.maxsize)
            j = j + 1
        self.StartStatistic(KolPareto)

    def load_pareto_set_excel(self,NameFile,KolPareto):
        AllParetoSet = []
        pathArrParetoSet = []
        AllSolution = 0
        NomParetoSet = 0
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(NameFile)
        sheet = wb.ActiveSheet
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

            NomParetoSet=NomParetoSet+1
            st = sheet.Cells(2 + NomParetoSet, 1).value
#TimeParetoSet	39,136248	AllParetoSet	1040	AllSolution	1960001
#-1	-2,718281828	0	-1	0	0	-1	0	0	0	0	0	-1	0	0	0	0	0	0

        # сохраняем рабочую книгу
        wb.Save()
        # закрываем ее
        wb.Close()
        # закрываем COM объект
        Excel.Quit()
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
                        sheet.Cells(2 + NomParetoSet, 1 + len(AllParetoSet[NomParetoSet]) + 2 + ElNomParetoSet).value = \
                        pathArrParetoSet[NomParetoSet][ElNomParetoSet]
                        ElNomParetoSet = ElNomParetoSet + 1
                NomParetoSet = NomParetoSet + 1
        # сохраняем рабочую книгу
        wb.Save()
        # закрываем ее
        wb.Close()
        # закрываем COM объект
        Excel.Quit()

    def SaveStatisticsExcelParetto(self, NameFile, koliter, NomC):
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(NameFile)
        sheet = wb.ActiveSheet
        NomR = sheet.Cells(1, 1).value
        sheet.Cells(NomR - 1, NomC).value = self.MkolParetto
        sheet.Cells(NomR - 1, NomC + 1).value = self.MkolParettoElement
        sheet.Cells(NomR - 1, NomC + 2).value = self.MkolCurrentParettoSearch / koliter
        sheet.Cells(NomR - 1, NomC + 3).value = self.DkolCurrentParettoSearch / koliter
        sheet.Cells(NomR - 1, NomC + 4).value = self.MkolCurrentParettoElement
        sheet.Cells(NomR - 1, NomC + 5).value = self.MkolComparisonParetoSet / koliter
        sheet.Cells(NomR - 1, NomC + 6).value = self.DkolComparisonParetoSet / koliter
        # сохраняем рабочую книгу
        wb.Save()
        # закрываем ее
        wb.Close()
        # закрываем COM объект
        Excel.Quit()

    def SaveStatisticsExcel(self, NameFile, KolAnt, KolPareto, time, koliter, OptimPath, P):
        Excel = win32com.client.Dispatch("Excel.Application")
        wb = Excel.Workbooks.Open(NameFile)
        sheet = wb.ActiveSheet
        NomR = int(sheet.Cells(1, 1).value)
        sheet.Cells(NomR, 1).value = P
        sheet.Cells(NomR, 2).value = koliter
        sheet.Cells(NomR, 3).value = KolAnt

        sheet.Cells(NomR, 4).value = OptimPath
        sheet.Cells(NomR, 5).value = self.MTime / koliter
        sheet.Cells(NomR, 6).value = self.DTime / koliter
        sheet.Cells(NomR, 7).value = '=F'+str(NomR)+'-E'+str(NomR)+'*E'+str(NomR)  #=E5-D5*D5
        sheet.Cells(NomR, 8).value = '=E' + str(NomR) + '-КОРЕНЬ(G' + str(NomR) + ')/КОРЕНЬ(B' + str(NomR)+')*$B$1' #=D5-КОРЕНЬ(F5)/КОРЕНЬ(B5)*B1
        sheet.Cells(NomR, 9).value = '=E' + str(NomR) + '+КОРЕНЬ(G' + str(NomR) + ')/КОРЕНЬ(B' + str(NomR)+')*$B$1' #=D5+КОРЕНЬ(F5)/КОРЕНЬ(B5)*B1
        sheet.Cells(NomR, 10).value = '=E' + str(NomR) + '/(A' + str(NomR) + '*C' + str(NomR)+')' #=D5/(A5*C5)
        sheet.Cells(NomR, 11).value = '=J' + str(NomR) + '-КОРЕНЬ(G' + str(NomR) + ')/КОРЕНЬ(B' + str(NomR)+')*$B$1' #=I5-КОРЕНЬ(F5)/КОРЕНЬ(B5)*$B$1
        sheet.Cells(NomR, 12).value = '=J' + str(NomR) + '+КОРЕНЬ(G' + str(NomR) + ')/КОРЕНЬ(B' + str(NomR)+')*$B$1' #=I5+КОРЕНЬ(F5)/КОРЕНЬ(B5)*$B$1
        sheet.Cells(NomR, 13).value = self.KolAllAntZero / koliter
        sheet.Cells(NomR, 14).value = self.KolAntZero / koliter
        sheet.Cells(NomR, 15).value = self.MIterationAntZero / koliter
        sheet.Cells(NomR, 16).value = self.DIterationAntZero / koliter
        sheet.Cells(NomR, 17).value = '=P' + str(NomR) + '-O' + str(NomR) + '*O' + str(NomR)  # =E5-D5*D5
        sheet.Cells(NomR, 18).value = '=O' + str(NomR) + '-КОРЕНЬ(Q' + str(NomR) + ')/КОРЕНЬ(B' + str(
            NomR) + ')*$B$1'  # =D5-КОРЕНЬ(F5)/КОРЕНЬ(B5)*B1
        sheet.Cells(NomR, 19).value = '=O' + str(NomR) + '+КОРЕНЬ(Q' + str(NomR) + ')/КОРЕНЬ(B' + str(
            NomR) + ')*$B$1'  # =D5+КОРЕНЬ(F5)/КОРЕНЬ(B5)*B1
        sheet.Cells(NomR, 20).value = self.MSolution / koliter
        sheet.Cells(NomR, 21).value = self.DSolution / koliter
        sheet.Cells(NomR, 22).value = '=U'+str(NomR)+'-T'+str(NomR)+'*T'+str(NomR)  #=E5-D5*D5
        sheet.Cells(NomR, 23).value = '=T' + str(NomR) + '-КОРЕНЬ(V' + str(NomR) + ')/КОРЕНЬ(B' + str(NomR)+')*$B$1' #=D5-КОРЕНЬ(F5)/КОРЕНЬ(B5)*B1
        sheet.Cells(NomR, 24).value = '=T' + str(NomR) + '+КОРЕНЬ(V' + str(NomR) + ')/КОРЕНЬ(B' + str(NomR)+')*$B$1' #=D5+КОРЕНЬ(F5)/КОРЕНЬ(B5)*B1
        sheet.Cells(NomR, 25).value = '=T' + str(NomR) + '/(A' + str(NomR) + '*C' + str(NomR)+')' #=D5/(A5*C5)
        sheet.Cells(NomR, 26).value = '=Y' + str(NomR) + '-КОРЕНЬ(V' + str(NomR) + ')/КОРЕНЬ(B' + str(NomR)+')*$B$1' #=I5-КОРЕНЬ(F5)/КОРЕНЬ(B5)*$B$1
        sheet.Cells(NomR, 27).value = '=Y' + str(NomR) + '+КОРЕНЬ(V' + str(NomR) + ')/КОРЕНЬ(B' + str(NomR)+')*$B$1' #=I5+КОРЕНЬ(F5)/КОРЕНЬ(B5)*$B$1
        sheet.Cells(NomR, 28).value = self.MIter / koliter
        sheet.Cells(NomR, 29).value = self.DIter / koliter

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
                if self.ArrKolEndIs[j][i] != 0:
                    sheet.Cells(NomR, NomC + j * 2).value = self.ArrMOFI[j][i] / self.ArrKolEndIs[j][i]
                    sheet.Cells(NomR, NomC + j * 2 + 1).value = self.ArrDOFI[j][i] / self.ArrKolEndIs[j][i]
                    sheet.Cells(NomR, NomC + j * 2 + 2 * self.lenProcIS + 4).value = self.ArrMOFS[j][i] / self.ArrKolEndIs[j][i]
                    sheet.Cells(NomR, NomC + j * 2 + 1 + 2 * self.lenProcIS + 4).value = self.ArrDOFS[j][i] / self.ArrKolEndIs[j][i]
                    sheet.Cells(NomR, NomC + j + 4 * self.lenProcIS + 9).value = self.ArrKolEndIs[j][i] / koliter
                    sheet.Cells(NomR, NomC + j + 5 * self.lenProcIS + 10).value = self.ArrOFProc[j][i] / self.ArrKolEndIs[j][i]
                    sheet.Cells(NomR, NomC + j + 6 * self.lenProcIS + 11).value = self.ArrMEndIs[j][i] / self.ArrKolEndIs[j][i]
                j = j + 1
                sheet.Cells(NomR, NomC + 4 * self.lenProcIS + 4).value = '=BO' + str(NomR) + '-BN' + str(NomR) + '*BN' + str(NomR)  # =E5-D5*D5
                sheet.Cells(NomR, NomC + 4 * self.lenProcIS + 5).value = '=BN' + str(NomR) + '-КОРЕНЬ(BP' + str(NomR) + ')/КОРЕНЬ(B' + str(
                    NomR) + ')*$B$1'  # =D5-КОРЕНЬ(F5)/КОРЕНЬ(B5)*B1
                sheet.Cells(NomR, NomC + 4 * self.lenProcIS + 6).value = '=BN' + str(NomR) + '+КОРЕНЬ(BP' + str(NomR) + ')/КОРЕНЬ(B' + str(
                    NomR) + ')*$B$1'  # =D5+КОРЕНЬ(F5)/КОРЕНЬ(B5)*B1
            NomC = NomC  + 7 * self.lenProcIS + 15
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

        sheet.Cells(1, 1).value = NomR + 1
        # сохраняем рабочую книгу
        wb.Save()
        # закрываем ее
        wb.Close()
        # закрываем COM объект
        Excel.Quit()

    def SaveProcBestOF(self, OF, Proc):
        if (self.BestOF - self.LowOF) * Proc + self.LowOF <= OF:
            return 1
        else:
            return 0

    def SaveTime(self, Nom, timeDuration):
        Nom = int(Nom) - 1
        self.ArrTime[Nom] = self.ArrTime[Nom] + timeDuration
        self.DArrTime[Nom] = self.DArrTime[Nom] + timeDuration * timeDuration
        return 0

    def SaveTimeIteration(self, time1):
        self.MTime = self.MTime + time1
        self.DTime = self.DTime + time1 * time1

    def SaveTimeSocket(self, time1):
        self.MSocketTime = self.MSocketTime + time1
        self.DSocketTime = self.DSocketTime + time1 * time1
        print(self.MSocketTime)
        print('Cluster', self.MClusterTime)

    def SaveTimeCluster(self, time1):
        self.MClusterTime = self.MClusterTime + time1
        self.DClusterTime = self.DClusterTime + time1 * time1

    def StatIterationAntZero(self, NomIteration):
        self.MIterationAntZero = self.MIterationAntZero + NomIteration
        self.DIterationAntZero = self.DIterationAntZero + NomIteration*NomIteration


    def StatIterationAntZeroGraphTree(self, KolGraphTree):
        i = 0
        while i < len(self.NomElGraphTree):
            self.NomElGraphTree[i] = self.NomElGraphTree[i] + KolGraphTree[i]
            i = i + 1

    def StatAllAntZero(self, NomIteration, NomSolution):
        if self.EndAllAntZero == 0:
            self.MIterAllAntZero = self.MIterAllAntZero + NomIteration
            self.DIterAllAntZero = self.DIterAllAntZero + NomIteration * NomIteration
            self.MSltnAllAntZero = self.MSltnAllAntZero + NomSolution
            self.DSltnAllAntZero = self.DSltnAllAntZero + NomSolution * NomSolution
            self.EndAllAntZero = 1

    def StatParettoSet(self, kolParetto, kolParettoElement, CurrentParettoSearch, kolCurrentParettoElement,
                       ComparisonParetoSet):
        self.MkolParetto = kolParetto
        self.MkolParettoElement = kolParettoElement
        # print(self.MkolCurrentParettoSearch, self.DkolCurrentParettoSearch)
        self.MkolCurrentParettoSearch = self.MkolCurrentParettoSearch + CurrentParettoSearch
        self.DkolCurrentParettoSearch = self.DkolCurrentParettoSearch + CurrentParettoSearch * CurrentParettoSearch
        # print(self.MkolCurrentParettoSearch, self.DkolCurrentParettoSearch)
        self.MkolCurrentParettoElement = kolCurrentParettoElement
        self.MkolComparisonParetoSet = self.MkolComparisonParetoSet + len(ComparisonParetoSet)
        self.DkolComparisonParetoSet = self.DkolComparisonParetoSet + len(ComparisonParetoSet) * len(
            ComparisonParetoSet)

    def EndStatistik(self, NomIteration, NomSolution):
        self.MSolution = self.MSolution + NomSolution
        self.DSolution = self.DSolution + NomSolution * NomSolution
        self.MIter = self.MIter + NomIteration
        self.DIter = self.DIter + NomIteration * NomIteration
        self.SumProcAntZero = self.SumProcAntZero + self.ProcAntZero / NomIteration
        i = 0
        while i < self.lenProcIS:
            self.MEndIs[i] = self.MEndIs[i] + self.EndIS[i]
            i = i + 1

    def ProcBestOFArray(self, OF, NomArr, MaxOptimization, NomIteration, NomSolution):
        i = 0
        #print(self.ArrBestOF,self.ArrLowOF,self.ArrEndIS, self.ArrMOFI)
        while i < self.lenProcIS:
            if MaxOptimization == 1:
                if (self.ArrBestOF[NomArr] - self.ArrLowOF[NomArr]) * self.ProcIS[i] + self.ArrLowOF[NomArr] <= OF and \
                        self.ArrEndIS[i][NomArr]== 0:
                    self.ArrMOFI[i][NomArr] = self.ArrMOFI[i][NomArr] + NomIteration
                    self.ArrDOFI[i][NomArr] = self.ArrDOFI[i][NomArr] + NomIteration * NomIteration
                    self.ArrMOFS[i][NomArr] = self.ArrMOFS[i][NomArr] + NomSolution
                    self.ArrDOFS[i][NomArr] = self.ArrDOFS[i][NomArr] + NomSolution * NomSolution
                    self.ArrOFProc[i][NomArr] = self.ArrOFProc[i][NomArr] + OF
                    self.ArrKolEndIs[i][NomArr] = self.ArrKolEndIs[i][NomArr] + 1
                if (self.ArrBestOF[NomArr] - self.ArrLowOF[NomArr]) * self.ProcIS[i] + self.ArrLowOF[NomArr] <= OF:
                    self.ArrEndIS[i][NomArr] = self.ArrEndIS[i][NomArr] + 1
            else:
                if self.ArrBestOF[NomArr] - (self.ArrBestOF[NomArr] - self.ArrLowOF[NomArr]) * self.ProcIS[i] >= OF and self.ArrEndIS[i][NomArr] == 0:
                    self.ArrMOFI[i][NomArr] = self.ArrMOFI[i][NomArr] + NomIteration
                    self.ArrDOFI[i][NomArr] = self.ArrDOFI[i][NomArr] + NomIteration * NomIteration
                    self.ArrMOFS[i][NomArr] = self.ArrMOFS[i][NomArr] + NomSolution
                    self.ArrDOFS[i][NomArr] = self.ArrDOFS[i][NomArr] + NomSolution * NomSolution
                    self.ArrOFProc[i][NomArr] = self.ArrOFProc[i][NomArr] + OF
                    self.ArrKolEndIs[i][NomArr] = self.ArrKolEndIs[i][NomArr] + 1
                if self.ArrBestOF[NomArr] - (self.ArrBestOF[NomArr] - self.ArrLowOF[NomArr]) * self.ProcIS[i] >= OF:
                    self.ArrEndIS[i][NomArr] = self.ArrEndIS[i][NomArr] + 1
            i = i + 1

    def ProcBestOF(self, OF, MaxOptimization, NomIteration, NomSolution):
        i = 0
        while i < self.lenProcIS:
            if MaxOptimization == 1:
                if (self.BestOF - self.LowOF) * self.ProcIS[i] + self.LowOF <= OF and self.EndIS[i] == 0:
                    self.MOFI[i] = self.MOFI[i] + NomIteration
                    self.DOFI[i] = self.DOFI[i] + NomIteration * NomIteration
                    self.MOFS[i] = self.MOFS[i] + NomSolution
                    self.DOFS[i] = self.DOFS[i] + NomSolution * NomSolution
                    self.OFProc[i] = self.OFProc[i] + OF
                    self.KolEndIs[i] = self.KolEndIs[i] + 1
                if (self.BestOF - self.LowOF) * self.ProcIS[i] + self.LowOF <= OF:
                    self.EndIS[i] = self.EndIS[i] + 1
            else:
                if self.BestOF - (self.BestOF - self.LowOF) * self.ProcIS[i] >= OF and self.EndIS[i] == 0:
                    self.MOFI[i] = self.MOFI[i] + NomIteration
                    self.DOFI[i] = self.DOFI[i] + NomIteration * NomIteration
                    self.MOFS[i] = self.MOFS[i] + NomSolution
                    self.DOFS[i] = self.DOFS[i] + NomSolution * NomSolution
                    self.OFProc[i] = self.OFProc[i] + OF
                    self.KolEndIs[i] = self.KolEndIs[i] + 1
                if self.BestOF - (self.BestOF - self.LowOF) * self.ProcIS[i] >= OF:
                    self.EndIS[i] = self.EndIS[i] + 1
            i = i + 1

    def SbrosStatistic(self,KolPareto):
        self.EndIS.clear()
        self.EndAllAntZero = 0
        i = 0
        while i < self.lenProcIS:
            self.EndIS.append(0)
            i = i + 1
        self.ArrEndIS.clear()
        i = 0
        while i < self.lenProcIS:
            self.ArrEndIS.append([])
            j = 0
            while j < KolPareto:
                self.ArrEndIS[i].append(0)
                j=j+1
            i = i + 1


    def StartStatisticGrahTree(self, KolEl):
        self.NomElGraphTree.clear()
        i = 0
        while i < KolEl:
            self.NomElGraphTree.append(0)
            i = i + 1

    def StartStatistic(self, KolPareto):

        self.MSolution = 0
        self.DSolution = 0
        self.MIter = 0
        self.DIter = 0
        self.MIterAllAntZero = 0
        self.DIterAllAntZero = 0
        self.MSltnAllAntZero = 0
        self.DSltnAllAntZero = 0
        self.KolAllAntZero = 0
        self.KolAntZero = 0
        self.ProcAntZero = 0
        self.SumProcAntZero = 0
        self.MIterationAntZero = 0
        self.DIterationAntZero = 0
        self.MTime = 0
        self.DTime = 0
        self.MkolParetto = 0
        self.MkolParettoElement = 0
        self.MkolCurrentParettoSearch = 0
        self.DkolCurrentParettoSearch = 0
        self.MkolCurrentParettoElement = 0
        self.MkolComparisonParetoSet = 0
        self.DkolComparisonParetoSet = 0
        self.EndIS.clear()
        self.MOFI.clear()
        self.DOFI.clear()
        self.MOFS.clear()
        self.DOFS.clear()
        self.OFProc.clear()
        self.KolEndIs.clear()
        self.ArrEndIS.clear()
        self.ArrMOFI.clear()
        self.ArrDOFI.clear()
        self.ArrMOFS.clear()
        self.ArrDOFS.clear()
        self.ArrOFProc.clear()
        self.ArrKolEndIs.clear()
        self.ArrTime.clear()
        self.ArrMEndIs.clear()
        self.EndAllAntZero = 0
        i = 0
        while i < self.lenProcIS:
            self.EndIS.append(0)
            self.MOFI.append(0)
            self.DOFI.append(0)
            self.MOFS.append(0)
            self.DOFS.append(0)
            self.OFProc.append(0)
            self.KolEndIs.append(0)
            self.MEndIs.append(0)
            self.ArrEndIS.append([])
            self.ArrMOFI.append([])
            self.ArrDOFI.append([])
            self.ArrMOFS.append([])
            self.ArrDOFS.append([])
            self.ArrOFProc.append([])
            self.ArrKolEndIs.append([])
            self.ArrMEndIs.append([])
            j = 0
            while j < KolPareto:
                self.ArrEndIS[i].append(0)
                self.ArrMOFI[i].append(0)
                self.ArrDOFI[i].append(0)
                self.ArrMOFS[i].append(0)
                self.ArrDOFS[i].append(0)
                self.ArrOFProc[i].append(0)
                self.ArrKolEndIs[i].append(0)
                self.ArrMEndIs[i].append(0)
                j=j+1
            i = i + 1
        i = 0
        while i < self.KolTimeDelEl:
            self.ArrTime.append(0.0)
            self.DArrTime.append(0.0)
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
            NomC=NomC + 7 * self.lenProcIS + 15
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
