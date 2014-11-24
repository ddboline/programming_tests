#!/usr/bin/python

#!/usr/bin/python
import os
import numpy as np

def func_f( a , b , c ) :
    return a**b - c


def integrate_f( Nx , Ny , Nz ) :
    x , y , z = np.ogrid[0:1:(Nx)*1j,0:1:(Ny)*1j,0:1:(Nz)*1j]
    
    return func_f( x , y , z).mean()
