#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as pl

pl.clf()
# Create a new figure of size 8x6 points, using 100 dots per inch
pl.figure(figsize=(8, 6), dpi=100)

# Create a new subplot from a grid of 1x1
pl.subplot(111)

X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)

# Plot cosine using blue color with a continuous line of width 1 (pixels)
pl.plot(X, C, color="blue", linewidth=2.5, linestyle="--", label='Cosine')

# Plot sine using green color with a continuous line of width 1 (pixels)
pl.plot(X, S, color="red", linewidth=2.5, linestyle="-", label='Sine')

# Set x limits
pl.xlim(X.min()*1.1, X.max()*1.1)

# Set y limits
pl.ylim(C.min()*1.1, C.max()*1.1)

ax = pl.gca()  # gca stands for 'get current axis'
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))

# Set x ticks
pl.xticks(np.linspace(-np.pi, np.pi, 5, endpoint=True), ['$-\pi$', '$-\pi/2$', '', '$+\pi/2$', '$+\pi$'])

# Set y ticks
pl.yticks(np.linspace(-1, 1, 3, endpoint=True), ['$-1$', '', '$+1$'])

pl.legend(loc='upper left')

t = 2 * np.pi / 3
pl.plot([t, t], [0, np.cos(t)], color='blue', linewidth=2.5, linestyle="--")
pl.scatter([t,], [np.cos(t),], 50, color='blue')

pl.annotate(r'$sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
            xy=(t, np.sin(t)), xycoords='data',
            xytext=(+10, +30), textcoords='offset points', fontsize=16,
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

pl.plot([t, t], [0, np.sin(t)], color='red', linewidth=2.5, linestyle="--")
pl.scatter([t,], [np.sin(t),], 50, color='red')

pl.annotate(r'$cos(\frac{2\pi}{3})=-\frac{1}{2}$',
            xy=(t, np.cos(t)), xycoords='data',
            xytext=(-90, -50), textcoords='offset points', fontsize=16,
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))


for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(16)
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65))

pl.savefig('plot_test.png')
