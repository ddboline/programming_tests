#!/bin/python
import random

#!/bin/python
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
    print ' '.join('%s' % x for x in newar)
    return newar

arr = [1, 3, 9, 8, 2, 7, 5]
quickSort(arr)

import random
arr = [random.randint(-10000,10000) for x in range(10)]
quickSort(arr)

arr = [406, 157, 415, 318, 472, 46, 252, 187, 364, 481, 450, 90, 390, 35, 452, 74, 196, 312, 142, 160, 143, 220, 483, 392, 443, 488, 79, 234, 68, 150, 356, 496, 69, 88, 177, 12, 288, 120, 222, 270, 441, 422, 103, 321, 65, 316, 448, 331, 117, 183, 184, 128, 323, 141, 467, 31, 172, 48, 95, 359, 239, 209, 398, 99, 440, 171, 86, 233, 293, 162, 121, 61, 317, 52, 54, 273, 30, 226, 421, 64, 204, 444, 418, 275, 263, 108, 10, 149, 497, 20, 97, 136, 139, 200, 266, 238, 493, 22, 17, 39]
print '\n', ' '.join(['%s' % x for x in arr]), '\n'
quickSort(arr)
