#!/usr/bin/python

cdef double f(double x) :
    return x**2 - x

cpdef double integrate_f(double a, double b, long int N) :
    cdef long int i
    cdef double s = 0 , dx
    s = 0
    dx = (b - a) / N
    i = 0
    while i < N :
        s += f(a + i * dx)
        i += 1
    return s * dx
