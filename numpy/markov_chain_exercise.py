#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def prob(i, j):
    return

def first(n_states=5):

    trans_man = np.random.rand(n_states, n_states)
    prob_dist = np.random.rand(n_states)

    trans_man = trans_man / np.sum(trans_man, axis=1)[:, np.newaxis]
    prob_dist = prob_dist / np.sum(prob_dist)

    for k in range(50):
        prob_dist = trans_man.T.dot(prob_dist)

    w, v = np.linalg.eig(trans_man.T)
    print(w)
    j = np.argmin(abs(w - 1.))
    pstat = v[:, j].real
    pstat /= np.sum(pstat)
    print(pstat)
    print(prob_dist)
    print((pstat-prob_dist).sum())

first()
