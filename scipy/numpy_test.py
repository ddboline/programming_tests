#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np

def examples() :
    c = np.array([[[1], [2]], [[3], [4]]])
    print c

    a = np.ones((3, 3))
    print a

    c = np.eye(3)
    print c

    d = np.diag(np.array([1, 2, 3, 4]))
    print d

    a = np.random.rand(4)
    print a

def prime_number_sieve() :
    is_prime = np.ones( (100,) , dtype = bool )
    is_prime[:2] = False
    N_max = int( np.sqrt( len(is_prime) ) )
    for j in range( 2 , N_max ) :
        is_prime[2*j::j] = False
    a = list( np.nonzero( is_prime )[0] )
    print a , type(a)
    b = [ N for N , a in filter( lambda a : a[1] , enumerate( is_prime ) ) ]
    print b , type(b)

prime_number_sieve()
