#!/usr/bin/python3

#from integ0 import integrate_f

import pyximport
pyximport.install()

import integ0
import integ1
import integ2
import integ3
import time
import os
from subprocess import call

t = []
t.append(time.clock())
print(integ0.integrate_f(0., 1., 5e7))
t.append(time.clock())
print(integ1.integrate_f(0., 1., 5e7))
t.append(time.clock())
print(integ2.integrate_f(0., 1., 5e7))
t.append(time.clock())
print(integ3.integrate_f(0., 1., 5e7))
t.append(time.clock())
call('./integ', shell=True)
t.append(time.clock())

print('timing:',)
for n in range(1, len(t)):
    print(t[n]-t[n-1],)
print('')
