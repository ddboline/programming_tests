#!/usr/bin/python
# -*- coding: utf-8 -*-

def fib_func(n):
    if type(n) != int or n < 0:
        exit(0)
    if n == 0:
        return 1
    elif n == 1:
        return 1
    elif n >= 2:
        return fib_func(n-1) + fib_func(n-2)

if __name__ == '__main__':
    for n in range(0, 20):
        print(n, fib_func(n))
