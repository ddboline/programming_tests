#!/bin/python
import random

def find_indicies(M, C):
    D = len(C)*[-1]
    D_dict = {}
    for n in range(len(C)):
        diff = M - C[n]
        if diff > 0:
            D[n] = diff
            D_dict[diff] = n
    for n in range(len(C)):
        if C[n] in D_dict and n != D_dict[C[n]] and n < D_dict[C[n]]:
            print n, D_dict[C[n]]
            return

M = 4
C = [1, 4, 5, 3, 2]
find_indicies(M, C)

M = 4
C = [2, 2, 4, 3]
find_indicies(M, C)

M = random.randint(2,10000)
C = [random.randint(1,10000) for x in range(2,10000)]
find_indicies(M, C)
