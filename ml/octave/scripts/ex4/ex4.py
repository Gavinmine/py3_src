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
from neural_network import computerCost,gradientDescent,randInitializeWeights
from os import path


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
    lam = 1 
    J = computerCost(theta1, theta2, X, Y, lam)
    print('Sum:', J)
    #print('After transpose')
    #print('Theta1:', theta1.shape)
    #print('Theta2:', theta2.shape)

    if path.exists('theta1.npy') and path.exists('theta2.npy'):
        initial_Theta1 = np.load('theta1.npy')
        initial_Theta2 = np.load('theta2.npy')
    else:
        initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size)
        initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels)
        initial_Theta1 = np.transpose(initial_Theta1)
        initial_Theta2 = np.transpose(initial_Theta2)
        #print('After transpose')
        #print('initial_Theta1:', initial_Theta1.shape)
        #print('initial_Theta2:', initial_Theta2.shape)

    alpha1 = np.ones(initial_Theta1.shape)
    alpha2 = np.ones(initial_Theta2.shape)
    alpha1 = alpha1*0.5
    alpha2 = alpha2*0.1
    for i in range(200):
        tmp_theta1, tmp_theta2 = gradientDescent(initial_Theta1, initial_Theta2, X, Y, lam)
        J = computerCost(initial_Theta1, initial_Theta2, X, Y, lam)
        print('Cost for neural_network:', J)

        tmp_theta1 = initial_Theta1 - alpha1*tmp_theta1
        tmp_theta2 = initial_Theta2 - alpha2*tmp_theta2

        initial_Theta1 = tmp_theta1
        initial_Theta2 = tmp_theta2

    np.save('theta1.npy', initial_Theta1)
    np.save('theta2.npy', initial_Theta2)

    hl = np.dot(X, initial_Theta1)
    ones = np.ones((hl.shape[0],1))
    hl = np.c_[ones, hl]
    ol = np.dot(hl, initial_Theta2)
    p_y = np.argmax(ol, axis=1)
    p_y = p_y+1
    p_y = p_y.reshape(p_y.shape[0], 1)

    accuracy = np.mean(np.double(p_y == y))
    print('accuracy:', accuracy)

    #print('tmp_theta1 shape:', tmp_theta1.shape)
    #print('tmp_theta2 shape:', tmp_theta2.shape)

    #print('tmp_theta1:', tmp_theta1)
    #print('tmp_theta2:', tmp_theta2)


    # Gradient checking
    #num_theta1 = np.zeros(tmp_theta1.shape)
    #num_theta2 = np.zeros(tmp_theta2.shape)

    #e = 0.0001
    #j,k = num_theta1.shape
    #for i in range(j):
    #    for l in range(k):
    #        loss_theta1 = initial_Theta1.copy()
    #        theta_v = initial_Theta1[i,l]
    #        loss_theta1[i,l] = theta_v + e

    #        loss_theta2 = initial_Theta1.copy()
    #        theta_v = initial_Theta1[i,l]
    #        loss_theta2[i,l] = theta_v - e

    #        num_theta1[i,l] = (computerCost(loss_theta1, initial_Theta2, X, Y, lam) - computerCost(loss_theta2, initial_Theta2, X, Y, lam))/2/e

    #        print('gd:%f,   num:%f' %(tmp_theta1[i,l], num_theta1[i,l]))

    #j,k = num_theta2.shape
    #for i in range(j):
    #    for l in range(k):
    #        loss_theta1 = initial_Theta2.copy()
    #        theta_v = initial_Theta2[i,l]
    #        loss_theta1[i,l] = theta_v + e

    #        loss_theta2 = initial_Theta2.copy()
    #        theta_v = initial_Theta2[i,l]
    #        loss_theta1[i,l] = theta_v - e

    #        num_theta2[i,l] = (computerCost(initial_Theta1, loss_theta1, X, Y, lam) - computerCost(initial_Theta1, loss_theta2, X, Y, lam))/2/e

    #        print('gd:%f,   num:%f' %(tmp_theta2[i,l], num_theta2[i,l]))
