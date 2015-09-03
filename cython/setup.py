#!/usr/bin/python

import os
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
                 libraries = ['m']),
    Extension('sampling_vose_alias_method1',
              ['sampling_vose_alias_method1.pyx'],
              language="c++",),
    Extension('smith_number2',
              ['smith_number2.pyx'],
              language="c++",),
    Extension('primes1',
              ['primes1.pyx'],
              language="c++",),
]
setup(
    ext_modules = cythonize(extensions),
)
