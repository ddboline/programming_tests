#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def data_statistics():
    data = np.loadtxt('populations.txt')
    year, hares, lynxes, carrots = data.T

    names = ('Hare', 'Lynx', 'Carrot')

    plt.axes([0.2, 0.1, 0.5, 0.8])
    plt.plot(year, hares, year, lynxes, year, carrots)
    plt.legend(names, loc=(1.05, 0.5))
    plt.savefig('data_statistics.png')

    print('        %10s %10s %10s' % ('Mean', 'StdDev', 'MaxYear'))
    print('Hares   %10d %10d %10d' % (hares.mean(), hares.std(), year[np.argmax(hares)]))
    print('Lynxes  %10d %10d %10d' % (lynxes.mean(), lynxes.std(), year[np.argmax(lynxes)]))
    print('Carrots %10d %10d %10d' % (carrots.mean(), carrots.std(), year[np.argmax(carrots)]))

    j = np.argsort(data[:, 1:])
    # print(j
    a = np.resize(np.array(names), j.shape)[j == 0].copy()
    b = np.concatenate((year[:, np.newaxis], a[:, np.newaxis]), axis=1)
    c = np.array([['year', 'MostPopulousAnimal']])
    print(b.shape, c.shape)
    print(np.concatenate((c, b), axis=0))
    print(year[np.any(data[:, 1:] > 50000, axis=1)])
    j = np.argsort(data[:, 1:], axis=0)
    print(j)
    print(names[0], year[j[:2, 0]])
    print(names[1], year[j[:2, 1]])
    print(names[2], year[j[:2, 2]])

    plt.clf()
    plt.axes([0.2, 0.1, 0.5, 0.8])
    plt.plot(year, np.gradient(hares), year, np.gradient(lynxes), year, np.gradient(carrots))
    plt.legend(names, loc=(1.05, 0.5))
    plt.savefig('data_statistics_gradient.png')

    gh = np.gradient(hares)
    gl = np.gradient(lynxes)
    gc = np.gradient(carrots)

    a = np.concatenate((gh[:, np.newaxis], gl[:, np.newaxis]), axis=1)
    print(np.corrcoef(a.T))
    a = np.concatenate((a, gc[:, np.newaxis]), axis=1)
    print(a.T)
    print(np.corrcoef(a.T))

data_statistics()
