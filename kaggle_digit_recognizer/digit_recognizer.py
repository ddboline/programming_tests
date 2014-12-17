#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import pylab as pl
import numpy as np
import pandas as pd
from sklearn import ensemble, neighbors

def digit_recognizer():
    train_samp = pd.read_csv('train.csv', header=0)

    indicies = np.random.permutation( np.arange(train_samp.shape[0]) )
    x_train = train_samp.iloc[indicies[:21000],1:]
    y_train = train_samp.iloc[indicies[:21000],0]
    x_test = train_samp.iloc[indicies[21000:],1:]
    y_test = train_samp.iloc[indicies[21000:],0]
    
    forest = ensemble.RandomForestClassifier()
    print forest.fit(x_train, y_train)
    print forest.score(x_test, y_test)
    
    
    knn = neighbors.KNeighborsClassifier()
    print knn.fit(x_train, y_train)
    print knn.score(x_test, y_test)
    
    
    return

if __name__ == '__main__':
    digit_recognizer()