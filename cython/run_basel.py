#!/usr/bin/python

import pyximport
pyximport.install()

import basel0
import basel1
import basel2
import time
import math

import pstats, cProfile

def time_execution():
    t = []
    print(math.pi)
    t.append(time.clock())
    print(basel0.approx_pi(10**7))
    t.append(time.clock())
    print(basel1.approx_pi(10**7))
    t.append(time.clock())
    print(basel1.approx_pi(10**8))
    t.append(time.clock())
    print(basel2.approx_pi(10**7))
    t.append(time.clock())
    print(basel2.approx_pi(10**8))
    t.append(time.clock())

    print('timing:',)
    for n in range(1, len(t)):
        print(t[n]-t[n-1],)
    print('')

def cprofile_basel0():
    cProfile.runctx('basel0.approx_pi()', globals(), locals(), 'Profile.prof')

    s = pstats.Stats('Profile.prof')
    s.strip_dirs().sort_stats("time").print_stats()

def cprofile_basel1():
    cProfile.runctx('basel1.approx_pi()', globals(), locals(), 'Profile.prof')

    s = pstats.Stats('Profile.prof')
    s.strip_dirs().sort_stats("time").print_stats()

time_execution()
