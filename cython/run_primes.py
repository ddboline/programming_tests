#!/usr/bin/python3

import pyximport
pyximport.install()

import primes0
import primes1
import primes2
import primes3

import time
from subprocess import call

ts = []

ts.append(time.clock())
print(primes0.primes(10000))
ts.append(time.clock())
print(primes1.primes(10000))
ts.append(time.clock())
print(primes2.primes(10000))
ts.append(time.clock())
print(primes3.primes(10000))
ts.append(time.clock())
call('./primes 10000', shell=True)
ts.append(time.clock())

for i in range(0,len(ts)-1):
    print('timing:', ts[i+1] - ts[i])
