#!/usr/bin/python3
from numba import jit

@jit
def fact(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        f = 1
        for idx in range(1, n+1):
            f *= idx
        return f

@jit
def chudnovsky_denom(k):
    denom = fact(3 * k)
    denom *= (fact(k))**3
    denom *= 640320**(3.*k + 3./2.)
    return denom

@jit
def chudnovsky_num(k):
    numerator = 163 * 3344418 * k + 13591409
    numerator *= fact(6 * k)
    numerator *= (-1)**k
    return float(numerator)

@jit
def chudnovsky_term(k):
    return chudnovsky_num(k) / chudnovsky_denom(k)

@jit
def calc_chudnovsky_pi(k):
    pi_inv = 0.
    for idx in range(0, k+1):
        pi_inv += chudnovsky_term(k)
    pi_inv *= 12.
    return 1./pi_inv
