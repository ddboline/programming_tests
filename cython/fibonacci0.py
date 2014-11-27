#!/usr/bin/python

import os

def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def next_fibonacci():
    n = 0
    fib0 = 0
    fib1 = 1
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
