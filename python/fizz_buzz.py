#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

for N in range(1,100+1):
    output = ''
    if N % 3 == 0:
        output += 'Fizz'
    elif N % 5 == 0:
        output += 'Buzz'
    else:
        output = '%s' % N
    print(output)

