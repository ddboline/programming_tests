#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def first():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    print('a', a)
    print('a.ravel()', a.ravel())
    print('a', a)
    print('a.T', a.T)
    print('a.T.ravel()', a.T.ravel())
    print('a.shape', a.shape)
    b = a.ravel()
    b = b.reshape((2, 3))
    print('b', b)
    print('a.reshape((2,-1))', a.reshape((2, -1)))
    b[0, 0] = 99
    print('a', a)
    a = np.zeros((3, 2))
    b = a.T.reshape(3*2)
    print('a', a)
    print('b', b)
    b[0] = 9
    print('a', a)
    print('b', b)

def second():
    a = np.arange(4*3*2).reshape(4, 3, 2)
    print('a.shape', a.shape)
    print('a[0,2,1]', a[0, 2, 1])
    b = a.transpose(1, 2, 0)
    print('b.shape', b.shape)
    print('b[2,1,0]', b[2, 1, 0])

def third():
    a = np.arange(4)
    a.resize((8,))
    print('a', a)
    a = np.arange(4)
    b = np.resize(a, (8,))
    print('b', b)

def sort():
    a = np.array([[4, 3, 5], [1, 2, 1]])
    print('a', a)
    b = np.sort(a, axis=1)
    print('b', b)
    print('a[0]', a[0])
    j = np.argsort(a[0])
    print('j', j)
    print('a[:,j]', a[:, j])
#first()
#second()
#third()
sort()
