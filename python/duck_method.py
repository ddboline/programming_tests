#!/usr/bin/python

class SomeClass(object):
    firstattr = 25
    secondattr = (range(5))
    
    def __init__(self):
        self.thirdattr = 15
    
    def __repr__(self):
        return 'firstattr = %s, secondattr = %s, thirdattr = %s' % (self.firstattr, self.secondattr, self.thirdattr)

c = SomeClass()

print c
print SomeClass.__dict__
print c.__dict__

def duck_method(inst, x):
    inst.fourthattr = 30
    return x+1

SomeClass.duck_method = duck_method

print c.duck_method(5)
print c.fourthattr
print SomeClass.__dict__
print c.__dict__
