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
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':
    file_name = 'ex1data1.txt'
    datas = pd.read_csv(file_name, names=['population', 'profit'])

    X = pd.DataFrame(datas, columns=['X0','population'])
    X['X0'] = 1
    Y = datas['profit']
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Y = Y.reshape(len(Y), 1)
    r,c = X.shape
    alpha = 0.01
    #theta=np.random.random((c,1))
    theta=np.zeros((c,1))
    save_times = 1500
    times = list(range(save_times))
    costs = []
    theta0 = []
    theta1 = []
    for i in range(1500):
        #print("Theta: ", theta)
        cost = computeCost(X, Y, theta)
        #print("Cost: ", cost)
        if i < save_times:
            costs.append(cost)
            theta0.append(theta[0])
            theta1.append(theta[1])
        theta = gradientDescent(X, Y, theta, alpha)

    print(theta)

    #datas.plot(kind='scatter', x='population', y='profit')
    datas.plot.scatter('population', 'profit')
    x = np.linspace(5,25,1000)
    y = theta[0]+theta[1]*x
    plt.plot(x,y)
    plt.figure(2)
    plt.plot(times, costs)
    plt.xlabel("Time(s)")
    plt.ylabel("Cost(s)")
    fig = plt.figure(3)
    ax = fig.gca(projection = '3d')
    ax.plot(theta0, theta1, costs, label='Curve')
    ax.legend()
    ax.set_xlabel('Theta0')
    ax.set_ylabel('Theta1')
    ax.set_zlabel('Cost(s)')
    plt.show()
