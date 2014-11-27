#!/usr/bin/python

#from integ0 import integrate_f

import pyximport
pyximport.install()

import integral_approx0
import integral_approx1
import integral_approx2
import time
import os 

#Nx, Ny, Nz = 24, 12, 6
Nx, Ny, Nz = 100, 100, 100

t0 = time.clock()
print integral_approx0.integrate_f(Nx, Ny, Nz)
t1 = time.clock()
print integral_approx1.integrate_f(Nx, Ny, Nz)
t2 = time.clock()
print integral_approx2.integrate_f(Nx, Ny, Nz)
t3 = time.clock()
#os.system('/home/ddboline/temp/cython/integ')
t4 = time.clock()

print t4-t3, t3-t2, t2-t1, t1-t0
