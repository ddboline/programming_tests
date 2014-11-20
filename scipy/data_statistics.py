#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
matplotlib.use( 'Agg' )
import matplotlib.pyplot as plt

def data_statistics() :
    data = np.loadtxt( 'populations.txt' )
    year , hares , lynxes , carrots = data.T
    
    plt.axes( [ 0.2 , 0.1 , 0.5 , 0.8 ] )
    plt.plot( year , hares , year , lynxes , year , carrots )
    plt.legend( ( 'Hare' , 'Lynx' , 'Carrot' ) , loc = ( 1.05,0.5 ) )
    plt.savefig( 'data_statistics.png' )

data_statistics()