#!/usr/bin/python3

import numpy as np
cimport numpy as np
cimport cython

#ctypedef np.float64_t dtype_t

@cython.boundscheck(False)
@cython.wraparound(False)
def matmul2(np.ndarray[np.float64_t, ndim=2] A, np.ndarray[np.float64_t, ndim=2] B, np.ndarray[np.float64_t, ndim=2] out):
    cdef int i, j, k
    cdef double s = 0
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            s = 0
            for k in range(A.shape[1]):
                s += A[i,k] * B[k,j]
            out[i,j] = s
