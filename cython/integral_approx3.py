#!/usr/bin/python

from numba import jit

@jit
def func_f(a, b, c):
    return a**b - c

@jit
def integrate_f(Nx, Ny, Nz):
    s = 0.
    x = 0.
    y = 0.
    z = 0.
    dx = 1. / (Nx - 1)
    dy = 1. / (Ny - 1)
    dz = 1. / (Nz - 1)
    i, j, k = 0, 0, 0
    while i < Nx:
        j = 0
        while j < Ny:
            k = 0
            while k < Nz:
                x = i * dx
                y = j * dy
                z = k * dz
                s += func_f(x, y, z)
                k += 1
            j += 1
        i += 1
    return s / (Nx * Ny * Nz)
