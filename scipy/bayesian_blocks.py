#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import pylab as pl

def bayesian_blocks(t):
    """Bayesian Blocks Implementation

    By Jake Vanderplas.  License: BSD
    Based on algorithm outlined in http://adsabs.harvard.edu/abs/2012arXiv1207.5578S

    Parameters
    ----------
    t: ndarray, length N
        data to be histogrammed

    Returns
    -------
    bins: ndarray
        array containing the (N+1) bin edges

    Notes
    -----
    This is an incomplete implementation: it may fail for some
    datasets.  Alternate fitness functions and prior forms can
    be found in the paper listed above.
    """

    # copy and sort the array
    t = np.sort(t)
    N = t.size

    # create length-(N + 1) array of cell edges
    edges = np.concatenate([t[:1],
                            0.5 * (t[1:]+ t[:-1]),
                            t[-1:]])
    block_length = t[-1]- edges

    # arrays needed for the iteration
    nn_vec = np.ones(N)
    best = np.zeros(N, dtype=float)
    last = np.zeros(N, dtype=int)

    #-----------------------------------------------------------------
    # Start with first data cell; add one cell at each iteration
    #-----------------------------------------------------------------
    for K in range(N):
        # Compute the width and count of the final bin for all possible
        # locations of the K^th changepoint
        width = block_length[:K + 1]- block_length[K + 1]
        count_vec = np.cumsum(nn_vec[:K + 1][::-1])[::-1]

        # evaluate fitness function for these possibilities
        fit_vec = count_vec * (np.log(count_vec) - np.log(width))
        fit_vec -= 4  # 4 comes from the prior on the number of changepoints
        fit_vec[1:] += best[:K]

        # find the max of the fitness: this is the K^th changepoint
        i_max = np.argmax(fit_vec)
        last[K] = i_max
        best[K] = fit_vec[i_max]

    #-----------------------------------------------------------------
    # Recover changepoints by iteratively peeling off the last block
    #-----------------------------------------------------------------
    change_points = np.zeros(N, dtype=int)
    i_cp = N
    ind = N
    while True:
        i_cp -= 1
        change_points[i_cp] = ind
        if ind == 0:
            break
        ind = last[ind - 1]
    change_points = change_points[i_cp:]

    return edges[change_points]

def plot_test_dist():
    # Define our test distribution: a mix of Cauchy-distributed variables
    np.random.seed(0)
    x = np.concatenate([stats.cauchy(-5, 1.8).rvs(500),
                        stats.cauchy(-4, 0.8).rvs(2000),
                        stats.cauchy(-1, 0.3).rvs(500),
                        stats.cauchy(2, 0.8).rvs(1000),
                        stats.cauchy(4, 1.5).rvs(500)])

    # truncate values to a reasonable range
    x = x[(x > -15) & (x < 15)]

    #pl.hist(x, bins=100, normed=True)

    # plot a standard histogram in the background, with alpha transparency
    H1 = pl.hist(x, bins=200, histtype='stepfilled',
            alpha=0.2, normed=True)
    # plot an adaptive-width histogram on top
    H2 = pl.hist(x, bins=bayesian_blocks(x), color='black',
            histtype='step', normed=True)

    pl.savefig('bayesian_blocks.png')

if __name__ == "__main__":
    plot_test_dist()
