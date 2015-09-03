#!/usr/bin/python

cpdef int primes(int kmax):  # The argument will be converted to int or raise a TypeError.
    cdef int n, k, i  # These variables are declared with C types.
    cdef int p[10000]  # Another C type
    cdef int result = 0  # A Python type
    if kmax > 10000:
        kmax = 10000
    k = 0
    n = 2
    while k < kmax:
        i = 0
        while i < k and n % p[i] != 0:
            i += 1
        if i == k:
            p[k] = n
            k += 1
            result = n
        n += 1
    return result
