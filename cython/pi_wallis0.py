#!/usr/bin/python

import os

def pi_wallis(n=10):
    val = 2.
    for i in range(1, n):
        val *= (4.*i**2) / (4.*i**2 - 1.)
    return val
