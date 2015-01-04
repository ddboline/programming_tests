#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import pylab as pl
import numpy as np
from sklearn import linear_model
from sklearn import svm, neighbors, svm, grid_search
import csv, os, time
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.mixture import GMM
from sklearn.decomposition import PCA

def kaggle_submit(model, xtrain, ytrain, pca=None):
    print model.fit(xtrain,ytrain)

    xtest = pd.read_csv('test.csv', header=None).as_matrix()
    if pca:
        xtest = pca.transform(xtest)
    ytest = model.predict(xtest)

    with open('submit.csv', 'w') as outfile:
        ow = csv.writer(outfile)
        ow.writerow(['Id', 'Solution'])
        for n, out in enumerate(ytest):
            ow.writerow([n+1, out])

def kaggle_dsl_scoring(gauss_train_size=1000):
    xt = pd.read_csv('train.csv', header=None).as_matrix()
    yt = pd.read_csv('trainLabels.csv', header=None).as_matrix()
    xtest = pd.read_csv('test.csv', header=None).as_matrix()

    pca = None
    pca = PCA(n_components=12)
    pca.fit(xtest)
    xtp = pca.transform(xt)

    i0 = np.argwhere(yt==0)[:, 0]
    i1 = np.argwhere(yt==1)[:, 0]
    x0_mean = np.mean(xtp[i0,:], axis=0)
    x0_cov = np.cov(xtp[i0,:], rowvar=0)
    x1_mean = np.mean(xtp[i1,:], axis=0)
    x1_cov = np.cov(xtp[i1,:], rowvar=0)

    #gauss_train_size = 7000
    xtg0 = np.random.multivariate_normal(x0_mean, x0_cov, gauss_train_size)
    xtg1 = np.random.multivariate_normal(x1_mean, x1_cov, gauss_train_size)

    xt = np.r_[xtg0, xtg1]
    yt = np.r_[[0]*gauss_train_size, [1]*gauss_train_size]

    gammas = np.logspace(-6, -1, 10)
    svc = svm.SVC()
    clf = grid_search.GridSearchCV(estimator=svc, param_grid=dict(gamma=gammas), n_jobs=-1)

    classifier_dict = {
                #'gridCV': clf,
                #'linear_model': linear_model.LogisticRegression(fit_intercept=False,penalty='l1'),
                #'linSVC': svm.LinearSVC(),
                #'kNC5': KNeighborsClassifier(),
                #'kNC6': KNeighborsClassifier(6),
                #'SVC': SVC(kernel="linear", C=0.025),
                #'DT': DecisionTreeClassifier(max_depth=5),
                'RF': RandomForestClassifier(n_estimators=200),
                #'Ada': AdaBoostClassifier(),
                #'Gauss': GaussianNB(),
                #'LDA': LDA(),
                #'QDA': QDA(),
                #'GMM': GMM(),
                #'SVC2': SVC(),
               }

    classifier_list = classifier_dict.values()
    classifier_scores = {}
    for k in classifier_dict:
        classifier_scores[k] = []

    for idx in range(1):
        randperm = np.random.permutation(np.arange(xt.shape[0]))
        xtrain = xt[randperm[::2],:]
        ytrain = yt[randperm[::2]]
        xtest = xt[randperm[1::2],:]
        ytest = yt[randperm[1::2]]

        #pca.fit(xt)
        #xtrain = pca.transform(xtrain)
        #xtest = pca.transform(xtest)

        #gmm = GMM()
        #gmm.fit(xt)
        #xtrain = gmm.transform(xtrain)
        #xtest = gmm.transform(xtest)

        def score_model(model):
            try:
                model.fit(xtrain, ytrain)
                #print xtest.shape, ytest.shape
                return model.score(xtest, ytest), model
            except:
                print model
                exit(0)

        for k, c in classifier_dict.iteritems():
            s, m = score_model(c)
            classifier_scores[k].append(s)

    ksarr = sorted([(ks[1], ks[0]) for ks in classifier_scores.items()])
    smarr = []
    for s, k in ksarr:
        #print np.max(s) c, k
        smarr.append(np.max(s))

    return classifier_dict[ksarr[-1][1]], xt, yt, pca, max(smarr)

if __name__ == '__main__':
    try:
        N = int(os.sys.argv[1])
    except:
        N = 0
    times = [time.clock()]
    model, x, y, pca, sc = kaggle_dsl_scoring(gauss_train_size=N)
    times.append(time.clock())
    dt = times[-1]-times[-2]
    print N, dt, sc
    kaggle_submit(model, x, y, pca)

    #times = [time.clock()]
    #with open('timing.txt','w') as timefile:
        #for N in [1000, 2000, 3000, 4000, 5000, 7000, 10000, 15000]:
            #model, x, y, pca, sc = kaggle_dsl_scoring(gauss_train_size=N)
            #times.append(time.clock())
            #dt = times[-1]-times[-2]
            #print N, dt, sc
            #timefile.write('%d %d %f\n' % (N, dt, sc))
            #timefile.flush()
