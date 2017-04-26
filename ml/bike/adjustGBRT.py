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
from common import getTime, getMonth, squaredLogError
from sklearn.cross_validation import KFold, cross_val_score


def main():
    direct = './input/'
    trainName = direct + 'train.csv'

    train = pd.read_csv(trainName)

    datetime = train['datetime']
    time = datetime.apply(getTime)
    month = datetime.apply(getMonth)

    dropTrainDatetimeTrain = train.drop(labels='datetime', axis=1)
    dropTrainDatetimeTrain['time'] = time
    dropTrainDatetimeTrain['month'] = month

    trainData = dropTrainDatetimeTrain

    #predictors = ['month', 'time', 'season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']
    predictors = ['time', 'season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']
    #predictors = ['time', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']

    loss = ['ls', 'lad', 'huber', 'quantile']

    for los in loss:
        #est = GradientBoostingRegressor(n_estimators=1000, max_depth=6, max_features=3, loss=los)
        est = GradientBoostingRegressor(n_estimators=1000, max_depth=6, loss=los)
        trainCasual = trainData['casual'].values
        trainCasual = trainCasual + 1
        trainCasual = np.log(trainCasual)
        score = cross_val_score(est, trainData[predictors], trainCasual, cv=10)
        print('loss:%s' % los)
        print(score)
        #est.fit(trainData[predictors], trainCasual)
        #casual = est.predict(forValid[predictors])
        #casual = np.exp(casual) - 1

        #trainRegistered = trainData['registered'].values
        #trainRegistered = trainRegistered + 1
        #trainRegistered = np.log(trainRegistered)
        #est.fit(trainData[predictors], trainRegistered)
        #registered = est.predict(forValid[predictors])
        #registered = np.exp(registered) - 1

        #allCounts = casual+registered
        #for i in range(len(allCounts)):
        #    if allCounts[i] <= 0:
        #        allCounts[i] = 1

        #rmsle = np.sqrt(squaredLogError(allCounts, forValid['count'].values).mean())
        #print('loss:%s  rmsle:%f' % (los, rmsle))


if __name__ == '__main__':
    main()
