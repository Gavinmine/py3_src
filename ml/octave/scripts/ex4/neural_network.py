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

def normalFunction(X,theta):
    X = np.asarray(X, dtype=np.float64)
    theta = np.asarray(theta, dtype=np.float64)

    return np.dot(X,theta)


def sigmoid(Z):
    return 1/(1+np.exp(-Z))


def computerCost(theta1, theta2, X, Y, lam):
    theta1 = np.asarray(theta1, dtype=np.float64)
    theta2 = np.asarray(theta2, dtype=np.float64)
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    #Y = Y.reshape(len(Y), 1)

    m = X.shape[0]

    H = sigmoid(normalFunction(X, theta1))
    T = np.ones((m, 1))
    H = np.c_[T, H]
    #print('H:', H.shape)
    H = sigmoid(normalFunction(H, theta2))
    #print('H:', H.shape)

    req = lam/2/m
    tr1 = theta1.shape[0]
    tr2 = theta2.shape[0]
    T1 = theta1[1:tr1]
    T2 = theta2[1:tr2]

    tsum = ((T1*T1).sum()+(T2*T2).sum())*req

    TMP = -Y*np.log(H) - (1-Y)*(np.log(1-H))
    return TMP.sum()/m+tsum
