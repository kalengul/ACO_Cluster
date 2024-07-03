import sys

import VirtualKlaster
import GoTime
import Stat

AllParetoSet = []
pathArrParetoSet = []
AllSolution=0

def update_pareto_set(AllParetoSet,AllSolution,pathArrParetoSet, pathArr, ArrOf):
    AddParetoSet = True
    AllSolution=AllSolution+1
    NomParettoSet = 0
    while (NomParettoSet<len(AllParetoSet)) and (AddParetoSet):
        # Сравнение двух массивов
        if all(x <= y for x, y in zip(ArrOf, AllParetoSet[NomParettoSet])):
            AddParetoSet = False
        if all(x > y for x, y in zip(ArrOf, AllParetoSet[NomParettoSet])):
            del AllParetoSet[NomParettoSet]
            if pathArrParetoSet!=None:
                del pathArrParetoSet[NomParettoSet]
            NomParettoSet = NomParettoSet - 1
            #print(AllParetoSet)
        NomParettoSet=NomParettoSet+1
    if AddParetoSet:
        AllParetoSet.append(ArrOf)
        if pathArrParetoSet != None:
            pathArrParetoSet.append(pathArr)
    return AllParetoSet,AllSolution

def CreateAllParetoSet(ParametricGraph, TypeKlaster, TypeProbability,Stat,NameFile,lock_excel):
    global AllParetoSet
    global pathArrParetoSet
    global AllSolution
    global TimeParetoSet
    StartTime=GoTime.now()
    FirstPath = []
    NomNodePath = []
    NomPar = 0
    BestOF=-sys.maxsize
    LowOf=sys.maxsize
    while NomPar < len(ParametricGraph):
        FirstPath.append(ParametricGraph[NomPar].node[0].val)
        NomNodePath.append(0)
        NomPar = NomPar + 1
    SocketClusterTime = 0
    OF, ArrOf = VirtualKlaster.GetObjectivFunction(FirstPath, TypeKlaster, SocketClusterTime, TypeProbability)
    #Проверка вхождения ArrOf в AllParetoSet
    AllParetoSet,AllSolution = update_pareto_set(AllParetoSet,AllSolution,pathArrParetoSet, FirstPath, ArrOf)
    NomPar = 0
    while NomPar < len(ParametricGraph):
        NomNodePath[NomPar]=NomNodePath[NomPar]+1
        EndNomNodePath=False
        while (NomPar < len(ParametricGraph)) and (NomNodePath[NomPar]>len(ParametricGraph[NomPar].node)-1):
            NomNodePath[NomPar]=0
            NomPar=NomPar+1
            if NomPar < len(ParametricGraph):
                NomNodePath[NomPar]=NomNodePath[NomPar]+1
                if NomPar >= len(ParametricGraph) - 4:
                    print(GoTime.now(),'len(AllParetoSet)=', len(AllParetoSet),'NomPar=', NomPar, 'NomNodePath=', NomNodePath)
                EndNomNodePath=True
            else:
                EndNomNodePath = False
                print(NomPar,NomNodePath,EndNomNodePath)
            #print('NomNodePath=',NomNodePath)
        if EndNomNodePath:
            NomPar=0

        Path = []
        NomParPath = 0
        while NomParPath < len(ParametricGraph):
            Path.append(ParametricGraph[NomParPath].node[NomNodePath[NomParPath]].val)
            NomParPath=NomParPath+1
        OF, ArrOf = VirtualKlaster.GetObjectivFunction(Path, TypeKlaster, SocketClusterTime, TypeProbability)
        j=0
        while j<len(Stat.ArrBestOF):
            if ArrOf[j]>Stat.ArrBestOF[j]:
                Stat.ArrBestOF[j] = ArrOf[j]
            if ArrOf[j]<Stat.ArrLowOF[j]:
                Stat.ArrLowOF[j] = ArrOf[j]
            j=j+1
        BestOF = -sys.maxsize
        LowOf = sys.maxsize
        #print('Path, ArrOf ', Path, ArrOf)
        # Проверка вхождения ArrOf в AllParetoSet
        AllParetoSet,AllSolution = update_pareto_set(AllParetoSet,AllSolution,pathArrParetoSet, Path, ArrOf)
        #print('AllParetoSet= ',AllParetoSet)
    TimeParetoSet=GoTime.now()-StartTime
    lock_excel.acquire()
    Stat.save_pareto_set_excel(NameFile,TimeParetoSet,AllParetoSet,pathArrParetoSet,AllSolution)
    lock_excel.release()
    print('save_all_pareto_set_excel')

def ComparisonParetoSet(ParetoSet):
    common_elements = set(map(tuple, AllParetoSet)) & set(map(tuple, ParetoSet))
    result = [list(elem) for elem in common_elements]
    return result