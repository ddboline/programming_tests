#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os, hashlib

#from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker

hostname = os.uname()[1]

class FileInfo(object):
    __slots__ = ['fullfilename', 'hostname', 'md5sum', 'filestat']
    
    def __init__(self, fn='', hn='localhost', md5='', fs=None):
        self.fullfilename = fn.encode(errors='ignore')
        self.hostname = hn
        self.md5sum = md5
        self.filestat = fs
    
    def __repr__(self):
        return '<FileInfo(fn=%s, hs=%s, md5=%s, size=%s>' % (self.fullfilename,
                                                             self.hostname, self.md5sum, self.filestat.st_size)

def get_md5_full(fname):
    m = hashlib.md5()
    with open(fname, 'r') as infile:
        for line in infile:
            m.update(line)
    return m.hexdigest()

def parse_dir(arg, path, filelist):
    for fn in filelist:
        fullfn = ('%s/%s' % (path, fn)).replace('//', '/')
                
        if os.path.isfile(fullfn):
            stobj = os.stat(fullfn)
            if fullfn in arg and arg[fullfn].filestat.st_size == stobj.st_size:
                continue
            md5val = get_md5_full(fullfn)
            finfo = FileInfo(fn=fullfn, hn=hostname, md5=md5val, fs=stobj)
            print(finfo)
            arg[fullfn] = finfo

def recursive_read(directory, finf_dict):
    os.path.walk(directory, parse_dir, finf_dict)
    return

def file_sync():
    return

if __name__ == '__main__':
    testfname = '%s/setup_files/build/programming_tests/python/file_sync.py' % os.getenv('HOME')
    #file_sync()
    print(get_md5_full(testfname))
    print(testfname)
    print(os.stat(testfname), '\n')
    
    testdir = '/home/ddboline/Documents/mp3'
    testdir = '%s/setup_files/build/programming_tests' % os.getenv('HOME')
    fileinfo_dict = {}
    recursive_read(testdir, fileinfo_dict)

