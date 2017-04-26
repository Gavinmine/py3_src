#!/usr/bin/env python3
# coding=utf-8

#　　　　　 　　┏┓ 　┏┓+ +
#　　　　　　　┏┛┻━━━┛┻┓ + +
#　　　　　　　┃　　　　　　　┃ 　
#　　　　　　　┃　　　━　　　┃ ++ + + +
# 　　 　　　  ████━████ ┃+
#　　　　　　　┃　　　　　　　┃ +
#　　　　　　　┃　　　┻　　　┃
#　　　　　　　┃　　　　　　　┃ + +
#　　　　　　　┗━┓　　　┏━┛
#　　　　　　　　┃　　　┃ + + + +
#　　　　　　　　┃　　　┃
#　　　　　　　　┃　　　┃　　　　Code is far away from bug with the animal protecting
#　　　　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug
#　　　　　　　　┃　　　┃
#　　　　　　　　┃　　　┃　　+
#　　　　　　　　┃　 　　┗━━━┓ + +
#　　　　　　　　┃ 　　　　　　　┣┓
#　　　　　　　　┃ 　　　　　　　┏┛
#　　　　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　　　┃┫┫　┃┫┫
# 　　　　　　　　┗┻┛　┗┻┛+ + + +


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def classificationFigure(X, Y):
    types = Y.unique()
    columns = X.columns

    X = np.asarray(X, dtype=np.float64)

    marks = ['o', '+', '.', ',', '*', 'X', 'D']

    fig = plt.figure()
    if len(columns) == 2:
        plt.xlabel(columns[0])
        plt.ylabel(columns[1])
    elif len(columns) == 3:
        ax = fig.gca(projection = '3d')
        ax.set_xlabel(columns[0])
        ax.set_ylabel(columns[1])
        ax.set_zlabel(columns[2])
    else:
        print('Only support 2D or 3D figure')
        exit(2)

    for i in range(len(types)):
        index = Y[Y==types[i]].index
        if len(columns) == 2:
            plt.plot(X[index, 0], X[index, 1], marks[i])
        elif len(columns) == 3:
            ax.plot(X[index, 0], X[index, 1], X[index, 2], marks[i])

    #plt.show()
    return plt
