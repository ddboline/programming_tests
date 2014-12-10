#!/usr/bin/python

import pyximport
pyximport.install()

import numpy as np

import matmul0
import matmul1
import matmul2

import os
import time

def run_matmul():
    x = int(os.sys.argv[1])
    y = int(os.sys.argv[2])
    z = int(os.sys.argv[3])
    
    ts = []
    a = np.random.random_sample( ( x,y ) )
    b = np.random.random_sample( ( y , z ) )
    cs = [ np.zeros((x,z)) for i in range(3) ]
    
    ts.append( time.clock() )
    matmul0.matmul( a , b , cs[0] )
    ts.append( time.clock() )
    #matmul1.matmul( a , b , cs[1] )
    cs[1] = a.dot(b)
    ts.append( time.clock() )
    matmul2.matmul( a , b , cs[2] )
    ts.append( time.clock() )

    for i in range(3):
        print np.mean(cs[i]) , ts[i+1] - ts[i]

    return

if __name__ == '__main__':
    run_matmul()