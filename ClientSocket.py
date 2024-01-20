# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 16:22:36 2023

@author: Юрий
"""
import socket
import LoadSettingsIniFile as Setting
import GoTime
import time
import threading

#SocketIp = '127.0.0.1'
#SocketPort=8080
KolSocket=6
ArraySocketClient=[]

def ConnectSocket(SocketIp, SocketPort, Nom_Timer,SocketClusterTime):
    SocketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    print(GoTime.now(),'Client connect ',SocketIp, SocketPort)
    SocketClient.connect((SocketIp, SocketPort))  # подключемся к серверному сокету
    string_numbers = 'CTIME'+ str(int(Nom_Timer))+ "*"+str(int(SocketClusterTime)) +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    time.sleep(0.01)
    return SocketClient
    

def StartSocket(SocketClient,Nom_Timer):
    GoTime.setSocketTime()
    string_numbers='START'+ str(int(Nom_Timer)) +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    print(GoTime.now(),'StartSocket')
    time.sleep(0.01)


def FinishSocket(SocketClient,Nom_Timer):
    string_numbers='FINSH'+ str(int(Nom_Timer)) +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    print(GoTime.now(),'FinishSocket')
    data=b""
    while not b"\r\n" in data:
        tmp=SocketClient.recv(1024)
        if not tmp: 
            break
        else:
            data+=tmp
    data=data.decode('utf-8')
    return data


def SocketSendOF(SocketClient,Stat,Nom_Timer,way,TypeKlaster):
    string_numbers = 'WAYAG'+ str(int(Nom_Timer))+ "*"+str(int(TypeKlaster)) + "*" + '| '.join(str((num)) for num in way) + "\r\n"
    GoTime.setClusterTime()
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    data=b""
    while not b"\r\n" in data:
        tmp=SocketClient.recv(1024)
        if not tmp: 
            break
        else:
            data+=tmp
    data=data.decode('utf-8')
    Stat.SaveTimeCluster((GoTime.DeltClusterTime()).total_seconds())
    return data

def SocketEnd(SocketClient):
    string_numbers='CLOSE' +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    SocketClient.close()
