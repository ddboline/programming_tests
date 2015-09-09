#!/usr/bin/python

from cython.parallel import parallel, prange

cpdef double integrate_f(double a, double b, long int N):
    cdef long int i
    cdef double s = 0, dx, x
    s = 0
    dx = (b - a) / N
    i = 0
    with nogil, parallel():
        for i in prange(N):
            x = a + i * dx
            s += x**2 - x
    return s * dx
