#!/usr/bin/python

def f(x):
    return x**2 - x

def integrate_f(a, b, N):
    s = 0
    dx = (b - a) / N
    i = 0
    while i < N:
        s += f(a + i * dx)
        i += 1
    return s * dx
