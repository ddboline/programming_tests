#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def first():
    a = np.arange(1, 16).reshape((3, 5)).T
    print a
    print a[1::2]
    
def second():
    a = np.arange(25).reshape(5, 5)
    print a
    b = np.resize(np.array([1., 5, 10, 15, 20]), (5, 5))
    print a/b
    print a/b.T

def third():
    a = np.random.rand(10, 3)
    print a
    j = np.argsort(((a-0.5)**2))
    print j
    print a.shape, j.shape
    print a[j == 0, np.newaxis]
    
#first()
#second()
third()
