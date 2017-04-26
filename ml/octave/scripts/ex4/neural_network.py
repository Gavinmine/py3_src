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
import pandas as pd


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


def cost_Grad(theta, input_layer_size, hidden_layer_size, num_labels, X, Y, lam):
    J = computer_Cost(theta, input_layer_size, hidden_layer_size, num_labels, X, Y, lam)
    nn_params = gradient_Descent(theta, input_layer_size, hidden_layer_size, num_labels, X, Y, lam)

    #print('Cost:', J)
    return (J, nn_params)


def computer_Cost(theta, input_layer_size, hidden_layer_size, num_labels, X, Y, lam):
    theta = np.asarray(theta, dtype=np.float64)
    theta1 = theta[0:hidden_layer_size*(input_layer_size+1)]
    theta2 = theta[hidden_layer_size*(input_layer_size+1):]
    theta1 = theta1.reshape(hidden_layer_size, (input_layer_size+1))
    theta2 = theta2.reshape(num_labels, (hidden_layer_size + 1))
    theta1 = theta1.T
    theta2 = theta2.T

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


def gradient_Descent(theta, input_layer_size, hidden_layer_size, num_labels, X, Y, lam):
    theta = np.asarray(theta, dtype=np.float64)
    theta1 = theta[0:hidden_layer_size*(input_layer_size+1)]
    theta2 = theta[hidden_layer_size*(input_layer_size+1):]
    theta1 = theta1.reshape(hidden_layer_size, (input_layer_size+1))
    theta2 = theta2.reshape(num_labels, (hidden_layer_size + 1))
    theta1 = theta1.T
    theta2 = theta2.T

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

    theta1_grad = theta1_grad.T
    theta2_grad = theta2_grad.T

    #nn_params = np.append(theta1_grad, theta2_grad)
    nn_params = np.hstack([theta1_grad.flatten(),theta2_grad.flatten()])

    return nn_params


def predict(theta, input_layer_size, hidden_layer_size, num_labels, X):
    theta1 = theta[0:hidden_layer_size*(input_layer_size+1)]
    theta2 = theta[hidden_layer_size*(input_layer_size+1):]
    theta1 = theta1.reshape(hidden_layer_size, (input_layer_size+1))
    theta2 = theta2.reshape(num_labels, (hidden_layer_size + 1))
    theta1 = theta1.T
    theta2 = theta2.T

    hl = np.dot(X, theta1)
    ones = np.ones((hl.shape[0],1))
    hl = np.c_[ones, hl]
    ol = np.dot(hl, theta2)
    p_y = np.argmax(ol, axis=1)
    p_y = p_y+1
    p_y = p_y.reshape(p_y.shape[0], 1)

    return p_y


def nnCostFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, features, classes, reg):
    theta1 = nn_params[0:(hidden_layer_size*(input_layer_size+1))].reshape(hidden_layer_size,(input_layer_size+1))
    theta2 = nn_params[(hidden_layer_size*(input_layer_size+1)):].reshape(num_labels,(hidden_layer_size+1))

    m = features.shape[0]
    y_matrix = pd.get_dummies(classes.ravel()).as_matrix()

    #Cost
    al = features   #5000*4001

    z2 = theta1.dot(al.T)   #25*401 * 401*5000 = 25*5000
    a2 = np.c_[np.ones((features.shape[0], 1)), sigmoid(z2.T)]  #5000*26

    z3 = theta2.dot(a2.T)   # 10*26 * 26 * 5000 = 10*5000
    a3 = sigmoid(z3)    #10*5000

    J = -1*(1/m)*np.sum((np.log(a3.T)*(y_matrix)+np.log(1-a3).T*(1-y_matrix))) + \
            (reg/(2*m))*(np.sum(np.square(theta1[:,1:])) + np.sum(np.square(theta2[:,1:])))

    return J


def nnGradFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, features, classes, reg):
    theta1 = nn_params[0:(hidden_layer_size*(input_layer_size+1))].reshape(hidden_layer_size,(input_layer_size+1))
    theta2 = nn_params[(hidden_layer_size*(input_layer_size+1)):].reshape(num_labels,(hidden_layer_size+1))

    m = features.shape[0]
    y_matrix = pd.get_dummies(classes.ravel()).as_matrix()

    #Cost
    al = features   #5000*401

    z2 = theta1.dot(al.T)   #25*401 * 401*5000 = 25*5000
    a2 = np.c_[np.ones((features.shape[0], 1)), sigmoid(z2.T)]  #5000*26

    z3 = theta2.dot(a2.T)   # 10*26 * 26 * 5000 = 10*5000
    a3 = sigmoid(z3)    #10*5000

    #print('a3.T shape:', a3.T.shape)
    #print('y_matrix shape:', y_matrix.shape)
    J = -1*(1/m)*np.sum((np.log(a3.T)*(y_matrix)+np.log(1-a3).T*(1-y_matrix))) + \
            (reg/(2*m))*(np.sum(np.square(theta1[:,1:])) + np.sum(np.square(theta2[:,1:])))

    # Gradients
    d3 = a3.T - y_matrix    #5000*10
    d2 = theta2[:, 1:].T.dot(d3.T)*sigmoidGradient(z2)  #25*10 * 10*5000 * 25*5000 = 25*5000

    delta1 = d2.dot(al) #25*5000 * 5000*401 = 25*401
    delta2 = d3.T.dot(a2)   #10*5000 * 5000*26 = 10*26

    theta1_ = np.c_[np.ones((theta1.shape[0], 1)), theta1[:, 1:]]
    theta2_ = np.c_[np.ones((theta2.shape[0], 1)), theta2[:, 1:]]

    theta1_grad = delta1/m + (theta1_*reg)/m
    theta2_grad = delta2/m + (theta2_*reg)/m

    return np.append(theta1_grad, theta2_grad)
    #return(J, theta1_grad, theta2_grad)
    #return(J, np.hstack([theta1_grad.flatten(),theta2_grad.flatten()]))
