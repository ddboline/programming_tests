#!/usr/bin/python
# # # cython: profile=True

#cimport cython

#@cython.profile(False)
#cdef double recip_square( int i ) :
    #return 1./i**2

def approx_pi( int n = 10**7 ) :
    cdef double val = 0.
    cdef double kfloat = 1.
    cdef double k = 1.
    while k < n+1 :
        val += 1. / k**2
        k += 1.
    return ( 6. * val )**.5
