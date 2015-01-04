#!/usr/bin/python

import pyximport
pyximport.install()

import fibonacci0
import fibonacci1

import time
import math

N = 30

results = []
for n in range(0, 20):
    t0 = time.clock()
    n0 = fibonacci0.fibonacci(n)
    t1 = time.clock()
    n1 = fibonacci1.fibonacci(n)
    t2 = time.clock()

    print 'timing:', n, t1-t0, t2-t1
    results.append([n, t1-t0, t2-t1])

t0 = time.clock()
for n, f in fibonacci0.next_fibonacci():
    if n == 20:
        break
    t1 = time.clock()

    print n, t1-t0
    results[n].append(t1-t0)
    t0 = time.clock()


for n, t0, t1, t2 in results:
    print 'timing:', n, t0, t1, t2
