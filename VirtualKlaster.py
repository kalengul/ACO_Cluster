# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:22:49 2022

@author: Юрий
"""

import math

import GoTime
import Model.SIRVD
import Model.Rosaviation.Rosaviation
import os
import win32com.client  # Для загрузки из Excel
import time
import LoadSettingsIniFile as Setting

VivodKlasterExcel = 0


def SavePathExcel(NameFile, path, OF, TypeKlaster):
    Excel = win32com.client.Dispatch("Excel.Application")
    wb = Excel.Workbooks.Open(NameFile)
    sheet = wb.ActiveSheet
    NomR = sheet.Cells(1, 1).value
    sheet.Cells(1, 2).value = TypeKlaster
    i = 1;
    while i < len(path):
        sheet.Cells(NomR, i).value = path[i - 1]
        i = i + 1
    sheet.Cells(NomR, i).value = OF
    wb.Save()
    # закрываем ее
    wb.Close()
    # закрываем COM объект
    Excel.Quit()


def Klaster1(path):
    OF = 0
    if path[0] > 3:
        OF = OF + 10
    if path[2] == 0:
        OF = OF * 5
    if path[4] == 0:
        OF = OF + 3
    return OF


def Klaster2(path):
    OF = 0
    OF = OF + path[0] - path[1] + 2 * path[2] + path[3] + 2 * path[4]
    OF = OF + 0.5 * path[5] - 0.12 * path[6] - path[7] + 80 * path[8] + 0.00001 * path[9]
    if path[10] == 'Сильное':
        OF = OF + 20
    return OF


def Klaster2o(path):
    OF = 0
    OF = OF + path[4] - path[12] + 2 * path[2] + path[3] + 2 * path[5]
    OF = OF + 0.5 * path[7] - 0.12 * path[10] - path[11] + 80 * path[0] + 0.00001 * path[6]
    if path[1] == 'Сильное':
        OF = OF + 20
    return OF


def Klaster2no(path):
    OF = 0
    OF = OF + path[8] - path[0] + 2 * path[10] + path[9] + 2 * path[7]
    OF = OF + 0.5 * path[5] - 0.12 * path[2] - path[1] + 80 * path[12] + 0.00001 * path[6]
    if path[11] == 'Сильное':
        OF = OF + 20
    return OF


def Klaster2so(path):
    OF = 0
    OF = OF + path[5] - path[4] + 2 * path[7] + path[12] + 2 * path[3]
    OF = OF + 0.5 * path[9] - 0.12 * path[6] - path[8] + 80 * path[10] + 0.00001 * path[11]
    if path[1] == 'Сильное':
        OF = OF + 20
    return OF


def Klaster2nso(path):
    OF = 0
    OF = OF + path[12 - 5] - path[12 - 4] + 2 * path[12 - 7] + path[12 - 12] + 2 * path[12 - 3]
    OF = OF + 0.5 * path[12 - 9] - 0.12 * path[12 - 6] - path[12 - 8] + 80 * path[12 - 10] + 0.00001 * path[12 - 11]
    if path[12 - 1] == 'Сильное':
        OF = OF + 20
    return OF


def Klaster3(path):
    OF = 0
    OF = OF + (path[0] - 4) * (path[0] - 4) + math.cos(path[1]) + math.cos(math.exp(path[2])) + (path[3] - 10) * (
                path[3] - 10) + 2 * path[4]
    OF = OF + 0.5 * path[5] - 0.12 * path[6] - path[7] + 80 * path[8] + 0.00001 * path[9]
    OF = OF * 15
    if path[10] == 'Сильное':
        OF = OF + 20
    return OF


def Bench4(path):
    a1 = path[0] ** 2
    a2 = path[1] ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(path[0]) * math.cos(path[1]) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench4x(path):
    p0 = path[0] + path[1]
    p1 = path[2] + path[3]
    a1 = p0 ** 2
    a2 = p1 ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(p0) * math.cos(p1) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench4x1(path):
    p0 = path[0] * path[1]
    p1 = path[2] * path[3]
    a1 = p0 ** 2
    a2 = p1 ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(p0) * math.cos(p1) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench4x2(path):
    p0 = path[0] * (path[1] + path[2])
    p1 = path[3] * (path[4] + path[5])
    a1 = p0 ** 2
    a2 = p1 ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(p0) * math.cos(p1) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench4x3(path):
    p0 = path[0] * (path[1] + path[2] + path[3])
    p1 = path[4] * (path[5] + path[6] + path[7])
    a1 = p0 ** 2
    a2 = p1 ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(p0) * math.cos(p1) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench4x4(path):
    p0 = path[0] * (path[1] + path[2] + path[3] + path[4])
    p1 = path[5] * (path[6] + path[7] + path[8] + path[9])
    a1 = p0 ** 2
    a2 = p1 ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(p0) * math.cos(p1) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench4x22(path):
    p0 = path[0] * (path[1] + path[2] + path[3])
    p1 = path[4] * (path[5] + path[6] + path[7])
    a1 = p0 ** 2
    a2 = p1 ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(p0) * math.cos(p1) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench4x222(path):
    p0 = path[0] * (path[1] + path[2] + path[3] + path[4])
    p1 = path[5] * (path[6] + path[7] + path[8] + path[9])
    a1 = p0 ** 2
    a2 = p1 ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(p0) * math.cos(p1) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench4x2222(path):
    p0 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5])
    p1 = path[6] * (path[7] + path[8] + path[9] + path[10] + path[11])
    a1 = p0 ** 2
    a2 = p1 ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(p0) * math.cos(p1) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench4xo2222(path):
    p0 = path[10] * (path[8] + path[6] + path[4] + path[2] + path[0])
    p1 = path[11] * (path[9] + path[7] + path[5] + path[3] + path[1])
    a1 = p0 ** 2
    a2 = p1 ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.cos(p0) * math.cos(p1) * math.exp((math.fabs(a)))) ** 2
    return OF


def Bench1(path):
    a1 = path[0] ** 2
    a2 = path[1] ** 2
    a = (a1 + a2) / 200
    OF = 4 * math.fabs(math.sin(path[0]) * math.cos(path[1]) * math.exp(math.fabs(math.cos(a))))
    return OF


def Bench1m(path):
    a1 = path[0] ** 2
    a2 = path[1] ** 2
    a = (a1 + a2) / 200
    OF = -4 * math.fabs(math.sin(path[0]) * math.cos(path[1]) * math.exp(math.fabs(math.cos(a))))
    return OF


def Bench3m(path):
    a1 = path[0] ** 2
    a2 = path[1] ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = -math.fabs(math.cos(path[0]) * math.cos(path[1]) * math.exp(math.fabs(math.cos(a))))
    return OF


def Bench4m(path):
    a1 = path[0] ** 2
    a2 = path[1] ** 2
    a = 1 - (a1 + a2) ** 0.5 / math.pi
    OF = -((math.cos(path[0]) * math.cos(path[1]) * math.exp((math.fabs(a)))) ** 2) / 30
    return OF


def Bench5m(path):
    a1 = path[0] ** 2
    a2 = path[1] ** 2
    a = 100 - (a1 + a2) ** 0.5 / math.pi
    OF = -0.0001 * (math.fabs(math.sin(path[0]) * math.sin(path[1]) * math.exp((math.fabs(a)))) + 1) ** 0.1
    return OF


def Bench6m(path):
    a1 = path[0] ** 2
    a2 = path[1] ** 2
    a = 100 - (a1 + a2) ** 0.5 / math.pi
    OF = 0.0001 * (math.fabs(math.sin(path[0]) * math.sin(path[1]) * math.exp((math.fabs(a)))) + 1) ** 0.1
    return OF


def Bench7m(path):
    a1 = path[0] ** 2
    a2 = path[1] ** 2
    a = 100 - (a1 + a2) ** 0.5 / math.pi
    OF = (math.fabs(math.sin(path[0]) * math.sin(path[1]) * math.exp((math.fabs(a)))) + 1) ** -0.1
    return OF


def Bench8m(path):
    a1 = path[0] ** 2
    a2 = path[1] ** 2
    a = 100 - (a1 + a2) ** 0.5 / math.pi
    OF = -(math.fabs(math.sin(path[0]) * math.sin(path[1]) * math.exp((math.fabs(a)))) + 1) ** -0.1
    return OF


def Bench10(path):
    a1 = math.sin(path[0]) * math.exp((1 - math.cos(path[1])) ** 2)
    a2 = math.cos(path[1]) * math.exp((1 - math.sin(path[0])) ** 2)
    a = a1 + a2
    OF = a + (path[0] - path[1]) ** 2
    return OF


def BenchRozenbrok(path):
    alf = 100
    OF = -alf * (path[1] - path[0] * path[0]) * (path[1] - path[0] * path[0]) - (1 - path[0]) * (1 - path[0]) + 2500
    return OF


def BenchRozenbrokO(path):
    alf = 100
    OF = -alf * (path[1] - path[0] * path[0]) * (path[1] - path[0] * path[0]) - (1 - path[0]) * (1 - path[0])
    return OF


def BenchRozenbrokM(path):
    alf = 100
    OF = abs(-alf * (path[1] - path[0] * path[0]) * (path[1] - path[0] * path[0]) - (1 - path[0]) * (1 - path[0]))
    return OF


def BenchMultiFunction(path):
    OF = path[0] * math.sin(4 * math.pi * path[0]) + path[1] * math.sin(4 * math.pi * path[1]) + 5
    return OF


def BenchMultiFunctionO(path):
    OF = path[0] * math.sin(4 * math.pi * path[0]) + path[1] * math.sin(4 * math.pi * path[1])
    return OF


def BenchMultiFunctionM(path):
    OF = abs(path[0] * math.sin(4 * math.pi * path[0]) + path[1] * math.sin(4 * math.pi * path[1]))
    return OF


def BenchBirdFunction(path):
    OF = -math.sin(path[0]) * math.exp((1 - math.cos(path[1])) * (1 - math.cos(path[1]))) - math.cos(
        path[1]) * math.exp((1 - math.sin(path[0])) * (1 - math.sin(path[0]))) - (path[0] - path[1]) * (
                     path[0] - path[1])
    return OF


def BenchShevefeliaFunction(path):
    OF = -abs(path[0]) - abs(path[1]) - abs(path[0]) * abs(path[1]) + 120
    return OF


def BenchShevefeliaFunctionO(path):
    OF = -abs(path[0]) - abs(path[1]) - abs(path[0]) * abs(path[1])
    return OF


def BenchShevefeliaFunctionM(path):
    OF = abs(-abs(path[0]) - abs(path[1]) - abs(path[0]) * abs(path[1]))
    return OF


def BenchRozenbrokx10(path):
    alf = 100
    x1 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5])
    x2 = path[6] * (path[7] + path[8] + path[9] + path[10] + path[11])
    OF = -alf * (x2 - x1 * x1) * (x2 - x1 * x1) - (1 - x1) * (1 - x1) + 2500
    return OF


def BenchMultiFunctionx10(path):
    x1 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5])
    x2 = path[6] * (path[7] + path[8] + path[9] + path[10] + path[11])
    OF = x1 * math.sin(4 * math.pi * x1) + x2 * math.sin(4 * math.pi * x2) + 5
    return OF


def BenchShafferaFunctionx10(path):
    x1 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5] + path[6])
    x2 = path[7] * (path[8] + path[9] + path[10] + path[11] + path[12] + path[13])
    OF = 1 / 2 - (math.sin(math.sqrt(x1 * x1 + x2 * x2)) * math.sin(math.sqrt(x1 * x1 + x2 * x2)) - 0.5) / (
                1 + 0.001 * (x1 * x1 + x2 * x2))
    return OF


def BenchKornFunctionx10(path):
    x1 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5])
    x2 = path[6] * (path[7] + path[8] + path[9] + path[10] + path[11])
    z = complex(x1, x2)
    OF = 1 / (1 + abs(pow(z, 6) - 1))
    return OF


def BenchRastriginFunctionx10(path):
    i0=0
    i1=6
    x1 = path[i0] * (path[i0+1] + path[i0+2] + path[i0+3] + path[i0+4] + path[i0+5])
    x2 = path[i1] * (path[i1+1] + path[i1+2] + path[i1+3] + path[i1+4] + path[i1+5])
    OF = -20 + (10 * math.cos(2 * math.pi * x1) - x1 * x1) + (10 * math.cos(2 * math.pi * x2) - x2 * x2)
    return OF


def BenchBirdFunctionx10(path):
    x1 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5])
    x2 = path[6] * (path[7] + path[8] + path[9] + path[10] + path[11])
    OF = -math.sin(x1) * math.exp(pow(1 - math.cos(x2), 2)) - math.cos(x2) * math.exp(pow(1 - math.sin(x1), 2)) - pow(
        x1 - x2, 2)
    return OF


def BenchEkliFunctionx10(path):
    x1 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5] + path[6])
    x2 = path[7] * (path[8] + path[9] + path[10] + path[11] + path[12] + path[13])
    OF = -math.e + 20 * math.exp(-math.sqrt((pow(x1, 2) + pow(x2, 2)) / 50)) + math.exp(
        1 / 2 * (math.cos(2 * math.pi * x1) + math.cos(2 * math.pi * x2)))
    return OF


def BenchRozenbrokxPareto(path):
    alf = 100
    i0=0
    i1=int(len(path)/2)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i0+i+1]
        i=i+1
    x1 = path[i0] * (sum)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i1+i+1]
        i=i+1
    x2 = path[i1] * (sum)
    OF = -alf * (x2 - x1 * x1) * (x2 - x1 * x1) - (1 - x1) * (1 - x1)
    return OF


def BenchMultiFunctionPareto(path):
    i0=0
    i1=int(len(path)/2)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i0+i+1]
        i=i+1
    x1 = path[i0] * (sum)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i1+i+1]
        i=i+1
    x2 = path[i1] * (sum)
    OF = x1 * math.sin(4 * math.pi * x1) + x2 * math.sin(4 * math.pi * x2)
    return OF


def BenchShafferaFunctionPareto(path):
    i0=0
    i1=int(len(path)/2)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i0+i+1]
        i=i+1
    x1 = path[i0] * (sum)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i1+i+1]
        i=i+1
    x2 = path[i1] * (sum)
    OF = 1 / 2 - (math.sin(math.sqrt(x1 * x1 + x2 * x2)) * math.sin(math.sqrt(x1 * x1 + x2 * x2)) - 0.5) / (
                1 + 0.001 * (x1 * x1 + x2 * x2))
    return OF


def BenchKornFunctionPareto(path):
    i0=0
    i1=int(len(path)/2)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i0+i+1]
        i=i+1
    x1 = path[i0] * (sum)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i1+i+1]
        i=i+1
    x2 = path[i1] * (sum)
    z = complex(x1, x2)
    OF = 1 / (1 + abs(pow(z, 6) - 1))
    return OF


def BenchRastriginFunctionPareto(path):
    i0=0
    i1=int(len(path)/2)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i0+i+1]
        i=i+1
    x1 = path[i0] * (sum)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i1+i+1]
        i=i+1
    x2 = path[i1] * (sum)
    OF = -20 + (10 * math.cos(2 * math.pi * x1) - x1 * x1) + (10 * math.cos(2 * math.pi * x2) - x2 * x2)
    return OF


def BenchBirdFunctionPareto(path):
    i0=0
    i1=int(len(path)/2)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i0+i+1]
        i=i+1
    x1 = path[i0] * (sum)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i1+i+1]
        i=i+1
    x2 = path[i1] * (sum)
    OF = -math.sin(x1) * math.exp(pow(1 - math.cos(x2), 2)) - math.cos(x2) * math.exp(pow(1 - math.sin(x1), 2)) - pow(
        x1 - x2, 2)
    return OF


def BenchEkliFunctionPareto(path):
    i0=0
    i1=int(len(path)/2)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i0+i+1]
        i=i+1
    x1 = path[i0] * (sum)
    sum=0
    i=0
    while i<i1-2:
        sum=sum+path[i1+i+1]
        i=i+1
    x2 = path[i1] * (sum)
    OF = -math.e + 20 * math.exp(-math.sqrt((pow(x1, 2) + pow(x2, 2)) / 50)) + math.exp(
        1 / 2 * (math.cos(2 * math.pi * x1) + math.cos(2 * math.pi * x2)))
    return OF


def SIRVD1(path):
    Model.SIRVD.Susceptible = 107137780
    Model.SIRVD.Infected = 3609122
    Model.SIRVD.Recovered = 9192702
    Model.SIRVD.Vaccinated = 25132827
    Model.SIRVD.Dead = 30313
    Model.SIRVD.beta = path[0]
    Model.SIRVD.gamma = path[1]
    Model.SIRVD.alpha = path[2]
    Model.SIRVD.sigma = path[3]
    Model.SIRVD.delta = path[4]
    i = 0
    OF = 0
    while i <= 5:
        Model.SIRVD.start_next()
        OF = OF + Model.SIRVD.go_OF_Excel_File(os.getcwd() + '/' + 'SIRVD.xlsx', i)
        i = i + 1
    OF = ((10000000000 - OF) / 1000000000 - 9.9) * 10
    # print(OF)
    return OF


def SIRVD2(path):
    Model.SIRVD.Susceptible = path[0]
    Model.SIRVD.Infected = path[1]
    Model.SIRVD.Recovered = path[2]
    Model.SIRVD.Vaccinated = path[3]
    Model.SIRVD.Dead = path[4]
    Model.SIRVD.beta = path[5]
    Model.SIRVD.gamma = path[6]
    Model.SIRVD.alpha = path[7]
    Model.SIRVD.sigma = path[8]
    Model.SIRVD.delta = path[9]
    i = 0
    OF = 0
    while i <= 5:
        Model.SIRVD.start_next()
        OF = OF + Model.SIRVD.go_OF_Excel_File(os.getcwd() + '/' + 'SIRVD.xlsx', i)
        i = i + 1
    OF = ((10000000000 - OF) / 1000000000 - 9.9) * 10
    return OF

def BenchRosaviation(TypeKlaster,path):
    if TypeKlaster==6000:
        return Model.Rosaviation.Rosaviation.goSARIMAX(path)
    elif TypeKlaster==6001:
        return Model.Rosaviation.Rosaviation.goSARIMAX_component(path)


def GetObjectivFunction(path, TypeKlaster, SocketClusterTime, TypeProbability):
    OF = 0
    ArrOf = []
    if TypeKlaster == 1:
        OF = Klaster1(path)
    elif TypeKlaster == 2:
        OF = Klaster2(path)
    elif TypeKlaster == 2001:
        OF = Klaster2o(path)
    elif TypeKlaster == 2002:
        OF = Klaster2no(path)
    elif TypeKlaster == 2003:
        OF = Klaster2so(path)
    elif TypeKlaster == 2004:
        OF = Klaster2nso(path)
    elif TypeKlaster == 3:
        OF = Klaster3(path)
    elif TypeKlaster == 401:
        OF = Bench1(path)
    elif TypeKlaster == 4019:
        OF = Bench1m(path)
    elif TypeKlaster == 404:
        OF = Bench4(path)
    elif TypeKlaster == 4049:
        OF = Bench4m(path)
    elif TypeKlaster == 4040:
        OF = Bench4x(path)
    elif TypeKlaster == 4041:
        OF = Bench4x1(path)
    elif TypeKlaster == 4042:
        OF = Bench4x2(path)
    elif TypeKlaster == 40442:
        OF = Bench4x3(path)
    elif TypeKlaster == 40443:
        OF = Bench4x4(path)
    elif TypeKlaster == 4043:
        OF = Bench4x22(path)
    elif TypeKlaster == 4044:
        OF = Bench4x222(path)
    elif TypeKlaster == 4045:
        OF = Bench4x2222(path)
    elif TypeKlaster == 40451:
        OF = Bench4xo2222(path)
    elif TypeKlaster == 410:
        OF = Bench10(path)
    elif TypeKlaster == 4109:
        OF = Bench10(path)
    elif TypeKlaster == 980:
        OF = BenchRozenbrok(path)
    elif TypeKlaster == 9801:
        OF = BenchRozenbrokO(path)
    elif TypeKlaster == 9802:
        OF = BenchRozenbrokM(path)
    elif TypeKlaster == 981:
        OF = BenchMultiFunction(path)
    elif TypeKlaster == 9811:
        OF = BenchMultiFunctionO(path)
    elif TypeKlaster == 9812:
        OF = BenchMultiFunctionM(path)
    elif TypeKlaster == 982:
        OF = BenchBirdFunction(path)
    elif TypeKlaster == 983:
        OF = BenchShevefeliaFunction(path)
    elif TypeKlaster == 9831:
        OF = BenchShevefeliaFunctionO(path)
    elif TypeKlaster == 9832:
        OF = BenchShevefeliaFunctionM(path)
    elif TypeKlaster == 9800:
        OF = BenchRozenbrokx10(path)
    elif TypeKlaster == 9810:
        OF = BenchMultiFunctionx10(path)
    elif TypeKlaster == 984:
        OF = BenchShafferaFunctionx10(path)
    elif TypeKlaster == 985:
        OF = BenchKornFunctionx10(path)
    elif TypeKlaster == 986:
        OF = BenchRastriginFunctionx10(path)
    elif TypeKlaster == 987:
        OF = BenchBirdFunctionx10(path)
    elif TypeKlaster == 988:
        OF = BenchEkliFunctionx10(path)
    elif TypeKlaster == 990:
        OF = SIRVD1(path)
    elif TypeKlaster == 991:
        OF = SIRVD2(path)
    elif TypeKlaster == 5000:
        # OF = BenchRastriginFunctionx10(path)
        ArrOf.append(BenchRozenbrokxPareto(path))
        ArrOf.append(BenchBirdFunctionPareto(path))
        ArrOf.append(BenchRastriginFunctionPareto(path))
        ArrOf.append(BenchEkliFunctionPareto(path))
        #ArrOf.append(BenchKornFunctionPareto(path))
        if (TypeProbability==6) or (TypeProbability==7):
            OF = ArrOf[0]
        else:
            OF=ArrOf[TypeProbability]
    elif (TypeKlaster == 5001) or (TypeKlaster == 5005):
        ArrOf.append(BenchRozenbrokxPareto(path))
        ArrOf.append(BenchBirdFunctionPareto(path))
        ArrOf.append(BenchRastriginFunctionPareto(path))
        ArrOf.append(BenchEkliFunctionPareto(path))
        #ArrOf.append(BenchKornFunctionPareto(path))
        if (TypeProbability==6) or (TypeProbability==7):
            OF = ArrOf[0]
        else:
            OF=ArrOf[TypeProbability]
    elif (TypeKlaster >= 6000) and (TypeKlaster <= 6010):
        #Start_Rosaviation_time=GoTime.now()
        AllOf=BenchRosaviation(TypeKlaster,path)
        #print(GoTime.now(),GoTime.now()-Start_Rosaviation_time,path,AllOf)
        i=0
        while i<len(AllOf):
            ArrOf.append(AllOf[i])
            i=i+1
        OF = ArrOf[0]
    # print(OF, path,TypeKlaster)
    if VivodKlasterExcel == 1:
        SavePathExcel('Cluster.xlsx', path, OF, TypeKlaster)
    #    print(SocketClusterTime)
    # time.sleep(SocketClusterTime/1000)
    if OF == 0:
        OF = 0.1 ** 100

    return OF, ArrOf


def GoMin(TypeKlaster):
    path = []
    MinOF = 100000
    path.append(-10)
    path.append(-10)
    while path[0] < 10:
        path[1] = -10
        while path[1] < 10:
            OF = GetObjectivFunction(path, TypeKlaster)
            # print(path,OF,GetObjectivFunction(path,TypeKlaster))
            if OF < MinOF:
                MinOF = OF
                MinPath = path
                print('Min', MinPath, MinOF)
            path[1] = path[1] + 0.1
        path[0] = path[0] + 0.1


def GoMax(TypeKlaster):
    path = []
    MaxPath = []
    MaxOF = -100000
    path.append(-10)
    path.append(-10)
    while path[0] < 10:
        path[1] = -10
        while path[1] < 10:
            OF = GetObjectivFunction(path, TypeKlaster)
            # print(path,OF,GetObjectivFunction(path,TypeKlaster))
            if OF > MaxOF:
                MaxOF = OF
                MaxPath = path
                print('Max', MaxPath, MaxOF)
            path[1] = path[1] + 0.1
        path[0] = path[0] + 0.1
