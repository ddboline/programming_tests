#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import fftpack
import matplotlib
matplotlib.use( 'Agg' )
import pylab as pl


def first() :
    dt = 0.02
    T = 5.
    tvec = np.arange( 0 , 20 , dt )
    sig = np.sin( 2 * np.pi / T * tvec ) + 0.5 * np.random.randn( tvec.size )

    #pl.plot( tvec , sig )
    
    samp_freq = fftpack.fftfreq( sig.size , d=dt )
    sig_fft = fftpack.fft(sig)
    #j = np.where( samp_freq > 0 )
    pl.plot( samp_freq , np.abs(sig_fft) )
    pl.xlim( -2 , 2 )
    pl.savefig( 'fft_test.png' )
    
first()