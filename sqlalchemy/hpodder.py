#!/usr/bin/python3

class podcasts(object):
    __tablename__ = 'podcasts'
    
    def __init__(self):
        self.castid = 0
        self.castname = ''
        self.feedurl = ''
        self.pcenabled = 1
        self.lastupdate = 0
        self.lastattempt = 0
        self.failedattempts = 0

class episodes(object):
    __tablename__ = 'episodes'
    
    def __init__(self):
        self.castid = 0
        self.episodeid = 0
        self.title = ''
        self.epurl = ''
        self.enctype = ''
        self.status = ''
        self.eplength = 0
        self.epfirstattempt = 0
        self.eplastattempt = 0
        self.epfailedattempts = 0
        self.epguid = ''
