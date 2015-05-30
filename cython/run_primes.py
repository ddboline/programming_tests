#!/usr/bin/python3

import pyximport
pyximport.install()

import primes0
import primes2
import time, os

os.system('gcc primes.c -o primes')

ts = []

ts.append(time.clock())
print(primes0.primes(10000))
ts.append(time.clock())
print(primes2.primes(10000))
ts.append(time.clock())
os.system('./primes 10000')
ts.append(time.clock())

for i in range(0,len(ts)-1):
    print('timing:', ts[i+1] - ts[i])
