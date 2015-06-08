#!/usr/bin/python3
try:
    from numba import jit
    from numba import int32
    def intarray():
        return int32[:]
except ImportError:
    def jit(arg):
        print('no jit')
        return arg
    def intarray():
        return []

@jit
def primes(kmax):  # The argument will be converted to int or raise a TypeError.
    #cdef int n, k, i  # These variables are declared with C types.
    #cdef int p[1000] # Another C type
    primes = intarray()
    largest_prime = 1
    n_primes = 0
    prime_candidate = 2
    while n_primes < kmax:
        i = 0
        while i < n_primes and prime_candidate % primes[i] != 0:
            i += 1
        if i == n_primes:
            primes.append(prime_candidate)
            n_primes += 1
            largest_prime = prime_candidate
        prime_candidate += 1
    return largest_prime
