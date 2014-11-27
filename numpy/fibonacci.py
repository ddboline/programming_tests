#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

#for n in range(0, int(os.sys.argv[1])):
    #print n, fib(n)

fib_v_n0 = 0
fib_v_n1 = 0
for n in range(0, int(os.sys.argv[1])):
    if n == 0:
        fib_v0 = 0
        fib_v1 = 0
    elif n == 1:
        fib_v0 = 0
        fib_v1 = 1
    else:
        fib = fib_v1 + fib_v0
        fib_v0 = fib_v1
        fib_v1 = fib
    print n, fib_v1, fib_v0