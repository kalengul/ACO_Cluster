# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 09:25:27 2023

@author: Юрий
"""

import socket
import time
from datetime import datetime
import multiprocessing 
import threading

SocketIp = '127.0.0.1'
SocketPort=8080
KolSocket=6
ArraySocketClient=[]

def ConnectSocket(Nom_Timer,SocketClusterTime):
    global SocketClient
    SocketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    SocketClient.connect((SocketIp, SocketPort))  # подключемся к серверному сокету
    print(datetime.now(),'Client connect ',SocketIp, SocketPort)
    string_numbers = 'CTIME'+ str(int(Nom_Timer))+ "*"+str(int(SocketClusterTime)) +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    time.sleep(0.01)
    return SocketClient
    

def StartSocket(SocketClient,Nom_Timer):
    string_numbers='START'+ str(int(Nom_Timer)) +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    print(datetime.now(),'StartSocket')
    time.sleep(0.01)


def FinishSocket(SocketClient,Nom_Timer):
    string_numbers='FINSH'+ str(int(Nom_Timer)) +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    print(datetime.now(),'FinishSocket')
    data=b""
    while not b"\r\n" in data:
        tmp=SocketClient.recv(1024)
        if not tmp: 
            break
        else:
            data+=tmp
    data=data.decode('utf-8')
    return data


def SocketSendOF(SocketClient,Nom_Timer,way,TypeKlaster):
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

def SocketEnd(SocketClient):
    string_numbers='CLOSE' +  "\r\n"
    SocketClient.send(bytes(string_numbers, 'utf-8'))
    SocketClient.close()
   
def GoSocket(nomProc,End,Time):
    Nom_Timer=nomProc
    SocketClusterTime = Time
    SocketClient=ConnectSocket(Nom_Timer,SocketClusterTime)
    StartSocket(SocketClient,Nom_Timer)
    way=['1','5']
    TypeKlaster=404
    nom=0
    while nom<End:
        OF=SocketSendOF(SocketClient,Nom_Timer,way,TypeKlaster)
        #print(datetime.now(),nomProc,nom,Time,End,OF)
        nom=nom+1
    TimeSocket_str=FinishSocket(SocketClient,Nom_Timer)

    print('Время выполнения на клиенте = ',TimeSocket_str,End,Time,End*Time)
   # print('Сравнение времени = ',TimeSocket/End,Time)
    SocketEnd(SocketClient)
    
def GoIterationSocket(SocketClient,nomProc,End):
    Nom_Timer=nomProc
    StartSocket(SocketClient,Nom_Timer)
    way=['1','5']
    TypeKlaster=404
    nom=0
    while nom<End:
        OF=SocketSendOF(SocketClient,Nom_Timer%KolSocket,way,TypeKlaster)
        print(datetime.now(),nomProc,nom,Nom_Timer,End,OF)
        nom=nom+1
    TimeSocket_str=FinishSocket(SocketClient,Nom_Timer)
    print('Время выполнения на клиенте = ',Nom_Timer,TimeSocket_str,End)
    
if __name__ == '__main__': 
    multiprocessing.freeze_support() # необходимо для корректной работы многопроцессорности в Window
    End=[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]
    Time=[1000,2000,3000,4000,5000,6000,70000,80000,90000,100000,1000,2000,3000,4000,5000,6000,70000,80000,90000,100000,1000,2000,3000,4000,5000,6000,70000,80000,90000,100000,1000,2000,3000,4000,5000,6000,70000,80000,90000,100000]
    print(datetime.now(),'START')
    Nom_Timer=0
    while Nom_Timer<KolSocket:
        CurrentSocketClient=(ConnectSocket(Nom_Timer,Time[Nom_Timer]))
        ArraySocketClient.append(CurrentSocketClient)
        #print(CurrentSocketClient,ArraySocketClient,Nom_Timer)
        
        Nom_Timer=Nom_Timer+1
    threads = []
    kol_thread = int(input('Количество потоков: '))

    for i in range(kol_thread):
        t = threading.Thread(target=GoIterationSocket, args=(ArraySocketClient[i%KolSocket],i,End[i]))
        threads.append(t)
        t.start()

    # Ждем завершения всех потоков
    for t in threads:
        t.join()
    
    Nom_Timer=0
    while Nom_Timer<KolSocket:
        SocketEnd(ArraySocketClient[Nom_Timer])
        Nom_Timer=Nom_Timer+1
    
    input('ПРОГРАММА ЗАВЕРШЕНА')
