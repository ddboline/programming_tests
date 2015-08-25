#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
from timeit import timeit

def quicksort(array):
    less = []
    greater = []
    if len(array) < 2:
        return array

    pivot = array.pop(len(array)//2)
    for x in array:
        if x <= pivot:
            less.append(x)
        else:
            greater.append(x)
    return quicksort(less) + [pivot]+ quicksort(greater)

if __name__ == '__main__':
    import time
    arr = np.random.randint(0, 100, 10000)
    t0 = time.clock()
    quicksort(list(arr))
    t1 = time.clock()
    sorted(list(arr))
    t2 = time.clock()
    print('quicksort %f sorted %f' % (t1-t0, t2-t1))
