#!/usr/bin/python
"""
    quick implementation of Vose Alias Sampling method taken from:
    http://www.keithschwarz.com/darts-dice-coins/
    
    This is python, so implementation is a transcription of the pseudocode,
    with slight modification required for c-style indicies [0,n-1] vs [1,n]
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from time import clock
from random import random, randint

from libcpp.vector cimport vector
from libcpp.deque cimport deque

cdef class VoseAliasMethod(object):
    cdef vector[int] alias
    cdef vector[double] prob
    cdef int num

    def __init__(self, vector[double] p):
        self.num = p.size()
        self.alias.clear()
        self.alias.resize(self.num)
        self.prob.clear()
        self.prob.resize(self.num)
        cdef deque[int] small
        cdef deque[int] large
        cdef vector[double] scaled_p = p
        for idx in range(self.num):
            scaled_p[idx] = p[idx] * self.num
        for idx in range(self.num):
            sp = scaled_p[idx]
            if sp < 1:
                small.push_back(idx)
            else:
                large.push_back(idx)
        while small.size() > 0 and large.size() > 0:
            l = small.front()
            small.pop_front()
            g = large.front()
            large.pop_front()
            self.prob[l] = scaled_p[l]
            self.alias[l] = g
            scaled_p[g] = (scaled_p[g]+scaled_p[l])-1
            if scaled_p[g] < 1:
                small.push_back(g)
            else:
                large.push_back(g)
        while large.size() > 0:
            g = large.front()
            large.pop_front()
            self.prob[g] = 1
        while small.size() > 0:
            l = small.front()
            small.pop_front()
            self.prob[l] = 1

    def generate(self):
        cdef int i = randint(0, self.num-1)
        cdef double r = random()
        if r < self.prob[i]:
            return i
        else:
            return self.alias[i]

def vose_alias_method_test(number=6):
    runs = [10, 10, 10, 100, 100, 100, 1000, 1000, 1000, 10000, 10000, 10000,
            100000, 100000, 100000, 1000000, 1000000, 1000000,
            10000000, 10000000, 10000000]
    t = [('begin', clock())]
    cdef int n = int(number)
    cdef vector[double] p
    p.resize(n)
    for idx in range(n):
        p[idx] = random()
    cdef double sump = 0.0
    for idx in range(n):
        sump += p[idx]
    for idx in range(n):
        p[idx] /= sump
    print(['%.2f' % x for x in p])
    
    cdef vector[double] hist
    v = VoseAliasMethod(p)
    t.append(('init', clock()))
    for run in runs:
        hist.clear()
        hist.resize(n)
        for _ in range(run):
            r = v.generate()
            hist[r] += 1
        sumh = 0.0
        for idx in range(n):
            sumh += hist[idx]
        for idx in range(n):
            hist[idx] /= sumh
        print('run%d' % run, ['%.2f' % (x) for x in hist])
        t.append(('run%d' % run, clock()))
    print('\n'.join(['%s %s' % (x, y) for x,y in t]))
