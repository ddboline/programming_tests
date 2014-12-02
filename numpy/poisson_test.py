#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as plt

def cent_lim_theorem_test(n = 10e5):
    p0 = np.random.poisson(lam = 12., size = n)
    p1 = np.random.poisson(lam = 8., size = n)
    p2 = np.random.poisson(lam = 20., size = n)
    p3 = p0+p1

    print (p2.mean() - p0.mean() - p1.mean()) / p2.std(), (p2.mean() - p3.mean()) / p2.std()
    #print p0.mean(), p1.mean(), p2.mean(), p3.mean()
    #print p0.std(), p1.std(), p2.std(), p3.std()
    #plt.clf()
    #plt.hist(p0, bins=50, range=(0.,50.), histtype='step')
    #plt.hist(p1, bins=50, range=(0.,50.), histtype='step')
    #plt.hist(p2, bins=50, range=(0.,50.), histtype='step')
    #plt.hist(p3, bins=50, range=(0.,50.), histtype='step')
    #plt.savefig('poisson_test.png')

for n in [10e2, 10e3, 10e4, 10e5]:
    t0 = time.clock()
    cent_lim_theorem_test(n)
    t1 = time.clock()
    print n, t1-t0
