#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import matplotlib
matplotlib.use('Agg')
import pylab as pl
import numpy as np
from sklearn import datasets, decomposition

def pca_example():
    iris = datasets.load_iris()
    pca = decomposition.PCA(n_components=2)
    print(pca.fit(iris.data))
    X = pca.transform(iris.data)
    pl.scatter(X[:, 0], X[:, 1], c=iris.target)
    pl.savefig('pca_example.png')

pca_example()
