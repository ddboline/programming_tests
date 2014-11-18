#!/usr/bin/python

import pyximport
pyximport.install()

import primes
import primes2
import time

t0 = time.clock()
print primes.primes( 10000 )
t1 = time.clock()
print primes2.primes( 10000 )
t2 = time.clock()

print t2-t1 , t1-t0