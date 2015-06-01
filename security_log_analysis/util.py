#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 18:32:18 2015

@author: ddboline
"""

def dateTimeString(d):
    ''' input should be datetime object, output is string '''
    if not hasattr(d, 'strftime'):
        return d
    s = d.strftime('%Y-%m-%dT%H:%M:%S%z')
    if len(s) == 24 or len(s) == 20:
        return s
    elif len(s) == 19 and 'Z' not in s:
        return '%sZ' % s
