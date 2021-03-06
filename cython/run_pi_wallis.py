#!/usr/bin/python

import pyximport
pyximport.install()

import pi_wallis0
import pi_wallis1
import pi_wallis2

import time
import math

N = 10**6

print(math.pi)
t0 = time.clock()
print(pi_wallis0.pi_wallis(N))
t1 = time.clock()
print(pi_wallis1.pi_wallis(N))
t2 = time.clock()
print(pi_wallis2.pi_wallis(N))
t3 = time.clock()

print('timing:', t1-t0, t2-t1, t3-t2)
