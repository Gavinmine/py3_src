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

def computeCost(x, y, theta):
    x_rows, x_cols = x.shape
    theta_rows, theta_cols = theta.shape
    if x_cols != theta_rows:
        print('x_cols:%d, theta_rows:%d' %(x_cols, theta_rows))
        print("Can not dot, please check")
        return None

    tmp = np.dot(x,theta)-y
    sum = (tmp*tmp).sum()
    return sum/2/x_rows


def gradientDescent(x, y, theta, alpha):
    theta0 = theta[0]
    theta1 = theta[1]
    h = np.dot(x,theta)
    r,c = h.shape
    tmp = (h-y)*x
    t0 = theta0 - (tmp[0:,0].sum())/r*alpha
    t1 = theta1 - (tmp[0:,1].sum())/r*alpha
    theta[0] = t0
    theta[1] = t1
    return theta

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
    theta=np.random.random((c,1))
    theta[0] = 0
    theta[1] = 0
    times = list(range(100))
    costs = []
    for i in range(1500):
        #print("Theta: ", theta)
        cost = computeCost(X, Y, theta)
        print("Cost: ", cost)
        if i < 100:
            costs.append(cost)
        theta = gradientDescent(X, Y, theta, alpha)

    print(theta)

    #datas.plot(kind='scatter', x='population', y='profit')
    datas.plot.scatter('population', 'profit')
    x = np.linspace(5,25,1000)
    y = theta[0]+theta[1]*x
    plt.plot(x,y)
    print(costs[0])
    print(costs[1])
    plt.figure(2)
    plt.plot(times, costs)
    plt.show()
