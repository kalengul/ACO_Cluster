# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 16:22:36 2023

@author: Юрий
"""
import socket
import LoadSettingsIniFile as Setting
import GoTime
import time



def ConnectSocket(Stat):
    global SocketClient
    GoTime.setSocketTime()
    SocketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    SocketClient.connect((Setting.SocketIp, Setting.SocketPort))  # подключемся к серверному сокету
    print('Client connect ',Setting.SocketIp, Setting.SocketPort)
    string_numbers = 'CTIME'+str(Setting.SocketClusterTime) + "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    time.sleep(0.001)

def SocketSendOF(Stat,way,TypeKlaster):
    string_numbers = 'WAYAG'+str(int(TypeKlaster)) + "*" + '| '.join(str(num) for num in way) + "\r\n"
    GoTime.setClusterTime()
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    data=b""
    while not b"\r\n" in data:
        tmp=SocketClient.recv(1024)
        if not tmp: 
            break
        else:
            data+=tmp
    Stat.SaveTimeCluster((GoTime.DeltClusterTime()).total_seconds())
    data=data.decode('utf-8')
    return data

def SocketEnd(Stat):
    string_numbers='CLOSE'
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    SocketClient.close()
    Stat.SaveTimeSocket((GoTime.DeltSocketTime()).total_seconds())