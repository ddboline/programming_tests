from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from math import log

def fast_pow(A, B):
    global ops
    if B == 0:
        return 1
    elif B == 1:
        return A
    else:
        tmp = fast_pow(A, B//2)
        if B % 2 == 0:
            ops += 1
            return tmp * tmp
        else:
            ops += 2
            return tmp * tmp * A

for N in range(40):
    ops = 0
    tmp = fast_pow(2, N)
    print(N, ops, tmp, 2*log(N+1))
