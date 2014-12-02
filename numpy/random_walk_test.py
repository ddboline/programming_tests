#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def random_walk():
    n_stories = 1000 # number of walkers
    t_max = 200

    t = np.arange(t_max)
    steps = 2 * np.random.random_integers(0, 1, (n_stories, t_max)) - 1
    # print np.unique(steps)
    positions = np.cumsum(steps, axis=1)
    sq_distance = positions**2
    mean_sq_distance = np.mean(sq_distance, axis=0)

    # plt.figure(figsize=(4, 3))
    plt.plot(t, np.sqrt(mean_sq_distance), 'g.', t, np.sqrt(t), 'y-')
    plt.xlabel(r"$t$")
    plt.ylabel(r"$\sqrt{\langle (\delta x)^2 \rangle}$")
    plt.savefig('random_walk_test.png')

    return

random_walk()
