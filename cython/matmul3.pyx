#!/usr/bin/python

import numpy as np
cimport numpy as np
cimport cython
#from scipy.linalg.blas import ddot

cdef extern from "gsl_cblas.h":
    double ddot "cblas_ddot"(const int N, const double *X, const int incX, const double *Y, const int incY)

def matmul3(np.ndarray[np.float64_t, ndim=2] A, np.ndarray[np.float64_t, ndim=2] B, np.ndarray[np.float64_t, ndim=2] out):
    cdef Py_ssize_t i, j
    cdef np.ndarray[np.float64_t, ndim=1] A_row, B_col
    for i in xrange(A.shape[0]):
        A_row = A[i,:]
        for j in range(B.shape[1]):
            B_col = B[:,j]
            out[i,j] = ddot( A_row.shape[0], <np.float64_t*> A_row.data, A_row.strides[0] // sizeof(np.float64_t),
                                             <np.float64_t*> B_col.data, B_col.strides[0] // sizeof(np.float64_t) )
