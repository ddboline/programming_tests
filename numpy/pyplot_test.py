#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def one_dim_plot():
    x = np.linspace(0, 3, 20)
    y = np.random.randn(20)
    plt.plot(x, y)
    plt.savefig('one_dim_plot.png', format='png')
    plt.clf()

def two_dim_plot():
    image = np.random.rand(30, 30)
    plt.imshow(image, cmap=plt.cm.hot)
    plt.colorbar()
    plt.savefig('two_dim_plot.png', format='png')
    plt.clf()

def gaussian_hist():
    x0 = np.random.poisson(lam=1., size=10000)
    x1 = np.random.poisson(lam=10., size=10000)
    x2 = np.random.poisson(lam=20., size=10000)
    plt.hist((x0, x1, x2), bins=np.linspace(0, 50, 50), histtype='step',)
    plt.savefig('gaussian_hist.png', format='png')
    plt.clf()

def sin_plot():
    x = np.linspace(-np.pi, np.pi, 1000)
    y = np.sin(x)
    plt.plot(x, y)
    plt.savefig('sin_plot.png', format='png')
    plt.clf()

one_dim_plot()
two_dim_plot()
gaussian_hist()
sin_plot()
