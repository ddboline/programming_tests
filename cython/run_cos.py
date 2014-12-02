#!/usr/bin/python

import pyximport
pyximport.install()

import cos_func
import numpy as np

print cos_func.cos_func(1.0)
print cos_func.cos_func(0.)
print cos_func.cos_func(np.pi)
