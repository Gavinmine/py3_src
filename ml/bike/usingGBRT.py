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
from sklearn.ensemble import GradientBoostingRegressor


def getTime(dateTime):
    return int(dateTime.split(' ')[1].split(':')[0])


def main():
    direct = './input/'
    trainName = direct + 'train.csv'
    testName = direct + 'test.csv'

    train = pd.read_csv(trainName)
    test = pd.read_csv(testName)

    datetime = train['datetime']
    time = datetime.apply(getTime)

    dropTrainDatetimeTrain = train.drop(labels='datetime', axis = 1)
    dropTrainDatetimeTrain['time'] = time

    predictors = ['time', 'season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']
    est = GradientBoostingRegressor(n_estimators=1000, max_depth=6, loss='lad')


    datetime = test['datetime']
    time = datetime.apply(getTime)

    dropTestDatetimeTrain = test.drop(labels='datetime', axis = 1)
    dropTestDatetimeTrain['time'] = time

    est.fit(dropTrainDatetimeTrain[predictors], dropTrainDatetimeTrain['casual'])
    casual = est.predict(dropTestDatetimeTrain[predictors])

    est.fit(dropTrainDatetimeTrain[predictors], dropTrainDatetimeTrain['registered'])
    registered = est.predict(dropTestDatetimeTrain[predictors])
    predCount = casual + registered

    #est.fit(dropTrainDatetimeTrain[predictors], dropTrainDatetimeTrain['count'])
    #predCount = est.predict(dropTestDatetimeTrain[predictors])
    #print(type(predCount))
    #print(predCount.shape)
    for i in range(len(predCount)):
        if predCount[i] < 0:
            predCount[i] = 1

    submission = pd.DataFrame({
        'datetime': datetime,
        'count': predCount
    })

    submission.to_csv('usingGBRT.csv', index=False)


if __name__ == '__main__':
    main()
