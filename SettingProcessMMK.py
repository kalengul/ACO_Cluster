# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 00:05:10 2024

@author: Юрий
"""
import psutil #Для установки конкретного номера CPU
import os #Для получения PID

import MMK
import ClientSocket as client_socket
import LoadSettingsIniFile as load_settings_ini_file

def run_script(text_print, nom_proc, folder, folder_pg, lock_excel):
    #Настроить процесс на CPU
    # Устанавливаем аффинити процессу
    #p = psutil.Process(os.getpid())
    #p.cpu_affinity([nom_proc])
    #Подключить необходимое количество сокет-соединений с сервером
    #Загрузка данных из ini файла
    load_settings_ini_file.readSettingVirtualClaster(folder+'/setting.ini')
    #Создание подключений
    nom_connect=0
    while nom_connect<load_settings_ini_file.SocketKolCluster:
        CurrentSocketClient=client_socket.ConnectSocket(load_settings_ini_file.SocketIp, load_settings_ini_file.SocketPort, nom_proc, load_settings_ini_file.SocketClusterTime)
        client_socket.ArraySocketClient.append(CurrentSocketClient)
        nom_connect=nom_connect+1
    # Запускаем ММК с заданными параметрами
    MMK.run_script(text_print, nom_proc, folder, folder_pg, lock_excel)
    #Завершение сокет-соединений с сервером
    nom_connect=0
    while nom_connect<len(client_socket.ArraySocketClient):
        client_socket.SocketEnd(client_socket.ArraySocketClient[nom_connect])
        nom_connect=nom_connect+1