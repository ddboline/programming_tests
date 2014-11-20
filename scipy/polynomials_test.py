#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use( 'Agg' )
import matplotlib.pyplot as plt

def first() :
    p = np.poly1d( [3,2,1] )
    print p(0)
    print p.roots
    print p.order
    
    x = np.linspace( 0 , 1 , 20 )
    y = np.cos(x) + 0.3*np.random.rand(20)
    pfit , cov = np.polyfit( x , y , 3 , cov=True)
    print cov
    p = np.poly1d( pfit )
    t = np.linspace( 0 , 1 , 200 )
    plt.plot( x , y , 'o' , t , p(t) , '-' )
    plt.savefig( 'polynomials_test.png' )

def second() :
    p = np.polynomial.Polynomial( [ -1 , 2 , 3 ] )
    print p(0)
    print p.roots()
    print p.degree()

def third() :
    x = np.linspace( -1 , 1 , 2000 )
    y = np.cos(x) + 0.3*np.random.rand(2000)
    p = np.polynomial.Chebyshev.fit( x , y , 10 )
    t = np.linspace( -1 , 1 , 200 )
    plt.plot( x , y , 'r.' )
    plt.plot( t , p(t) , 'k-' , lw=3 )
    plt.savefig( 'Chebyschev.png' )

#first()
#second()
third()
