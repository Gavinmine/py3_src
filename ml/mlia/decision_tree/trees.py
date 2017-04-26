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


import operator
import numpy as np
from math import log

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}

    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0

    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def createDataSet():
    dataSet = [[1, 1, 'yes'],
              [1, 1, 'yes'],
              [1, 0, 'no'],
              [0, 1, 'no'],
              [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def createWaterDataSet():
    dataSet = np.array([['nan', 'juanshuo', 'zhouxiang', 'qingxi', 'aoxian', 'yinghua', 1],
                        ['wuhei', 'juanshuo', 'chenmen', 'qingxi', 'aoxian', 'nan', 1],
                        ['wuhei', 'juanshuo', 'nan', 'qingxi', 'aoxian', 'yinghua', 1],
                        ['qinglv', 'juanshuo', 'chenmen', 'qingxi', 'aoxian', 'yinghua', 1],
                        ['nan', 'juanshuo', 'zhouxiang', 'qingxi', 'aoxian', 'yinghua', 1],
                        ['qinglv', 'shaojuan', 'zhouxiang', 'qingxi', 'nan', 'ruanlian', 1],
                        ['wuhei', 'shaojuan', 'zhouxiang', 'shaohu', 'shaoao', 'ruanlian', 1],
                        ['wuhei', 'shaojuan', 'zhouxiang', 'nan', 'shaoao', 'yinghua', 1],
                        ['wuhei', 'nan', 'chenmen', 'shaohu', 'shaoao', 'yinghua', 0],
                        ['qinglv', 'yingting', 'qingcui', 'nan', 'pingtan', 'ruanlian', 0],
                        ['qianbai', 'yingting', 'qingcui', 'mohu', 'pingtan', 'nan', 0],
                        ['qianbai', 'juanshuo', 'nan', 'mohu', 'pingtan', 'ruanlian', 0],
                        ['nan', 'shaojuan', 'zhouxiang', 'shaohu', 'aoxian', 'yinghua', 0],
                        ['qianbai', 'shaojuan', 'chenmen', 'mohu', 'aoxian', 'yinghua', 0],
                        ['wuhei', 'shaojuan', 'zhouxiang', 'qingxi', 'nan', 'ruanlian', 0],
                        ['qianbai', 'juanshuo', 'zhouxiang', 'mohu', 'pingtan', 'yinghua', 0],
                        ['qinglv', 'nan', 'chenmen', 'shaohu', 'shaoao', 'yinghua', 0]], dtype='U75')
    labels = np.array(['seze', 'gendi', 'qiaosheng', 'wenli', 'jibu', 'cugan'], dtype='U75')
    return dataSet, labels


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def removeColumnDataSet(dataSet, col, value):
    retDataSet = dataSet[dataSet[:,col] == value]
    retDataSet = np.delete(retDataSet, col, axis = 1)
    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def chooseBestFeatureToSplitWithMissed(dataSet):
    numFeatures = len(dataSet[0]) - 1
    bestInfoGain = -100.0
    bestFeature = -1
    totalLen = float(len(dataSet))
    for i in range(numFeatures):
        useDataSet = dataSet[dataSet[:,i] != 'nan']
        featList = useDataSet[:,i]
        useLen = float(len(useDataSet))
        baseProb = useLen/totalLen
        baseEntropy = calcShannonEnt(useDataSet)
        #print('baseEntropy:', baseEntropy)
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = removeColumnDataSet(useDataSet, i, value)
            prob = len(subDataSet)/float(len(useDataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
            #print('newEntropy:', newEntropy)
        infoGain = baseEntropy - newEntropy
        infoGain = baseProb * infoGain
        #print('infoGain:', infoGain)
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del (labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree


def createTreeWithArray(dataSet, labels):
    classList = dataSet[:,-1]
    if len(classList[classList==classList[0]]) == len(classList):
        return classList[0]
    print('len(dataSet[0]):', len(dataSet[0]))
    if len(dataSet[0]) == 1:
        print('majorityCnt:', majorityCnt(classList))
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplitWithMissed(dataSet)
    bestFeatLabel = labels[bestFeat]
    print('bestFeat:%d, bestFeatLabel:%s' % (bestFeat, bestFeatLabel))
    myTree = {bestFeatLabel:{}}
    labels = np.delete(labels, bestFeat, axis = 0)
    print('len(labels):', len(labels))
    featValues = dataSet[:,bestFeat]
    uniqueVals = set(featValues)
    uniqueVals.discard('nan')
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTreeWithArray(removeColumnDataSet(dataSet, bestFeat, value), subLabels)
    return myTree
