#!/usr/bin/python

try:
    from numba import jit
except ImportError:
    from util import jit

@jit
def approx_pi(n=10**7):
    val = 0.
    k = 1
    while k < n+1:
        val += 1./k**2
        k += 1
    return (6. * val)**.5
