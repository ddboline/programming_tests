#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import pylab as pl
import numpy as np
from sklearn import datasets, svm, linear_model, grid_search

def grid_search_test():
    digits = datasets.load_digits()
    data = digits.images.reshape((digits.images.shape[0], -1))

    gammas = np.logspace(-6, -1, 10)
    svc = svm.SVC()
    clf = grid_search.GridSearchCV(estimator=svc, param_grid=dict(gamma=gammas), n_jobs=-1)
    print clf.fit(data[:1000], digits.target[:1000])
    print clf.best_score_
    print clf.best_estimator_.gamma

def cross_validated_estimators():
    lasso = linear_model.LassoCV()
    diabetes = datasets.load_diabetes()
    X_diabetes = diabetes.data
    y_diabetes = diabetes.target
    print lasso.fit(X_diabetes, y_diabetes)

    # The estimator chose automatically its lambda:
    print lasso.alpha_

grid_search_test()
cross_validated_estimators()
