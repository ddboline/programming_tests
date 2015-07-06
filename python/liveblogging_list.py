#!/usr/bin/python
'''
    Script to automate something
'''
from urllib2 import urlopen
import lxml.etree

if __name__ == '__main__':
    urlout = urlopen(
        'http://www.bradford-delong.com/liveblogging-world-war-ii/atom.xml')
    for line in lxml.etree.parse(urlout).iter():
        if 'title' in line.tag and line.text and 'liveblog' in\
                line.text.lower():
            print line.text
        if 'link' in line.tag:
            _dict = {k: v for (k,v) in line.items()}
            print _dict['href']
