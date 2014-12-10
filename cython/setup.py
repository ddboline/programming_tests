#!/usr/bin/python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("matmul3", ["matmul3.pyx"],
        include_dirs = ['/usr/include/gsl/'],
        libraries = ['gsl'],
        library_dirs = ['/usr/lib']),
]
setup(
    ext_modules = cythonize(extensions),
)