# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 13:13:44 2022

@author: Юрий
"""

HashPath = {}
MaxPath = {}


def goPathStr(path):
    st = ''
    i = 0
    while i < len(path):
        st = st + ';' + str(path[i])
        i = i + 1
    return st


def KolHash():
    return len(HashPath)


def getPath(path):
    if HashPath.get(path):
        return True, HashPath[path]
    else:
        return False, 0


def addPath(path, OF):
    if HashPath.get(path):
        return HashPath[path]
    else:
        HashPath[path] = OF


def printPath():
    print(HashPath)


def GetMaxPath():
    max_value = max(HashPath.values())
    MaxPath = {k: v for k, v in HashPath.items() if v == max_value}
    return MaxPath


def SortHash():
    global MaxPath
    ssd = sorted(HashPath, key=HashPath.__getitem__)
    k = ssd[-1]
    MaxPath = {k: HashPath[k]}


def PrintMaxPath():
    print(MaxPath)
