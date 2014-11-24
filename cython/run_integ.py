#!/usr/bin/python

#from integ0 import integrate_f

import pyximport
pyximport.install()

import integ0
import integ1
import integ2
import time
import os 

os.system( 'gcc integ.c -o integ' )

t0 = time.clock()
print integ0.integrate_f( 0. , 1. , 5e7 )
t1 = time.clock()
print integ1.integrate_f( 0. , 1. , 5e7 )
t2 = time.clock()
print integ2.integrate_f( 0. , 1. , 5e7 )
t3 = time.clock()
os.system( './integ' )
t4 = time.clock()

print t4-t3 , t3-t2 , t2-t1 , t1-t0
