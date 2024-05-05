# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:52:24 2024

@author: Юрий
"""
import threading
import random
import time

AntArr=[]

class Ant:
   def __init__(self,NomAnt):
       self.NomAnt = NomAnt
       self.way = []
       self.OF = 0
       self.ignore = 0
       self.ZeroAnt = 0
       self.kolIterationAntZero = 0
       print('Создан агент №',self.NomAnt)
       
def AddAntArray(NomAnt):
    ant=Ant(NomAnt)
    AntArr.append(ant)
    return len(AntArr)

def go_ant(Pg,ant):
    print('Старт поиска пути агентом №',ant.NomAnt)
    ant.OF=random.random()
    ant.way=Pg
    ant.ignore=random.randint(0, 5)
    ant.kolIterationAntZero=random.randint(0, 1)
    print('Окончание поиска пути агентом №',ant.NomAnt)
    
def go_create_new_graph():
    #Блокируем поток до момента, когда маршрут найдет нужное число агентов
    #Создаем новый параметрический граф
    #
    pass



Pg=['1','5']
#Создать поток который будет обновлять параметрический граф
ReGraph = threading.Thread(target=go_create_new_graph, args=(Pg))
ReGraph.start()

KolIteration=9
KolAnt=10
AllAntIteration=KolIteration*KolAnt
ant_tread_array=[]


KolAntEndWay=0
while KolAntEndWay<KolIteration*KolAnt:
    if len(AddAntArray)<=KolAnt:
        #Создание агента-потока, добавление его в список текущих агентов
        NomAnt=AddAntArray(KolAntEndWay+len(AddAntArray)+1)
        #Поиск агентом маршрута и вычисление целевой функции на кластере + повторный поиск, если найден маршрут в Хэше
        ant = threading.Thread(target=go_ant, args=(Pg,AntArr[NomAnt]))
        ant_tread_array.append(ant)
        ant.start()
    
    




def my_function(param, event):
    # Реализация функции
    # По завершении работы функции мы устанавливаем событие
    event.set()

def on_thread_completion():
    # Функция, которую нужно выполнить после завершения любого потока
    print("Какой-то поток завершился")

events = [threading.Event() for _ in range(3)]  # Создаем список событий для каждого потока
params = [1, 2, 3]  # Список параметров для каждого потока
# Создаем и запускаем потоки
threads = []
for param, event in zip(params, events):
    thread = threading.Thread(target=my_function, args=(param, event))
    threads.append(thread)
    thread.start()

# Ждем завершения любого из потоков
for event in events:
    event.wait()
    on_thread_completion()

