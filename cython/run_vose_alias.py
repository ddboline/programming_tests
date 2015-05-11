#!/usr/bin/python

#import pyximport
#pyximport.install()

import sampling_vose_alias_method0
import sampling_vose_alias_method1
import time, os

os.system('g++ -std=c++11 -O3 sampling_vose_alias_method.cpp ' + 
          '-o sampling_vose_alias_method')

ts = []

for N in (5, 10, 20):
    ts_ = time.clock()
    sampling_vose_alias_method0.vose_alias_method_test(N)
    ts0 = time.clock()
    sampling_vose_alias_method1.vose_alias_method_test(N)
    ts1 = time.clock()
    os.system('./sampling_vose_alias_method %d' % N)
    ts2 = time.clock()
    ts.append((ts_, ts0, ts1, ts2))

for ts_, ts0, ts1, ts2 in ts:
    print 'timing:', ts0-ts_, ts1-ts0, ts2-ts1
