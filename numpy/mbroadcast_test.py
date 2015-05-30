#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def first_test():
    a = np.tile(np.arange(0, 40, 10), (3, 1)).T
    print(a)
    b = np.array([0, 1, 2])
    print(b)
    print(b+a)

def second_test():
    x, y = np.arange(5), np.arange(5)[:, np.newaxis]
    print(x, y)
    distance = np.sqrt(x ** 2 + y ** 2)
    print(distance)
    plt.pcolor(distance)
    plt.colorbar()
    plt.savefig('mbroadcast.png', format='png')

def mbroadcast_test():
    mileposts = np.array([0, 198, 303, 736, 871, 1175, 1475, 1544, 1913, 2448])
    distance_array = np.abs(mileposts - mileposts[:, np.newaxis])
    print(distance_array)
    return

first_test()
second_test()
mbroadcast_test()
