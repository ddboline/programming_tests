#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np

def first_test():
    a = np.arange(1, 5)
    print(a + 1)
    b = np.ones(4) + 1
    print(b)
    print(a - b)
    print(a * b)
    j = np.arange(5)
    print(2**(j+1) - j)

    c = np.ones((3, 3))
    print(c*c)
    print(c.dot(c))

    a = np.random.rand(3)
    a = a / np.sqrt(np.sum(a**2))
    print(a)
    b = np.random.rand(3)
    b = b / np.sqrt(np.sum(b**2))
    print(b)
    c = np.cross(a, b)
    print(c)
    print(a.dot(b), a.dot(c), b.dot(a), b.dot(c))

def second_test():
    x = np.array([[1, 1], [2, 2]])
    print(x)
    print(x.sum(axis=0))
    print(x.sum())
    print(x[:, 0].sum(), x[:, 1].sum())
    print(x.sum(axis=1))
    print(x[0,:].sum(), x[1,:].sum())

    x = np.random.rand(2, 2, 2)
    print(x.sum(axis=2)[0, 1])
    print(x[0, 1,:].sum())

    x = np.array([1, 3, 2])
    print(x)
    print(x.min())
    print(x.max())

    x = np.array([1, 2, 3, 1])
    print(x.mean(), np.median(x), x.std())

#first_test()
second_test()
