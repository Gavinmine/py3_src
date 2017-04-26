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
from sklearn.ensemble import GradientBoostingRegressor
from common import getTime, getMonth


def main():
    direct = './input/'
    trainName = direct + 'train.csv'
    testName = direct + 'test.csv'

    train = pd.read_csv(trainName)
    test = pd.read_csv(testName)

    datetime = train['datetime']
    time = datetime.apply(getTime)
    month = datetime.apply(getMonth)

    dropTrainDatetimeTrain = train.drop(labels='datetime', axis = 1)
    dropTrainDatetimeTrain['time'] = time
    dropTrainDatetimeTrain['month'] = month

    #predictors = ['month', 'time', 'season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']
    predictors = ['time', 'season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']
    los = 'lad'
    treeNum = 1500
    est = GradientBoostingRegressor(n_estimators=treeNum, max_depth=6, loss=los)
    #est = GradientBoostingRegressor(n_estimators=1000, max_depth=6, max_features=3, loss=los)


    datetime = test['datetime']
    time = datetime.apply(getTime)
    month = datetime.apply(getMonth)

    dropTestDatetimeTrain = test.drop(labels='datetime', axis = 1)
    dropTestDatetimeTrain['time'] = time
    dropTestDatetimeTrain['month'] = month

    trainCasual = dropTrainDatetimeTrain['casual'].values
    trainCasual = trainCasual + 1
    tranCasual = np.log(trainCasual)
    est.fit(dropTrainDatetimeTrain[predictors], tranCasual)
    casual = est.predict(dropTestDatetimeTrain[predictors])
    casual = np.exp(casual) - 1

    trainRegistered = dropTrainDatetimeTrain['registered'].values
    trainRegistered = trainRegistered + 1
    tranRegistered = np.log(trainRegistered)
    est.fit(dropTrainDatetimeTrain[predictors], tranRegistered)
    registered = est.predict(dropTestDatetimeTrain[predictors])
    registered = np.exp(registered) - 1
    predCount = casual + registered

    #est.fit(dropTrainDatetimeTrain[predictors], dropTrainDatetimeTrain['count'])
    #predCount = est.predict(dropTestDatetimeTrain[predictors])
    #print(type(predCount))
    #print(predCount.shape)
    for i in range(len(predCount)):
        if predCount[i] < 0:
            print('registered:', predCount[i])
            predCount[i] = 1

    submission = pd.DataFrame({
        'datetime': datetime,
        'count': predCount
    })

    saveName = 'usingGBRT'+'_'+los+str(treeNum)+'.csv'
    submission.to_csv(saveName, index=False)


if __name__ == '__main__':
    main()
