#!/usr/bin/python

import numpy as np
cimport numpy as np
cimport cython

#ctypedef np.float64_t dtype_t

@cython.boundscheck(False)
@cython.wraparound(False)
def matmul(np.ndarray[np.float64_t, ndim=2] A, np.ndarray[np.float64_t, ndim=2] B, np.ndarray[np.float64_t, ndim=2] out):
    cdef int i, j, k
    cdef double s = 0
    for i in xrange(A.shape[0]):
        for j in xrange(B.shape[1]):
            s = 0
            for k in xrange(A.shape[1]):
                s += A[i,k] * B[k,j]
            out[i,j] = s

