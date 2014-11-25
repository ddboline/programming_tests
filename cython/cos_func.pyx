#!/usr/bin/python

from __future__ import division
import numpy as np
cimport numpy as np

cdef extern from 'math.h' :
    double cos(double arg)

def cos_func( arg ) :
    return cos(arg)