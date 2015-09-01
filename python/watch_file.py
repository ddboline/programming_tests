#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pyinotify

class ProcessControlFile(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self, event):
        outval = open(event.pathname,'r').read().strip()
        if outval:
            print(outval)

    def process_default(self, event):
        print('default',event.maskname)

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)
wm.watch_transient_file('/tmp/temp.tcx', pyinotify.IN_MODIFY,
                        ProcessControlFile)
notifier.loop()

print('hello?')
