#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import jsonpickle

class Tree(collections.defaultdict):
    def __init__(self):
        self.default_factory = Tree

    def __repr__(self):
        return repr(dict(self))

a = Tree()
a['tree']['thing']['orother'] = 'Hello'

print a
