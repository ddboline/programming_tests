#!/usr/bin/python

import os

try:
    from numba import jit
except ImportError:
    from util import jit

@jit
def pi_wallis(n=10):
    val = 2.
    for i in range(1, n):
        val *= (4.*i**2) / (4.*i**2 - 1.)
    return val
