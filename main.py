# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 20:01:22 2023

@author: Юрий
"""

import multiprocessing # Для многопроцессного запуска ММК и организации блокировки Excel
import os #Для путей к файлам
import subprocess #Для запуска кластер-сервера на C# через отдельны процесс

import IterationStatistic as iteration_statistic # модуль для запуска ММК
import ServerCluster as server_cluster # модуль для запуска кластер-сервера на Python

if __name__ == '__main__': 
    multiprocessing.freeze_support() # необходимо для корректной работы многопроцессорности в Windows
    lock_excel = multiprocessing.Lock() # создаем объект блокировки для работы с файлом Excel
    kol_process = int(input('Количество процессов: ')) 
    
    # Создаем процесс для кластер-сервера на Python
    #p = multiprocessing.Process(target=server_cluster.run_server_cluster) 
    #p.start()
    
    # Запуск процесса сокет-сервера на С#
    #subprocess.Popen(['Server/SocketServer.exe'], creationflags=subprocess.CREATE_NEW_CONSOLE)

    # Создаем список процессов для ММК
    folder_pg = os.getcwd() + '/ParametricGraph' # определяем путь к папке с параметрическими графами
    processes = [] 
    print(os.getcwd())
    
    for i in range(kol_process): 
        folder = os.getcwd() + '/Program Process ' + str(i) # определяем путь к папке с данными ММК для текущего процесса (файлы Setting.ini и результатов)
        p = multiprocessing.Process(target=iteration_statistic.run_script, args=(i, folder, folder_pg, lock_excel)) 
        processes.append(p) 
        p.start() 
    
    # Ждем завершения всех процессов
    for p in processes:
        p.join()
    
    input('ПРОГРАММА ЗАВЕРШЕНА') 
