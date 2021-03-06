#!/bin/python
import random

def quickSort(ar):
    if len(ar) < 2:
        return ar
    p = ar[0]
    lower = []
    upper = []
    for n in range(1,len(ar)):
        if p > ar[n]:
            lower.append(ar[n])
        else:
            upper.append(ar[n])
    newar = quickSort(lower) + [p] + quickSort(upper)
    #print ' '.join('%s' % x for x in newar)
    return newar

def partition(ar, lidx, pidx):
    if lidx+1 == pidx:
        if ar[lidx] > ar[pidx]:
            tmp = ar[pidx]
            ar[pidx] = ar[lidx]
            ar[lidx] = tmp
            #print ' '.join(['%s' % x for x in ar])
        return lidx, -1, pidx
    first_idx = lidx
    for current_idx in range(lidx,pidx):
        if ar[current_idx] < ar[pidx]:
            tmp = ar[first_idx]
            ar[first_idx] = ar[current_idx]
            ar[current_idx] = tmp
            first_idx += 1
    #if ar[first_idx] > ar[pidx]:
    tmp = ar[first_idx]
    ar[first_idx] = ar[pidx]
    ar[pidx] = tmp
    #print ' '.join(['%s' % x for x in ar])
    if lidx <= first_idx-1:
        partition(ar, lidx, first_idx-1)
    if pidx > first_idx+1:
        partition(ar, first_idx+1, pidx)

arr = [1, 3, 9, 8, 2, 7, 5]
print '\n', ' '.join(['%s' % x for x in arr]), '\n'
print '\n', ' '.join(['%s' % x for x in quickSort(arr)]), '\n'
partition(arr, 0, len(arr)-1)
print '\n', ' '.join(['%s' % x for x in arr]), '\n'

arr = [9, 8, 6, 7, 3, 5, 4, 1, 2]
print '\n', ' '.join(['%s' % x for x in arr]), '\n'
print '\n', ' '.join(['%s' % x for x in quickSort(arr)]), '\n'
partition(arr, 0, len(arr)-1)
print '\n', ' '.join(['%s' % x for x in arr]), '\n'

import random
arr = [random.randint(-10000,10000) for x in range(10)]
print '\n', ' '.join(['%s' % x for x in arr]), '\n'
print '\n', ' '.join(['%s' % x for x in quickSort(arr)]), '\n'
partition(arr, 0, len(arr)-1)
print '\n', ' '.join(['%s' % x for x in arr]), '\n'

arr = [406, 157, 415, 318, 472, 46, 252, 187, 364, 481, 450, 90, 390, 35, 452, 74, 196, 312, 142, 160, 143, 220, 483, 392, 443, 488, 79, 234, 68, 150, 356, 496, 69, 88, 177, 12, 288, 120, 222, 270, 441, 422, 103, 321, 65, 316, 448, 331, 117, 183, 184, 128, 323, 141, 467, 31, 172, 48, 95, 359, 239, 209, 398, 99, 440, 171, 86, 233, 293, 162, 121, 61, 317, 52, 54, 273, 30, 226, 421, 64, 204, 444, 418, 275, 263, 108, 10, 149, 497, 20, 97, 136, 139, 200, 266, 238, 493, 22, 17, 39]
print '\n', ' '.join(['%s' % x for x in arr]), '\n'
print '\n', ' '.join(['%s' % x for x in quickSort(arr)]), '\n'
partition(arr, 0, len(arr)-1)
print '\n', ' '.join(['%s' % x for x in arr]), '\n'
