# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 09:25:27 2023

@author: Юрий
"""

import socket
import time

SocketIp = '127.0.0.1'
SocketPort=8080

def ConnectSocket(Nom_Timer):
    global SocketClient
    SocketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    SocketClient.connect((SocketIp, SocketPort))  # подключемся к серверному сокету
    print('Client connect ',SocketIp, SocketPort)
    string_numbers = 'CTIME'+ str(int(Nom_Timer))+ "*"+str(int(SocketClusterTime)) +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    time.sleep(0.001)
    

def StartSocket(Nom_Timer):
    string_numbers='START'+ str(int(Nom_Timer)) +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    print('START')
    time.sleep(0.001)


def FinishSocket(Nom_Timer):
    string_numbers='FINSH'+ str(int(Nom_Timer)) +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    print('FINSH')
    time.sleep(0.001)

def SocketSendOF(Nom_Timer,way,TypeKlaster):
    string_numbers = 'WAYAG'+ str(int(Nom_Timer))+ "*"+str(int(TypeKlaster)) + "*" + '| '.join(str((num)) for num in way) + "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    data=b""
    while not b"\r\n" in data:
        tmp=SocketClient.recv(1024)
        if not tmp: 
            break
        else:
            data+=tmp
    data=data.decode('utf-8')
    return data

def SocketEnd():
    string_numbers='CLOSE' +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    SocketClient.close()
    
Nom_Timer=0
SocketClusterTime = 20
ConnectSocket(Nom_Timer)
StartSocket(Nom_Timer)
way=['1','5']
TypeKlaster=404
print(SocketSendOF(Nom_Timer,way,TypeKlaster))
FinishSocket(Nom_Timer)
SocketEnd()