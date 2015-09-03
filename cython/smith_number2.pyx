#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:06:04 2015

@author: ddboline
"""
from libcpp.vector cimport vector

def prime_factors(int pval):
    cdef int cval = pval
    cdef vector[int] factors
    cdef vector[int] p
    cdef int k = 0
    cdef int n = 2
    while k < cval:
        i = 0
        while i < k and n % p[i] != 0:
            i += 1
        if i == k:
            p.push_back(n)
            k += 1
            while cval % n == 0:
                factors.push_back(n)
                cval /= n
        if k*k > cval:
            factors.push_back(cval)
            break
        n += 1
    return factors

def sum_of_digits(int number):
    cdef int sum_of_digit = 0
    cdef long divisor = 1
    while divisor < number:
        sum_of_digit += (number/divisor) % 10
        divisor *= 10
    return sum_of_digit

def smith_number(int number):
    cdef int sum_of_prime_dig = 0
    primes = prime_factors(number)
    for _prime in primes:
        sum_of_prime_dig += sum_of_digits(_prime)
    return int(sum_of_prime_dig == sum_of_digits(number))
