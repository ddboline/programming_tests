#!/usr/bin/python

import pyximport
pyximport.install()

import basel0
import basel1
import time
import math

import pstats, cProfile

def time_execution():
    print math.pi
    t0 = time.clock()
    print basel0.approx_pi(10**6)
    t1 = time.clock()
    print basel1.approx_pi(10**9)
    t2 = time.clock()

    print t1-t0, t2-t1

def cprofile_basel0():
    cProfile.runctx('basel0.approx_pi()', globals(), locals(), 'Profile.prof')

    s = pstats.Stats('Profile.prof')
    s.strip_dirs().sort_stats("time").print_stats()

def cprofile_basel1():
    cProfile.runctx('basel1.approx_pi()', globals(), locals(), 'Profile.prof')
    
    s = pstats.Stats('Profile.prof')
    s.strip_dirs().sort_stats("time").print_stats()

time_execution()