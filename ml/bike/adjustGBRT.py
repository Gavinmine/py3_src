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


def getTime(dateTime):
    return int(dateTime.split(' ')[1].split(':')[0])


def getMonth(dateTime):
    return int(dateTime.split(' ')[0].split('-')[1])


def squaredLogError(pred, actual):
    return (np.log(pred+1)-np.log(actual+1))**2


def main():
    direct = './input/'
    trainName = direct + 'train.csv'

    train = pd.read_csv(trainName)

    datetime = train['datetime']
    time = datetime.apply(getTime)
    month = datetime.apply(getMonth)

    dropTrainDatetimeTrain = train.drop(labels='datetime', axis = 1)
    dropTrainDatetimeTrain['time'] = time
    dropTrainDatetimeTrain['month'] = month

    #forTrain = dropTrainDatetimeTrain.head(8709)
    #forValid = dropTrainDatetimeTrain.tail(2177)

    forTrain = dropTrainDatetimeTrain.tail(8709)
    forValid = dropTrainDatetimeTrain.head(2177)

    #predictors = ['month', 'time', 'season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']
    predictors = ['time', 'season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']
    #predictors = ['time', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']

    loss = ['ls', 'lad', 'huber', 'quantile']

    for los in loss:
        #est = GradientBoostingRegressor(n_estimators=1000, max_depth=6, max_features=3, loss=los)
        est = GradientBoostingRegressor(n_estimators=1000, max_depth=6, loss=los)
        forTrainCasual = forTrain['casual'].values
        forTrainCasual = forTrainCasual + 1
        forTrainCasual = np.log(forTrainCasual)
        est.fit(forTrain[predictors], forTrainCasual)
        casual = est.predict(forValid[predictors])
        casual = np.exp(casual) - 1

        forTrainRegistered = forTrain['registered'].values
        forTrainRegistered = forTrainRegistered + 1
        forTrainRegistered = np.log(forTrainRegistered)
        est.fit(forTrain[predictors], forTrainRegistered)
        registered = est.predict(forValid[predictors])
        registered = np.exp(registered) - 1

        allCounts = casual+registered
        for i in range(len(allCounts)):
            if allCounts[i] <= 0:
                allCounts[i] = 1

        #meanSquaredError = mean_squared_error(forValid['count'], allCounts)
        #print('loss:%s  error:%f' % (los, meanSquaredError))
        rmsle = np.sqrt(squaredLogError(allCounts, forValid['count'].values).mean())
        print('loss:%s  rmsle:%f' % (los, rmsle))


if __name__ == '__main__':
    main()
