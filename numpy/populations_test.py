#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def pop_test():
    data = np.loadtxt('populations.txt')
    year, hares, lynxes, carrots = data.T
    populations = data[:, 1:]
    
    plt.axes([0.2, 0.1, 0.5, 0.8])
    plt.plot(year, hares, year, lynxes, year, carrots)
    plt.legend(('Hare', 'Lynx', 'Carrot'), loc=(1.05, 0.5))
    plt.savefig('populations_test.png')
    
    print populations.mean(axis=0)
    print populations.std(axis=0)
    print np.argmax(populations, axis=1)
    
    np.savetxt('pop2.txt', data)
    
    return

pop_test()
