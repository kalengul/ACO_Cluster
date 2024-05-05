# ACO_Cluster
This project is intended to develop modifications of the ant colony method (ACO) in Python Currently used for learning Python

To change the default settings, you need to create a file Setting.ini

Example:

[setting_global]
endprint = 0
endparametr = 1000
shagparametr = 50
typeparametr = 8
addferomonantzero = 0
sbrosgraphallantzero = 0
gonewiterationantzero = 1
gographtree = 0
koliteration = 600
kolstatiteration = 200
maxkoliterationantzero = 100
koltimedelel = 10
namefilegraph = BenchShevefeliaFunctionM.xlsx
gosavemap2 = 0
GoParallelAnt = 0
KolParallelAnt = 0


[ant]
n = 25
q = 500
ro = 0.9
kolelitagent = 0
deltzeropheromon = 1

[ParametricGraph]
alf1 = 1
alf2 = 1
alf3 = 1
koef1 = 1
koef2 = 1
koef3 = 1
typeprobability = 3
endallsolution = 1

[graph_tree]
sortpheromon = 0
horizontaltree = 0

[VirtualKlaster]
vivodklasterexcel = 0

[Stat]
lenprocis = 24
koltimedelel = 10

[Cluster]
socketkolcluster = 0
socketip = 127.0.0.1
socketport = 8080
socketclustertime = 0

