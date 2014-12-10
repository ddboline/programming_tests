#!/usr/bin/python

def matmul0(A, B, out):
    for i in xrange(A.shape[0]):
        for j in xrange(B.shape[1]):
            s = 0
            for k in xrange(A.shape[1]):
                s += A[i,k] * B[k,j]
            out[i,j] = s
