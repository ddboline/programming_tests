#!/usr/bin/python

from cython.parallel import parallel, prange

cpdef double integrate_f(double a, double b, long int N):
    cdef long int i = 0
    cdef double s = 0, dx, x
    dx = (b - a) / N
    with nogil, parallel():
        for i in prange(N):
            x = a + i * dx
            s += x**2 - x
    return s * dx
