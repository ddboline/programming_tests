#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
    with open(fname, 'rb') as infile:
        for line in infile:
            m.update(line)
    return m.hexdigest()

def recursive_read(directory, finf_dict):
    for path, dirlist, filelist in os.walk(directory):
        for direc in dirlist:
            recursive_read('%s/%s' % (path, direc), finf_dict)
        for fn in filelist:
            fullfn = ('%s/%s' % (path, fn)).replace('//', '/')
                    
            if os.path.isfile(fullfn):
                stobj = os.stat(fullfn)
                if fullfn in finf_dict and finf_dict[fullfn].filestat.st_size == stobj.st_size:
                    continue
                md5val = get_md5_full(fullfn)
                finfo = FileInfo(fn=fullfn, hn=hostname, md5=md5val, fs=stobj)
                print(finfo)
                finf_dict[fullfn] = finfo

def file_sync():
    return

if __name__ == '__main__':
    testfname = '%s/setup_files/build/programming_tests/python/file_sync.py' % os.getenv('HOME')
    #file_sync()
    print(get_md5_full(testfname))
    print(testfname)
    print(os.stat(testfname), '\n')
    
    testdir = '/home/ddboline/Documents/mp3'
    testdir = '%s/setup_files/build/programming_tests/python' % os.getenv('HOME')
    fileinfo_dict = {}
    recursive_read(testdir, fileinfo_dict)

