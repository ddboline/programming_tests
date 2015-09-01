#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os, hashlib
import gzip
try:
    import cPickle as pickle
except ImportError:
    import pickle

import json

#from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker

hostname = os.uname()[1]

class FileInfo(object):
    ''' file info class '''
    __slots__ = ['fullfilename', 'hostname', 'md5sum', 'filestat']

    finf_attrs = (__slots__)
    stat_attrs = ('st_atime', 'st_blksize', 'st_blocks', 'st_ctime', 'st_dev', 'st_gid', 'st_ino', 'st_mode', 'st_mtime', 'st_nlink', 'st_rdev', 'st_size', 'st_uid')
    
    def __init__(self, fn='', hn=hostname, md5='', fs=None):
        self.fullfilename = fn.encode(errors='ignore')
        self.hostname = hn
        if md5:
            self.md5sum = md5
        else:
            self.md5sum = self.get_md5_full(self.fullfilename)
        if fs:
            self.filestat = fs
        else:
            _fstat = os.stat(self.fullfilename)
            self.filestat = {attr: getattr(_fstat, attr) for attr in self.stat_attrs}

    def __repr__(self):
        return '<FileInfo(fn=%s, hs=%s, md5=%s, size=%s>' % (self.fullfilename,
                                                             self.hostname, self.md5sum, self.filestat.st_size)

    def get_md5_full(self, fname):
        if not os.path.exists(fname):
            return None
        m = hashlib.md5()
        with open(fname, 'r') as infile:
            for line in infile:
                m.update(line)
        return m.hexdigest()

class FileList(object):
    
    def __init__(self, basepath='', subdirectories=[]):
        self.pfilename = '%s/.file_sync_%s.pkl.gz' % (os.getenv('HOME'), hostname)
        if basepath:
            self.basepath = basepath
        else:
            self.basepath = '.'
        if subdirectories:
            self.subdirs = ['%s/%s' % (self.basepath, subdirectories)]
        else:
            self.subdirs = [self.basepath]
        self.filelist_dict = {}
        
    def remove_persistence_file(self):
        os.remove(self.pfilename)
        
    def read_persistence_file(self):
        if not os.path.exists(self.pfilename):
            return
        with gzip.open(self.pfilename, 'rb') as pfile:
            _temp = pickle.load(pfile)
            if _temp:
                self.filelist_dict = _temp
    
    def write_persistence_file(self):
        if not self.filelist_dict:
            return
        with gzip.open(self.pfilename, 'wb') as pfile:
            pickle.dump(self.filelist_dict, pfile, pickle.HIGHEST_PROTOCOL)

    def recursive_read(self):
        def parse_dir(arg, path, filelist):
            for fn in filelist:
                fullfn = ('%s/%s' % (path, fn)).replace('//', '/')
                if os.path.isfile(fullfn):
                    stobj = os.stat(fullfn)
                    if fullfn in arg and arg[fullfn].filestat.st_size == stobj.st_size:
                        continue
                    finfo = FileInfo(fn=fullfn, hn=hostname, fs=stobj)
                    print(finfo)
                    arg[fullfn] = finfo

        for d in self.subdirs:
            os.path.walk(d, parse_dir, self.filelist_dict)
        return
    
def read_config_file():
    conf_obj = []
    if os.path.exists('%s/.file_sync_config.json' % os.getenv('HOME')):
        with open('%s/.file_sync_config.json' % os.getenv('HOME')) as confile:
            return json.load(confile)
    else:
        return conf_obj

def file_sync():
    return

def run_tests():
    script_path = os.path.abspath(os.path.curdir)
    testfname = '%s/analyze_gmail.py' % script_path
    finfo = FileInfo(testfname)
    assert finfo.md5sum == 'e9dc10073356c4527d70752871c65e10'
    print(os.stat(testfname), '\n')
    
    testdir = '/home/ddboline/Documents/mp3'
    testdir = '%s' % script_path
    flist = FileList(basepath=testdir)
    flist.read_persistence_file()
    flist.recursive_read()
    flist.write_persistence_file()

    conf_obj = read_config_file()
    print(conf_obj, type(conf_obj))

if __name__ == '__main__':
    file_sync()
