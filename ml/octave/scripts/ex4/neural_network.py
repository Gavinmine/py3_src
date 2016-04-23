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


def sigmoidGradient(z):
    return sigmoid(z)*(1-sigmoid(z))


def randInitializeWeights(l_in, l_out):
    epsilon_init = 0.12

    return np.random.rand(l_out, l_in + 1)*2*epsilon_init - epsilon_init


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
    J = TMP.sum()/m+tsum

    return J


def gradientDescent(theta1, theta2, X, Y, lam):
    m = X.shape[0]

    #computer theta_grad
    a1 = X
    z2 = np.dot(a1, theta1)
    a2 = sigmoid(z2)
    j = a2.shape[0]
    ones = np.ones((j,1))
    a2 = np.c_[ones, a2]
    z3 = np.dot(a2, theta2)
    a3 = sigmoid(z3)
    d3 = a3-Y
    dz2 = sigmoidGradient(z2)
    td2 = np.dot(d3, np.transpose(theta2))
    n = td2.shape[0]
    d2 = td2[:, 1:n]*dz2

    theta1_grad = np.dot(np.transpose(d2), a1)
    theta2_grad = np.dot(np.transpose(d3), a2)

    theta1_grad = np.transpose(theta1_grad)
    theta2_grad = np.transpose(theta2_grad)

    #print('theta1_grad shape:', theta1_grad.shape)
    #print('theta1 shape:', theta1.shape)
    #print('theta2_grad shape:', theta2_grad.shape)
    #print('theta2 shape:', theta2.shape)

    req1 = lam/m*theta1
    req2 = lam/m*theta2
    req1[:, 0:1] = 0
    req2[:, 0:1] = 0

    theta1_grad = theta1_grad/m + req1
    theta2_grad = theta2_grad/m + req2
    #print('theta1_grad shape:', theta1_grad.shape)
    #print('theta2_grad shape:', theta2_grad.shape)

    return theta1_grad, theta2_grad
