#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    Script to automate something
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from urllib2 import urlopen
import lxml.etree

if __name__ == '__main__':
    urlout = urlopen('http://www.bradford-delong.com/liveblogging-world-war-ii/atom.xml')
    current_title = None
    link_dict = {}
    for line in lxml.etree.parse(urlout).iter():
        if 'title' in line.tag and line.text and 'liveblog' in\
                line.text.lower():
            current_title = line.text
        if 'link' in line.tag:
            _dict = {k: v for (k, v) in line.items()}
            if current_title:
                link_dict[current_title] = _dict['href']

    for key, val in link_dict.items():
        print('"%s": "%s"' % (key, val))
