#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np

def prime_number_sieve0(N=100):
    is_prime = np.ones((N,), dtype=bool)
    is_prime[:2] = False
    N_max = int(np.sqrt(len(is_prime)))
    for i in range(2, N_max):
        for j in range(i, N_max):
            is_prime[i*j::i] = False
    a = list(np.nonzero(is_prime)[0])
    return a

def prime_number_sieve1(N=100):
    is_prime = np.ones((N,), dtype=bool)
    is_prime[:2] = False
    N_max = int(np.sqrt(len(is_prime)))
    for i in range(2, N_max):
        if is_prime[i] == True:
            for j in range(i, N):
                if i * j >= N:
                    break
                is_prime[i*j] = False
    a = list(np.nonzero(is_prime)[0])
    return a

print prime_number_sieve0(100)
#prime_number_sieve1(1000)
