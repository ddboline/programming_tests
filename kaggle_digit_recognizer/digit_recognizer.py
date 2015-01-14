#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import pylab as pl
import numpy as np
import pandas as pd
from sklearn import ensemble, neighbors

def compare_rf_knn():
    train_samp = pd.read_csv('train.csv', header=0)
    test_samp = pd.read_csv('test.csv', header=0)

    indicies = np.random.permutation(np.arange(train_samp.shape[0]))
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

def digit_recognizer_submission():
    train_samp = pd.read_csv('train.csv', header=0)
    test_samp = pd.read_csv('test.csv', header=0)

    x_train = train_samp.iloc[:,1:]
    y_train = train_samp.iloc[:,0]
    
    knn = neighbors.KNeighborsClassifier()
    print knn.fit(x_train, y_train)

    x_test = test_samp
    y_test = knn.predict(x_test)

    with open('submit.csv', 'w') as outfile:
        outfile.write('ImageId,Label\n')
        for n, v in enumerate(y_test):
            outfile.write('%d,%d\n' % (n+1, v))

    return

def compare_algos():
    train_samp = pd.read_csv('train.csv', header=0)
    test_samp = pd.read_csv('test.csv', header=0)

    indicies = np.random.permutation(np.arange(train_samp.shape[0]))
    x_train = train_samp.iloc[indicies[:21000],1:]
    y_train = train_samp.iloc[indicies[:21000],0]
    x_test = train_samp.iloc[indicies[21000:],1:]
    y_test = train_samp.iloc[indicies[21000:],0]

    gammas = np.logspace(-6, -1, 10)
    svc = svm.SVC()
    clf = grid_search.GridSearchCV(estimator=svc, param_grid=dict(gamma=gammas), n_jobs=-1)

    classifier_dict = {
                'gridCV': clf,
                'linear_model': linear_model.LogisticRegression(fit_intercept=False,penalty='l1'),
                'linSVC': svm.LinearSVC(),
                'kNC5': KNeighborsClassifier(),
                'kNC6': KNeighborsClassifier(6),
                'SVC': SVC(kernel="linear", C=0.025),
                'DT': DecisionTreeClassifier(max_depth=5),
                'RF': RandomForestClassifier(n_estimators=200),
                'Ada': AdaBoostClassifier(),
                'Gauss': GaussianNB(),
                'LDA': LDA(),
                'QDA': QDA(),
                'GMM': GMM(),
                'SVC2': SVC(),
              }

    classifier_list = classifier_dict.values()
    classifier_scores = {}
    for k in classifier_dict:
        classifier_scores[k] = []

    def score_model(model):
        try:
            model.fit(x_train, y_train)
            #print xtest.shape, ytest.shape
            return model.score(x_test, y_test), model
        except:
            print model
            exit(0)

    for k, c in classifier_dict.iteritems():
        s, m = score_model(c)
        classifier_scores[k].append(s)

    for k, s in classifier_scores.items():
        print k, max(s)

    return

if __name__ == '__main__':
    digit_recognizer_submission()
