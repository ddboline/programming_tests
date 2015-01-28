#!/usr/bin/python3
# -*- coding: utf-8 -*-

import collections

class Tree(collections.defaultdict):
    def __init__(self):
        self.default_factory = Tree

    def __repr__(self):
        return repr(dict(self))

a = Tree()
a['tree']['thing']['orother'] = 'Hello'

print(a)
