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
import scipy.io
from neural_network import computerCost


if __name__ == "__main__":
    data_name = 'ex4data1.mat'
    weights_name = 'ex4weights.mat'
    datas = scipy.io.loadmat(data_name)
    weights = scipy.io.loadmat(weights_name)

    input_layer_size  = 400
    hidden_layer_size = 25
    num_labels = 10

    X = datas['X']
    y = datas['y']

    m = X.shape[0]
    ones = np.ones((m,1))
    X = np.c_[ones, X]

    Y = np.zeros((m,num_labels))
    for i in range(m):
        #顺序很重要
        Y[i, y[i][0]-1] = 1

    #print(Y.shape)

    theta1 = weights['Theta1']
    theta2 = weights['Theta2']

    #print('X:', X.shape)
    #print('Theta1:', theta1.shape)
    #print('Theta2:', theta2.shape)

    theta1 = np.transpose(theta1)
    theta2 = np.transpose(theta2)
    #print('After transpose')
    #print('Theta1:', theta1.shape)
    #print('Theta2:', theta2.shape)

    lam = 1 
    J = computerCost(theta1, theta2, X, Y, lam)
    print('Sum:', J)
