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


def computerCost(X, Y, theta):
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Y = Y.reshape(len(Y), 1)
    theta = np.asarray(theta, dtype=np.float64)
    theta = theta.reshape(len(theta), 1)

    m = X.shape[0]

    Z = normalFunction(X, theta)
    H = sigmoid(Z)

    cost = (-Y*np.log(H) - (1-Y)*(np.log(1-H))).sum()
    return cost/m


def gradientDescent(X, Y, theta, alpha):
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Y = Y.reshape(len(Y), 1)
    theta = np.asarray(theta, dtype=np.float64)
    theta = theta.reshape(len(theta), 1)
    r, c = X.shape

    Z = normalFunction(X, theta)
    H = sigmoid(Z)
    tmp = (H-Y)*X
    #tmp = tmp.sum(0)/r*alpha
    tmp = tmp.sum(0)/r
    tmp = tmp.reshape(c,1)
    tmp = tmp*alpha
    theta = theta - tmp
    return theta
