# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 20:01:22 2023

@author: Юрий
"""
import IterationStatistic
import multiprocessing
import time
import subprocess
import os

if __name__ == '__main__':
    lock_excel = multiprocessing.Lock()
    KolProcess = int(input('Количество процессов: '))
    # Создаем список процессов
    folderPg=os.getcwd()+'/ParametricGraph'
    processes = []
    for i in range(KolProcess):
        folder=os.getcwd()+'/Program Process '+str(i)
#        run_script(i,folder,folderPg,lock_excel)
        p = multiprocessing.Process(target=IterationStatistic.run_script, args=(i,folder,folderPg,lock_excel))
        processes.append(p)
#        print('Start process'+str(i))
        p.start()
    # Ждем завершения всех процессов
    for p in processes:
        p.join()
    input('ПРОГРАММА ЗАВЕРШЕНА')