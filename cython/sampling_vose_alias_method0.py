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

class VoseAliasMethod(object):
    
    def __init__(self, p):
        self.num = len(p)
        self.alias = self.num*[0]
        self.prob = self.num*[0]
        small = []
        large = []
        scaled_p = [x*self.num for x in p]
        for idx, sp in enumerate(scaled_p):
            if sp < 1:
                small.append(idx)
            else:
                large.append(idx)
        while len(small) > 0 and len(large) > 0:
            l = small.pop(0)
            g = large.pop(0)
            self.prob[l] = scaled_p[l]
            self.alias[l] = g
            scaled_p[g] = (scaled_p[g]+scaled_p[l])-1
            if scaled_p[g] < 1:
                small.append(g)
            else:
                large.append(g)
        while len(large) > 0:
            g = large.pop(0)
            self.prob[g] = 1
        while len(small) > 0:
            l = small.pop(0)
            self.prob[l] = 1

    def generate(self):
        i = randint(0, self.num-1)
        r = random()
        if r < self.prob[i]:
            return i
        else:
            return self.alias[i]

def vose_alias_method_test(number=6):
    runs = [10, 10, 10, 100, 100, 100, 1000, 1000, 1000, 10000, 10000, 10000,
            100000, 100000, 100000, 1000000, 1000000, 1000000,
            10000000, 10000000, 10000000]
    t = [('begin', clock())]
    n = int(number)
    p = [random() for _ in range(n)]
    p = [x/sum(p) for x in p]
    print(['%.2f' % x for x in p])
    
    v = VoseAliasMethod(p)
    t.append(('init', clock()))
    for run in runs:
        hist = [0 for _ in range(n)]
        for _ in range(run):
            r = v.generate()
            hist[r] += 1
        print('run%d' % run, ['%.2f' % (x/float(sum(hist))) for x in hist])
        t.append(('run%d' % run, clock()))
    print('\n'.join(['%s %s' % (x, y) for x,y in t]))

if __name__ == '__main__':
    vose_alias_method_test(os.sys.argv[1])
