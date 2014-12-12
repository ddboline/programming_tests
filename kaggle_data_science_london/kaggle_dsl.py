#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import pylab as pl
import numpy as np
from sklearn import linear_model
from sklearn import svm, neighbors , svm , grid_search
import csv
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

def kaggle_submit():
    train_file = open( 'train.csv' , 'r' )
    trainLabels_file = open( 'trainLabels.csv' , 'r' )
    
    xtrain = []
    ytrain = []
    
    for line in csv.reader( train_file ):
        xtrain.append( map( float , line  ) )

    for line in trainLabels_file:
        ytrain.append( int( line.strip() ) )
    
    xtrain = np.array( xtrain )
    ytrain = np.array( ytrain )

    model = KNeighborsClassifier()
    print model.fit(xtrain,ytrain)

    test_file = open( 'test.csv' , 'r' )
    
    xtest = []
    for line in csv.reader( test_file ):
        xtest.append( map( float , line ) )
    
    ytest = model.predict( xtest )

    with open('submit.csv', 'w') as outfile:
        outfile.write( 'Id,Solution\n' )
        ow = csv.writer( outfile )
        ow.writerow( [ 'Id' , 'Solution' ] )
        for n , out in enumerate(ytest):
            ow.writerow( [ n+1 , out ] )

def kaggle_dsl_scoring():
    train_file = open( 'train.csv' , 'r' )
    trainLabels_file = open( 'trainLabels.csv' , 'r' )
    
    xt = []
    yt = []
    
    for line in csv.reader( train_file ):
        xt.append( map( float , line  ) )

    for line in trainLabels_file:
        yt.append( int( line.strip() ) )
    
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
                'QDA': QDA() }

    classifier_list = classifier_dict.values()
    classifier_scores = {}
    for k in classifier_dict:
        classifier_scores[k] = []

    for idx in range(500):
        randperm = np.random.permutation( np.arange( len(xt) ) )
        xt = np.array( xt )
        yt = np.array( yt )
        xtrain = xt[randperm[:500]]
        ytrain = yt[randperm[:500]]
        xtest = xt[randperm[500:]]
        ytest = yt[randperm[500:]]
    
        def score_model( model ):
            model.fit(xtrain, ytrain)
            # if hasattr( model, 'coef_' ):
                # print model.coef_[0]
            return model.score(xtest, ytest) , model
    
        for k , c in classifier_dict.iteritems():
            s , m = score_model( c )
            classifier_scores[k].append( s )

    for k , s in classifier_scores.items():
        print s , k
    
if __name__ == '__main__':
    kaggle_dsl_scoring()
    kaggle_submit()