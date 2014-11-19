#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

def one_dim_plot() :
    x = np.linspace( 0 , 3 , 20 )
    y = np.random.randn( 20 )
    plt.plot( x , y )
    plt.show()

def two_dim_plot() :
    image = np.random.rand( 30 , 30 )
    plt.imshow( image , cmap = plt.cm.hot )
    plt.colorbar()
    plt.show()

def gaussian_hist() :
    x = np.random.poisson( lam=1. , size=10000 )
    plt.hist( x , bins = np.linspace( -10 , 30 , 40 ) , histtype='stepfilled', )
    plt.show()

def sin_plot() :
    x = np.linspace( -np.pi , np.pi , 1000 )
    y = np.sin( x )
    plt.plot( x , y )
    plt.show()

#one_dim_plot()
#two_dim_plot()
#gaussian_hist()
sin_plot()
