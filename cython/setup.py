#!/usr/bin/python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("matmul2", ["matmul2.pyx"]),
    Extension("matmul3", ["matmul3.pyx"],
        include_dirs = ['/usr/include/gsl/'],
        libraries = ['gslcblas'],
        library_dirs = ['/usr/lib']),
    Extension('cos_func', ['cos_func.pyx'],
                 libraries = ['m'])
]
setup(
    ext_modules = cythonize(extensions),
)
