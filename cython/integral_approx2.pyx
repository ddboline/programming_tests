#!/usr/bin/python

#!/usr/bin/python

cdef double func_f( double a , double b , double c ) :
    return a**b - c

cpdef double integrate_f( int Nx , int Ny , int Nz ) :
    cdef double s = 0
    cdef double x , y , z
    cdef double dx = 1. / ( Nx - 1 )
    cdef double dy = 1. / ( Ny - 1 )
    cdef double dz = 1. / ( Nz - 1 )
    cdef int i , j , k
    x = 0
    while x < 1. :
        y = 0.
        while y < 1. :
            z = 0.
            while z < 1. :
                s += func_f( x , y , z )
                z += dz
            y += dy
        x += dx
    return s / ( Nx * Ny * Nz )
