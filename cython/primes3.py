#!/usr/bin/python3
from numba import jit
import numpy as np

@jit(int64(int64))
def primes(kmax):  # The argument will be converted to int or raise a TypeError.
    #cdef int n, k, i  # These variables are declared with C types.
    #cdef int p[1000] # Another C type
    primes_ = np.array([], dtype=np.int64)
    largest_prime = 1
    n_primes = 0
    prime_candidate = 2
    while n_primes < kmax:
        i = 0
        while i < n_primes and prime_candidate % primes_[i] != 0:
            i += 1
        if i == n_primes:
            primes_.append(prime_candidate)
            n_primes += 1
            largest_prime = prime_candidate
        prime_candidate += 1
    return largest_prime
