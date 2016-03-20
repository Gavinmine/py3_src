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
from sklearn.linear_model import LogisticRegression

hand = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

#alg_list = []
predictors = []
#proba_list = []
#preds = []

count = 28*28

for i in range(count):
    pixel = 'pixel'+str(i)
    predictors.append(pixel)

alg = LogisticRegression(random_state=1)
alg.fit(hand[predictors], hand["label"])
predicts = alg.predict(test[predictors])

#for i in range(10):
#    alg = LogisticRegression(random_state=1)
#    alg.fit(hand[predictors], hand['label'] == i)
#    proba = alg.predict_proba(test[predictors])
#    #alg_list.append(alg)
#    proba_list.append(proba)
#
#for i in range(len(test)):
#    max_proba = 0
#    pred = -1
#    for proba in proba_list:
#        if proba[i][1] > max_proba:
#            max_proba = proba[i][1]
#            pred = proba_list.index(proba)
#
#    preds.append(pred)
#
#
print(predicts)
submission = pd.DataFrame({
    "ImageId": range(1, len(test)+1),
    "label": predicts
})

submission.to_csv('kaggle.csv', index=False)
