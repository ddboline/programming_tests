#!/usr/bin/python
"""
    quick implementation of Vose Alias Sampling method taken from:
    http://www.keithschwarz.com/darts-dice-coins/
"""
from random import random, randint

class VoseAliasMethod(object):
    
    def __init__(self, p):
        self.pval = p
        self.num = len(self.pval)
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

if __name__ == '__main__':
    n = 6
    p = [random() for _ in range(n)]
    p = [x/sum(p) for x in p]
    print ['%.2f' % x for x in p]
    
    v = VoseAliasMethod(p)
    hist = n*[0]
    for _ in range(int(1e6)):
        r = v.generate()
        hist[r] += 1
    print hist
    print ['%.2f' % (x/float(sum(hist))) for x in hist]
