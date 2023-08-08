# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 21:47:29 2023

@author: Юрий
"""
import MMK
import configparser
import os
import GoTime

def save_setting(name_file, type_config, subtype_config, parametr):
    """
    Функция для сохранения настроек в файл конфигурации.
    """
    config = configparser.ConfigParser()
    config.read(name_file)  
    config[type_config][subtype_config] = parametr
    with open(name_file, 'w') as configfile:
        config.write(configfile)
    
    
def save_parametr(folder, nom_proc, type_config, subtype_config, parametr):
    """
    Функция для сохранения параметров в файл конфигурации.
    """
    if os.path.exists(folder+'/setting.ini'):
        print(GoTime.now(), nom_proc, ' Save  '+folder+'/setting.ini','[', type_config, '][', subtype_config, ']=', parametr)  
        save_setting(folder+'/setting.ini', type_config, subtype_config, parametr)

def run_script(nom_proc, folder, folder_pg, lock_excel):
    """
    Функция для запуска ММК.
    """
    array_parametr=[]
    array_parametr.append('0.5')
    array_parametr.append('1')
    array_parametr.append('2')
    array_parametr.append('10')
    array_parametr2=[]
    array_parametr2.append('0.5')
    array_parametr2.append('1')
    array_parametr2.append('2')
    array_parametr2.append('10')
    type_config='ParametricGraph'
    subtype_config='koef1'
    type_config2='ParametricGraph'
    subtype_config2='koef2'
    
    # Итерируемся по всем значениям параметра koef2
    j=0
    while j<len(array_parametr2): 
        # Сохраняем значение параметра koef2 в конфигурационный файл
        save_parametr(folder, nom_proc, type_config2, subtype_config2, array_parametr2[j])
        text_print2='koef2='+array_parametr2[j]
        i=0
        # Итерируемся по всем значениям параметра koef1
        while i<len(array_parametr):
            # Сохраняем значение параметра koef1 в конфигурационный файл
            save_parametr(folder, nom_proc, type_config, subtype_config, array_parametr[i])
            text_print=text_print2+' koef1='+array_parametr[i]
            # Запускаем ММК с заданными параметрами
            MMK.run_script(text_print, nom_proc, folder, folder_pg, lock_excel)
            i=i+1
        j=j+1