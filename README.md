# ACO_Cluster
This project is intended to develop modifications of the ant colony method (ACO) in Python Currently used for learning Python

To change the default settings, you need to create a file Setting.ini

Example:

[setting_global]
endprint=0
endParametr=10000
shagParametr=50
typeParametr=8
AddFeromonAntZero=1
SbrosGraphAllAntZero=0
goNewIterationAntZero=0
goGraphTree=0
KolIteration=1000
KolStatIteration=100
MaxkolIterationAntZero=10
KolTimeDelEl=10
NameFileGraph=bench4x2.xlsx 
GoSaveMap2=0
[ant]
N=25
Q=2
Ro=0.9
[ParametricGraph]
alf1=1
alf2=1
alf3=1
koef1=1
koef2=1
koef3=1
typeProbability=3
EndAllSolution=1
[graph_tree]
SortPheromon=0
HorizontalTree=0
[VirtualKlaster]
VivodKlasterExcel=0
[Stat]
lenProcIS = 24
KolTimeDelEl = 10
