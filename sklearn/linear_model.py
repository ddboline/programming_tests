#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import pylab as pl
import numpy as np
from sklearn import datasets, linear_model

def sparse_model():
    diabetes = datasets.load_diabetes()
    diabetes_X_train = diabetes.data[:-20]
    diabetes_X_test  = diabetes.data[-20:]
    diabetes_y_train = diabetes.target[:-20]
    diabetes_y_test  = diabetes.target[-20:]

    regr = linear_model.Lasso(alpha=.3)
    print regr.fit(diabetes_X_train, diabetes_y_train)
    print regr.coef_
    print regr.score(diabetes_X_test, diabetes_y_test)
    
    lin = linear_model.LinearRegression()
    print lin.fit(diabetes_X_train, diabetes_y_train)
    print lin.coef_
    print lin.score(diabetes_X_test, diabetes_y_test)
    
sparse_model()