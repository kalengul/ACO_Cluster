# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 23:29:04 2022

@author: Титов Юрий
"""

SusceptibleF = []
InfectedF = []
RecoveredF = []
VaccinatedF = []
DeadF = []

SusceptibleF.append(107137780)
SusceptibleF.append(107000190)
SusceptibleF.append(106819739)
SusceptibleF.append(106634119)
SusceptibleF.append(106491671)
SusceptibleF.append(106351399)
SusceptibleF.append(106180944)

InfectedF.append(3609122)
InfectedF.append(3640052)
InfectedF.append(3696059)
InfectedF.append(3757776)
InfectedF.append(3807447)
InfectedF.append(3851048)
InfectedF.append(3915732)

RecoveredF.append(9192702)
RecoveredF.append(9246970)
RecoveredF.append(9336268)
RecoveredF.append(9432946)
RecoveredF.append(9509850)
RecoveredF.append(9579340)
RecoveredF.append(9677529)

VaccinatedF.append(25132837)
VaccinatedF.append(25185134)
VaccinatedF.append(25220178)
VaccinatedF.append(25247278)
VaccinatedF.append(25263039)
VaccinatedF.append(25290141)
VaccinatedF.append(25297552)

DeadF.append(30313)
DeadF.append(30408)
DeadF.append(30510)
DeadF.append(30635)
DeadF.append(30747)
DeadF.append(30826)
DeadF.append(30997)

Susceptible = 0
Infected = 0
Recovered = 0
Vaccinated = 0
Dead = 0
beta = 0
gamma = 0
alpha = 0
sigma = 0
delta = 0
epochs = 1
population =0

def go_population():
    global population
    global Susceptible
    global Infected
    global Recovered
    global Vaccinated
    global Dead
    population = Susceptible + Infected + Recovered + Vaccinated + Dead



def start_next():
  global population
  global Susceptible
  global Infected
  global Recovered
  global Vaccinated
  global Dead
  global beta
  global gamma
  global alpha
  global sigma
  global delta
  
  go_population()
  dS_dt = - (beta * Infected * Susceptible) / population + sigma * Recovered - alpha * Susceptible
  dI_dt = (beta * Infected * Susceptible) / population - gamma * Infected - delta * Infected
  dR_dt = gamma * Infected - sigma * Recovered
  dV_dt = alpha * Susceptible
  dD_dt = delta * Infected
  Susceptible=Susceptible + dS_dt
  Infected=Infected + dI_dt
  Recovered=Recovered + dR_dt
  Vaccinated=Vaccinated + dV_dt
  Dead=Dead + dD_dt
  
def go_OF_Excel_File(NameFile,NomRow):
    global population
    global Susceptible
    global Infected
    global Recovered
    global Vaccinated
    global Dead
    
    OF=abs(InfectedF[NomRow]-Infected)+abs(VaccinatedF[NomRow]-Vaccinated)+abs(DeadF[NomRow]-Dead)
    #print(OF)
    #print(beta,gamma,alpha,sigma,delta)
    #print(Susceptible,Infected,Recovered,Vaccinated,Dead,population)

    return OF