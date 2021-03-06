#!/usr/bin/env python3
# coding=utf-8

import numpy as np


def loadDataSet():
    return [[1,3,4], [2,3,5], [1,2,3,5], [2,5]]


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    return map(frozenset, C1)


def scanD(D, Ck, minSupport):
    D = list(D)
    Ck = list(Ck)
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.get(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(list(D)))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


if __name__ == "__main__":
    dataSet = loadDataSet()
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, suppData0 = scanD(D, C1, 0.5)
    print(L1, suppData0)