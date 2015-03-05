#!/bin/python
import math

t = int(input())
for _ in range(t):
    r2, k = (int(x) for x in raw_input().split())

    count = 0
    r = int(math.sqrt(r2))
    if r2 - r*r == 0:
        count = 4
    for a in range(1, r+1):
        a2 = a*a
        b = int(math.sqrt(r2-a2))
        if r2 - a2 - b*b == 0:
            if a < b:
                count += 8
            elif a == b:
                count += 4
    if k < count:
        print 'impossible'
    else:
        print 'possible'
