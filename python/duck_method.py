#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

class SomeClass(object):
    firstattr = 25
    secondattr = (range(5))
    
    def __init__(self):
        self.thirdattr = 15
    
    def __repr__(self):
        return 'firstattr = %s, secondattr = %s, thirdattr = %s' % (self.firstattr, self.secondattr, self.thirdattr)

c = SomeClass()

print(c)
print(dir(SomeClass))
print(dir(c))

def duck_method(inst, x):
    inst.fourthattr = 30
    return x+1

SomeClass.duck_method = duck_method

print(c.duck_method(5))
print(c.fourthattr)
print(dir(SomeClass))
print(dir(c))
