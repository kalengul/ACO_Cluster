# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 17:46:16 2022

@author: Юрий
"""
import win32com.client #Для загрузки из Excel

saveMap =[]
kolMap =[]

def CreateElMap2(NomCol,NomRow):
    global saveMap
    global kolMap
    Col=0
    print(NomCol)
    print(NomRow)
    saveMap = [0] * NomCol
    kolMap = [0] * NomCol
    while Col<NomCol:
        saveMap[Col] = [0] * NomRow
        kolMap[Col] = [0] * NomRow
        Col=Col+1
    print(saveMap)
    
def AddElMap2(ACol,ARow,OF):
    saveMap[ACol][ARow]=saveMap[ACol][ARow]+OF
    kolMap[ACol][ARow]=kolMap[ACol][ARow]+1
    
def PrintElMap2(NameFile):
   Excel = win32com.client.Dispatch("Excel.Application")
   wb = Excel.Workbooks.Open(NameFile)
   sheet = wb.ActiveSheet
   print(saveMap)
   Col=0
   while Col<len(saveMap):
       Row=0
       while Row<len(saveMap[Col]):
           sheet.Cells(Row+1,Col+1).value= saveMap[Col][Row]
           sheet.Cells(Row+2+len(saveMap[Col]),Col+1).value= kolMap[Col][Row]
           Row=Row+1
       Col=Col+1
       
   #сохраняем рабочую книгу
   wb.Save()
   #закрываем ее
   wb.Close()
   #закрываем COM объект
   Excel.Quit()