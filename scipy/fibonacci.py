#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def fib( n ) :
    if n == 0 :
        return 0
    if n == 1 :
        return 1
    return fib(n-1) + fib(n-2)

for n in range( 0 , int(os.sys.argv[1]) ) :
    print n , fib(n)