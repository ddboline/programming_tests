#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import pylab as pl
import numpy as np
from sklearn import linear_model
from sklearn import svm, neighbors , svm , grid_search
import csv
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

def kaggle_submit( model , xtrain , ytrain , pca ):
    print model.fit(xtrain,ytrain)

    xtest = pd.read_csv('test.csv', header=None).as_matrix()
    ytest = model.predict( xtest )
    
    if pca:
        xtest = pca.transform(xtest)

    with open('submit.csv', 'w') as outfile:
        outfile.write( 'Id,Solution\n' )
        ow = csv.writer( outfile )
        ow.writerow( [ 'Id' , 'Solution' ] )
        for n , out in enumerate(ytest):
            ow.writerow( [ n+1 , out ] )

def kaggle_dsl_scoring():
    xt = pd.read_csv('train.csv', header=None).as_matrix()
    yt = pd.read_csv('trainLabels.csv', header=None).as_matrix()
    xtest = pd.read_csv('test.csv', header=None).as_matrix()
    
    print np.mean(xt[yt==0], axis=0)
    print np.cov(xt[yt==0])
    print np.mean(xt[yt==1])
    print np.cov(xt[yt==1])
    
    #pca = PCA(n_components=12)
    #pca.fit(xt)
    #xtp = pca.transform(xt)
    
    gammas = np.logspace(-6, -1, 10)
    svc = svm.SVC()
    clf = grid_search.GridSearchCV(estimator=svc, param_grid=dict(gamma=gammas), n_jobs=-1)

    classifier_dict = { 'gridCV': clf,
                'linear_model': linear_model.LogisticRegression(fit_intercept=False,penalty='l1'),
                'linSVC': svm.LinearSVC(),
                'kNC5': KNeighborsClassifier(),
                'kNC6': KNeighborsClassifier(6),
                'SVC': SVC(kernel="linear", C=0.025),
                'SVC2': SVC(gamma=2, C=1),
                'DT': DecisionTreeClassifier(max_depth=5),
                'RF': RandomForestClassifier(),
                'Ada': AdaBoostClassifier(),
                'Gauss': GaussianNB(),
                'LDA': LDA(),
                'QDA': QDA(),
                #'GMM': GMM()
                }

    classifier_list = classifier_dict.values()
    classifier_scores = {}
    for k in classifier_dict:
        classifier_scores[k] = []
    
    for idx in range(1):
        randperm = np.random.permutation( np.arange( xt.shape[0] ) )
        xtrain = xt[randperm[:500],:]
        ytrain = yt[randperm[:500],0]
        xtest = xt[randperm[500:],:]
        ytest = yt[randperm[500:],0]
    
        #pca = PCA(whiten=True)
        #pca.fit(xt)
        #xtrain = pca.transform(xtrain)
        #xtest = pca.transform(xtest)
    
        #gmm = GMM()
        #gmm.fit(xt)
        #xtrain = gmm.transform(xtrain)
        #xtest = gmm.transform(xtest)
    
        def score_model( model ):
            model.fit(xtrain, ytrain)
            # if hasattr( model, 'coef_' ):
                # print model.coef_[0]
            return model.score(xtest, ytest) , model
    
        for k , c in classifier_dict.iteritems():
            s , m = score_model( c )
            classifier_scores[k].append( s )

    ksarr = sorted( [ (ks[1] , ks[0]) for ks in classifier_scores.items() ] )
    for s , k in ksarr:
        print np.mean(s) , k
    
    return classifier_dict[ksarr[-1][1]] , xt , yt , pca
    
if __name__ == '__main__':
    model , x , y , pca = kaggle_dsl_scoring()
    kaggle_submit( model , x , y , pca )
