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


def computerCost(theta, X, Y):
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


def gradientDescent(theta, X, Y, alpha):
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Y = Y.reshape(len(Y), 1)
    theta = np.asarray(theta, dtype=np.float64)
    theta = theta.reshape(len(theta), 1)
    r, c = X.shape

    Z = normalFunction(X, theta)
    H = sigmoid(Z)
    tmp = (H-Y)*X
    tmp = tmp.sum(0)/r
    tmp = tmp.reshape(c,1)
    tmp = tmp*alpha
    theta = theta - tmp
    return theta.flatten()


def computerCost_Req(theta, X, Y, l = 1):
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


def gradientDescent_Req(theta, X, Y, l = 1):
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Y = Y.reshape(len(Y), 1)
    theta = np.asarray(theta, dtype=np.float64)
    theta = theta.reshape(len(theta), 1)
    r, c = X.shape

    Z = normalFunction(X, theta)
    H = sigmoid(Z)
    tmp = (H-Y)*X
    tmp = tmp.sum(0)/r
    tmp = tmp.reshape(c,1)
    return tmp.flatten()


def cost_grad(theta, X, Y):
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    Y = Y.reshape(len(Y), 1)
    theta = np.asarray(theta, dtype=np.float64)
    #theta = theta.reshape(len(theta), 1)
    theta = theta.reshape(3, 1)

    m,c = X.shape

    Z = normalFunction(X, theta)
    H = sigmoid(Z)

    #cost = (-Y*np.log(H) - (1-Y)*(np.log(1-H))).sum(0)
    #cost = cost/m

    cost = (1.0 / m) * ((-Y.T.dot(np.log(H))) - ((1 - Y.T).dot(np.log(1.0 - H))))

    tmp = (H-Y)*X
    #tmp = tmp.sum(0)/r*alpha
    tmp = tmp.sum(0)/m

    return cost.flatten(), tmp.flatten()
    #return cost.flatten()
