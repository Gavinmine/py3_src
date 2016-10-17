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
import xgboost as xgb
from sklearn.decomposition import PCA
from sklearn.cross_validation import KFold
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import train_test_split


def catLabel(catNum=116):
    catLabels = []
    for n in range(catNum):
        catLabels.append('cat'+str(n+1))

    return catLabels


def transData(transName, saveName):
    train = pd.read_csv(transName)
    catList = catLabel()
    letter_num = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':10, 'K':11, 'L':12, 'M':13, 'N':14,
                  'O':15, 'P':16, 'Q':17, 'R':18, 'S':19, 'T':20, 'U':21, 'V':22, 'W':23, 'X':24, 'Y':25, 'Z':26}

    catTypesList = []
    catTypesDict = {}

    for cat in catList:
        catTypes = train[cat].unique()
        for catType in catTypes:
            if catType in catTypesList:
                pass
            else:
                catTypesList.append(catType)
        #if row != 2:
        #    print(cat, catTypes)

    for catType in catTypesList:
        if (len(catType) == 1):
            catTypesDict[catType] = letter_num[catType]
        else:
            total = 0
            for letter in catType:
                total += letter_num[letter]
            catTypesDict[catType] = total

    for cat in catList:
        train[cat].replace(catTypesDict, inplace=True)

    train.to_csv(saveName)


def doPCA(trainName):
    trans = pd.read_csv(trainName)
    transPixels = trans.iloc[:, 2:118]
    transPixelsArray = transPixels.values
    pca = PCA(n_components=10, whiten=True)
    pca.fit(transPixelsArray)
    afterTransPixels = pca.transform(transPixelsArray)

    transLabels = []
    for i in range(10):
        label = 'afterCat' + str(i+1)
        transLabels.append(label)

    afterTransData = pd.DataFrame(afterTransPixels, columns=transLabels)
    for i in range(14):
        contName = 'cont' + str(i+1)
        afterTransData[contName] = trans[contName]

    return afterTransData

    #trainData = afterTransData.values
    #trainLoss = trans['loss'].values
    #lossTrain = xgb.DMatrix(trainData, label=trainLoss )

    #param = {'eta':0.1}
    #lossXgb = xgb.train(param, lossTrain)


def xg_eval_mse(yhat, trainData):
    y = trainData.get_label()
    return 'mse', mean_squared_error(y, yhat)


def xg_eval_mae(yhat, trainData):
    y = trainData.get_label()
    return 'mse', mean_absolute_error(y, yhat)


def trainXGB(trainName, testName):
    train = pd.read_csv(trainName)
    test = pd.read_csv(testName)
    catLabels = catLabel()
    for cLabel in catLabels:
        gCatLabel = train.groupby(train[cLabel])['loss'].mean()
        train[cLabel] = train[cLabel].map(gCatLabel)
        test[cLabel] = test[cLabel].map(gCatLabel)

    allLoss = train['loss']
    allTrain = train.drop(['id', 'loss'], axis=1)

    trainData, validData, trainLoss, validLoss = train_test_split(allTrain, allLoss, test_size = 0.2, random_state = 234)
    lossTrain = xgb.DMatrix(trainData, trainLoss)
    lossValid = xgb.DMatrix(validData, validLoss)

    watchList = [(lossTrain, 'train'), (lossValid, 'valid')]
    param = {'eta':0.1}
    clf = xgb.train(param, lossTrain, 2500, watchList, early_stopping_rounds=30, verbose_eval=20, feval=xg_eval_mse, maximize=False)
    return clf, test


def trainning(trainName):
    train = pd.read_csv(trainName)
    mseList = []
    catLabels = catLabel()
    for cLabel in catLabels:
        gCatLabel = train.groupby(train[cLabel])['loss'].mean()
        train[cLabel] = train[cLabel].map(gCatLabel)

    trainLen = len(train)
    kf = KFold(trainLen, n_folds=10)
    for trainIndex, validIndex in kf:
        forTrain, forValid = train.loc[trainIndex], train.loc[validIndex]
        trainLoss = forTrain['loss']
        validLoss = forValid['loss']
        forTrain = forTrain.drop(['loss', 'id'], axis = 1)
        forValid = forValid.drop(['loss', 'id'], axis = 1)
        trainData = forTrain.values
        validData = forValid.values


        lossTrain = xgb.DMatrix(trainData, trainLoss.values)
        lossValid = xgb.DMatrix(validData, validLoss.values)
        param = {'eta':0.1}
        validDataXgb = xgb.DMatrix(validData, missing = -999.0)

        watchList = [(lossTrain, 'train'), (lossValid, 'valid')]

        clf = xgb.train(param, lossTrain, 2500, watchList, early_stopping_rounds=30, verbose_eval=20, feval=xg_eval_mse, maximize=False)
        #clf = xgb.train(param, lossTrain, 2500, watchList, early_stopping_rounds=30, verbose_eval=20, feval=xg_eval_mae, maximize=False)

        validLossPred = clf.predict(validDataXgb)
        mse = mean_squared_error(validLossPred, validLoss.values)
        mseList.append(mse)

    averageErr = sum(mseList)/len(mseList)
    print('Average MSE:', averageErr)




def main():
    direct = './input/'
    trainName = direct + 'transform_train.csv'
    testName = direct + 'transTest.csv'
    transTrain = doPCA(trainName)
    transTest = doPCA(testName)

    trainData = transTrain.values
    testData = transTest.values
    testDataXgb = xgb.DMatrix(testData, missing = -999.0)

    train = pd.read_csv(trainName)
    trainLoss = train['loss']

    lossTrain = xgb.DMatrix(trainData, label=trainLoss)
    param = {'eta':0.1}
    lossXgb = xgb.train(param, lossTrain)

    lossPred = lossXgb.predict(testDataXgb)

    test = pd.read_csv(testName)

    submission = pd.DataFrame({
        'id': test['id'],
        'loss': lossPred
    })

    saveName = 'usingXGB'+'.csv'
    submission.to_csv(saveName, index=False)


if __name__ == '__main__':
    #testName = './input/test.csv'
    #saveName = './input/transTest.csv'
    #transData(testName, saveName)
    #main()

    trainName = './input/train.csv'
    testName = './input/test.csv'
    #trainning(trainName)
    clf, test = trainXGB(trainName, testName)
    testData = test.drop(['id'], axis=1)
    testData = xgb.DMatrix(testData)
    testPred = clf.predict(testData)
    submission = pd.DataFrame({
        'id': test['id'],
        'loss': testPred
    })

    saveName = 'usingXGB'+'.csv'
    submission.to_csv(saveName, index=False)
