# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 11:43:39 2023

@author: Юрий
"""

import socket
import threading
import LoadSettingsIniFile as Setting
import VirtualKlaster

def serve_client(client_sock, cid, client_addr):
    print(f'Client #{cid} connected 'f'{client_addr[0]}:{client_addr[1]}')
    end_serve=True
    while end_serve:
        data=b""
        while not b"\r\n" in data:
            tmp=client_sock.recv(1024)
            if not tmp: 
                break
            else:
                data+=tmp
        data=str(data.decode())
        TypePacket = data[:5]
        data = data[5:]
        if TypePacket=='WAYAG':
            type_klaster_str, way_str = data.split('*')
            TypeKlaster=int(type_klaster_str)
            path = [float(num) for num in way_str.split('|')]
            OF=VirtualKlaster.GetObjectivFunction(path,TypeKlaster,SocketClusterTime[cid])
            string_numbers=str(OF)+"\r\n"
            client_sock.send(bytes(string_numbers, 'utf-8'))
        elif TypePacket=='CTIME':
            SocketClusterTime.append(float(data))
        elif TypePacket=='CLOSE':
            end_serve=False
            client_sock.close
            print(f'Client #{cid} close 'f'{client_addr[0]}:{client_addr[1]}')

def run_server_cluster():
    print('Старт процесса для сокет-сервера кластера ')
    print(Setting.SocketIp, Setting.SocketPort)
    global SocketClusterTime
    SocketClusterTime=[]
    sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sk.bind((Setting.SocketIp, Setting.SocketPort))
    sk.listen()
    try:
        while True:
            cid = 0
            while True:
                client_sock, client_addr = sk.accept()
                # Создание нового потока
                t = threading.Thread(target=serve_client,args=(client_sock, cid, client_addr)) 
                t.start()  # Запуск нового потока
                cid += 1
    finally: sk.close()