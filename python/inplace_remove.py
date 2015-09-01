#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

some_list = list(range(10))
print(some_list)
for item in some_list:
    print(item, some_list)
    some_list.remove(item)
print(some_list)
