#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import matplotlib
matplotlib.use('Agg')
#import pylab as pl
import numpy as np
from sklearn import datasets
from sklearn import svm, neighbors

def iris_example():
    iris = datasets.load_iris()

    print('size',iris.target.size)
    perm = np.random.permutation(iris.target.size)

    clf = svm.LinearSVC()
    print(clf.fit(iris.data[perm][:100], iris.target[perm][:100]))
    #print(clf.predict([[5.0,  3.6,  1.3,  0.25]]))
    #print(clf.coef_)
    print(clf.score(iris.data[perm][100:], iris.target[perm][100:]))

    knn = neighbors.KNeighborsClassifier()
    print(knn.fit(iris.data, iris.target))
    #print(knn.predict([[5.0,  3.6,  1.3,  0.25]]))
    #print(clf.coef_)
    print(knn.score(iris.data[perm][100:], iris.target[perm][100:]))

def digits_example():
    digits = datasets.load_digits()
    print(digits.images.shape)

    #pl.imshow(digits.images[0], cmap=pl.cm.gray_r)
    #pl.savefig('digits_example.png')

    data = digits.images.reshape((digits.images.shape[0], -1))

    perm = np.random.permutation(digits.target.size)
    N = digits.target.size

    for kern in ['linear', 'poly', 'rbf']:
        svc = svm.SVC(kernel=str(kern))
        print(svc.fit(data[perm][:int(N*0.9)],
                      digits.target[perm][:int(N*0.9)]))
        print(svc.score(data[perm][int(N*0.9):],
                        digits.target[perm][int(N*0.9):]))
        del svc

iris_example()
digits_example()
