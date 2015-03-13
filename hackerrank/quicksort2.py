#!/bin/python
import random

def quickSort(ar, lower=-1, upper=-1):
    if upper-lower < 2:
        return 'Here'
    pivot = ar[upper]
    new_lower = lower
    for n in range(lower, upper):
        if ar[n] > pivot:
            if ar[new_lower] < pivot:
                new_lower = n
        elif n > new_lower and ar[new_lower] > ar[n]:
            temp = ar[n]
            ar[n] = ar[new_lower]
            ar[new_lower] = temp
            new_lower += 1
    print ' '.join('%s' % x for x in ar)
    print quickSort(ar, lower=lower, upper=new_lower-1)
    print quickSort(ar, lower=new_lower+1, upper=upper)
    return 'There'

ar = [1, 3, 9, 8, 2, 7, 5]
print ar
print quickSort(ar, 0, len(ar)-1)
#m = input()
#ar = [int(i) for i in raw_input().strip().split()]
#quickSort(ar)
