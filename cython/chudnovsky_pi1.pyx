#!/usr/bin/python
# # # cython: profile=True

cpdef int fact(int n):
    cdef int f = 1
    cdef int idx = 1
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        for idx in xrange(1, n+1):
            f *= idx
        return f

cpdef double chudnovsky_denom(int k):
    cdef double denom = fact(3 * k)
    denom *= (fact(k))**3
    denom *= 640320**(3.*k + 3./2.)
    return denom

cpdef int chudnovsky_num(int k):
    cdef int numerator = 163 * 3344418 * k + 13591409
    numerator *= fact(6 * k)
    numerator *= (-1)**k
    return numerator

cpdef double chudnovsky_term(int k):
    return float(chudnovsky_num(k)) / float(chudnovsky_denom(k))

cpdef double calc_chudnovsky_pi(int k):
    cdef double pi_inv = 0.
    cdef int idx = 0
    for idx in xrange(0, k+1):
        pi_inv += chudnovsky_term(k)
    pi_inv *= 12.
    return 1./pi_inv
