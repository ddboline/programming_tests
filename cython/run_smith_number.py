#!/usr/bin/python3

import pyximport
pyximport.install()

import smith_number0
import smith_number1
import time
from subprocess import call, Popen, PIPE

call('g++ -O3 smith_number.cpp -o smith_number', shell=True)

ts = []

for N in (4, 22, 27, 28, 58, 59, 85, 94, 121, 4937775, 2050918644):
    ts_ = time.clock()
    n0 = smith_number0.smith_number(N)
    ts0 = time.clock()
    n1 = smith_number1.smith_number(N)
    ts1 = time.clock()
    command = './smith_number %d' % N
    _cmd = Popen(command, shell=True, stdout=PIPE, close_fds=True).stdout
    n2 = _cmd.read().strip()
    ts2 = time.clock()
    ts.append((ts_, n0, ts0, n1, ts1, n2, ts2))
    print(n0, n2, n2)

for ts_, n0, ts0, n1, ts1, n2, ts2 in ts:
    print('timing:', ts0-ts_, ts1-ts0, ts2-ts1)
