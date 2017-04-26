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
from logisticRegression import computerCost, gradientDescent
import matplotlib.pyplot as plt
from showDatas import classificationFigure

if __name__ == '__main__':
    name = 'ex2data1.txt'
    datas = pd.read_csv(name, names=['exam1', 'exam2', 'result'])
    Y = datas['result']
    X = pd.DataFrame(datas, columns=['X0', 'exam1','exam2'])
    X['X0'] = 1

    r,c = X.shape
    #alpha = 0.001
    alpha = np.zeros((c,1))
    alpha[0] = 1
    alpha[1] = 0.001
    alpha[2] = 0.001
    theta=np.zeros((c,1))
    #cost = computerCost(theta, X, Y)
    #print('cost:', cost)
    save_times = 1000
    times = list(range(save_times))
    costs = []
    for i in range(6000):
        cost = computerCost(theta, X, Y)
        if i < save_times:
            costs.append(cost)

        theta = gradientDescent(theta, X, Y, alpha)
        theta = theta.reshape(c,1)
        #if i < 10:
        #    print('Theta:', theta)

    print('Theta in the end:', theta)
    plt.plot(times, costs)
    plt.xlabel('Time(s)')
    plt.ylabel('Cost(s)')

    plt.figure(2)
    max = X['exam1'].max()
    min = X['exam1'].min()
    X = np.asarray(X, dtype=np.float64)
    pos = Y[Y==1].index
    neg = Y[Y==0].index
    plt.plot(X[pos, 1], X[pos, 2], '+')
    plt.plot(X[neg, 1], X[neg, 2], 'o')
    x = np.linspace(min,max,1000)
    #theta[0] = -25.161272
    #theta[1] = 0.206233
    #theta[2] = 0.201470
    y = -(theta[0] + theta[1]*x)/theta[2]
    plt.plot(x, y)

    plt.show()
