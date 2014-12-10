#!/usr/bin/python

# from __future__ import division
# from libc.math cimport cos

cdef extern from "math.h":
    double cos( double x )

cpdef double cos_func(double arg) :
    return cos(arg)
