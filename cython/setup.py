#!/usr/bin/python

import os
import sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

PY23 = 'python%d.%d' % (sys.version_info[0:2])
INCDIR = '/usr/lib/%s/numpy' % PY23
if not os.path.exists(INCDIR):
    INCDIR = '/usr/lib/%s/dist-packages/numpy/core/include' % PY23
if not os.path.exists(INCDIR):
    INCDIR = '/opt/conda/lib/%s/site-packages/numpy/core/include' % PY23

extensions = [
    Extension("matmul2", ["matmul2.pyx"], 
        include_dirs=[INCDIR]),
    Extension("matmul3", ["matmul3.pyx"],
        include_dirs=['/usr/include/gsl/', INCDIR],
        libraries=['gslcblas'],
        library_dirs=['/usr/lib']),
    Extension('cos_func', ['cos_func.pyx'], libraries=['m']),
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
