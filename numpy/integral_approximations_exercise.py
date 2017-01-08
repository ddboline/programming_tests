#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np

def func_f(a, b, c):
    return a**b - c

def first():
    #x = np.linspace(0, 1, 24)
    #y = np.linspace(0, 1, 12)
    #z = np.linspace(0, 1, 6)

    x, y, z = np.ogrid[0:1:24j, 0:1:12j, 0:1:6j]

    #w = np.sum(func_f(x, y, z) / (24. * 12. * 6.))
    w = func_f(x, y, z).mean()
    ww = np.log(2) - 0.5
    print(ww, w, (ww-w)/ww)

first()
