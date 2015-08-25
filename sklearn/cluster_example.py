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
from sklearn import datasets, cluster

def kmeans():
    iris = datasets.load_iris()
    k_means = cluster.KMeans(n_clusters=3)
    print(k_means.fit(iris.data))
    print(k_means.labels_[::10])
    print(iris.target[::10])

def posterize():
    from scipy import misc
    lena = misc.lena().astype(np.float32)
    pl.imshow(lena, cmap=pl.cm.gray)
    pl.savefig('lena.png')

    X = lena.reshape((-1, 1)) # We need an (n_sample, n_feature) array
    k_means = cluster.KMeans(n_clusters=5)
    k_means.fit(X)

    values = k_means.cluster_centers_.squeeze()
    labels = k_means.labels_
    lena_compressed = np.choose(labels, values)
    lena_compressed.shape = lena.shape

    pl.imshow(lena_compressed, cmap=pl.cm.gray)
    pl.savefig('lena_compressed.png')


kmeans()
posterize()
