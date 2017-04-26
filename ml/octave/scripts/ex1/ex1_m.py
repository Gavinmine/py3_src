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



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from common import computeCost, gradientDescent

if __name__ == "__main__":
    file_name = 'ex1data2.txt'
    datas = pd.read_csv(file_name, names=['size', 'room', 'price'])
    X = pd.DataFrame(datas, columns = ['size', 'room'])
    mean = X.mean()
    std = X.std()
    max = X.max()
    #X = (X-mean)/max
    X = (X-mean)/std
    X.insert(0, 'X0', 1)
    Y = datas['price']
    #print('X:\n',X)
    #print('Y:\n',Y)
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Y = Y.reshape(len(Y), 1)
    #print("X:",X)
    #print("length of X:",X.shape)
    #print("Y:",Y)
    #print("length of Y:",Y.shape)

    r,c = X.shape
    theta = np.zeros((c,1))
    alpha = 0.01
    save_times = 1500
    times = list(range(save_times))
    costs = []
    for i in range(1500):
        cost = computeCost(X,Y,theta)
        if i < save_times:
            costs.append(cost)
            #print('Theta:', theta)
        theta = gradientDescent(X,Y,theta,alpha)

    print('Theta:', theta)
    plt.plot(times, costs)
    plt.xlabel('Time(s)')
    plt.ylabel('Cost(s)')
    plt.show()
