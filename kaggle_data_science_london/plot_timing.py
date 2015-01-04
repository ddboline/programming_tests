#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as pl
import scipy.optimize as optimize


def lin_func(x, *p):
    return p[0] + p[1] * x + p[2] * x**2

def exp_func(x, *p):
    return p[0] + p[1] * np.exp(p[2]*x)

def do_fit(datax, datay, func, p0):
    #datax = data[:, 0]
    #datay = data[:, 1]
    p, c = optimize.curve_fit(func, datax, datay, p0=p0)
    l, v = np.linalg.eig(c)
    sig = v.dot(np.sqrt(np.diag(l))).dot(v.T)
    dp = np.sqrt(np.sum(sig.dot(v)**2, axis=1))

    errfunc = lambda p, x, y: func(x, *p) - y

    residuals = errfunc(p, datax, datay)
    s_res = np.std(residuals)
    ps = []
    datayerrors = None
    # 100 random data sets are generated and fitted
    for _ in range(100):
        if datayerrors is None:
            randomDelta = np.random.normal(0., s_res, len(datay))
            randomdataY = datay + randomDelta
        else:
            randomDelta = np.array([\
                               np.random.normal(0., derr, 1)[0] \
                               for derr in datayerrors])
            randomdataY = datay + randomDelta
        randomfit, randomcov = \
            optimize.leastsq(errfunc, p0, args=(datax, randomdataY),\
                              full_output=0)
        ps.append(randomfit)

    ps = np.array(ps)
    mean_pfit = np.mean(ps, 0)
    Nsigma = 1. # 1sigma gets approximately the same as methods above
                # 1sigma corresponds to 68.3% confidence interval
                # 2sigma corresponds to 95.44% confidence interval
    err_pfit = Nsigma * np.std(ps, 0)

    pfit_bootstrap = mean_pfit
    perr_bootstrap = err_pfit

    # print 'p', p
    # print 'pb', pfit_bootstrap
    # print 'dp', dp
    # print 'dpb', perr_bootstrap

    return p, dp
    # return pfit_bootstrap, perr_bootstrap


xvals, tvals = [], []
with open('timing.txt', 'r') as tfile:
    for line in tfile:
        ents = line.split()
        if len(ents) < 3:
            continue
        xvals.append(int(ents[0]))
        tvals.append(float(ents[1]))
x = np.array(xvals)
t = np.array(tvals)

pl.plot(x, t)

#fit_fun = exp_func
fit_fun = lin_func

p, dp = do_fit(x, t, fit_fun, p0=(0,0,0))

pp, pm = p+dp, p-dp
pl.plot(x, fit_fun(x, *p), 'r', linewidth=2.5)
pl.plot(x, fit_fun(x, *pp), 'r--')
pl.plot(x, fit_fun(x, *pm), 'r--')

for N in [1000, 10000, 20000, 30000]:
    print N, fit_fun(N, *p)/60., fit_fun(N, *pm)/60., fit_fun(N, *pp)/60.

pl.show()
pl.savefig('plot_timing.png')
