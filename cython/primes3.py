#!/usr/bin/python
from numba import jit, int64

@jit
def primes(kmax):  # The argument will be converted to int or raise a TypeError.
    primes_ = []
    primes_size = 0
    largest_prime = 1
    n_primes = 0
    prime_candidate = 2
    while n_primes < kmax:
        i = 0
        while i < n_primes and prime_candidate % primes_[i] != 0:
            i += 1
        if i == n_primes:
            if i == primes_size:
                primes_.extend(((primes_size+1)*2)*[0])
                primes_size = len(primes_)
            primes_[i] = prime_candidate
            n_primes += 1
            largest_prime = prime_candidate
        prime_candidate += 1
    return largest_prime
