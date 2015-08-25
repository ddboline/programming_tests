#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import misc

def framing_lena():
    lena = misc.lena()
    plt.imshow(lena, cmap=plt.cm.gray)
    plt.savefig('lena.png')

    crop_lena = lena[30:-30, 30:-30]
    plt.imshow(crop_lena)
    plt.savefig('crop_lena.png')

    y, x = np.ogrid[0:512, 0:512]
    print(y.shape, x.shape)
    centerx, centery = (256, 256)
    mask = (((y - centery)/1.)**2 + ((x - centerx)/0.8)**2) > 230**2
    lena[mask] = 0
    plt.imshow(lena[30:-30, 30:-30], cmap=plt.cm.gray)
    plt.savefig('lena_mask.png')
    return

framing_lena()
