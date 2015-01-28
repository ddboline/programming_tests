#!/usr/bin/python

import os

cpdef pi_wallis(int n = 10):
    cdef double val = 2.
    cdef double preval = 0.
    cdef double i = 1
    for i in xrange(1,n):
        val *= (4.*i**2) / (4.*i**2 - 1.)
    return val
