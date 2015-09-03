#!/usr/bin/python

import os

def fibonacci(int n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def next_fibonacci():
    cdef int n = 0
    cdef int fib0 = 0
    cdef int fib1 = 1
    while True:
        if n == 0:
            yield n, 0
        elif n == 1:
            yield n, 1
        else:
            fib = fib1 + fib0
            fib0 = fib1
            fib1 = fib
            yield n, fib
        n += 1
