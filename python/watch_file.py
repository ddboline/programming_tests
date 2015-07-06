import pyinotify

class ProcessControlFile(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self, event):
        outval = open(event.pathname,'r').read().strip()
        if outval:
            print outval

    def process_default(self, event):
        print 'default',event.maskname

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)
wm.watch_transient_file('/tmp/.roku_control_file', pyinotify.IN_MODIFY,
                        ProcessControlFile)
notifier.loop()

print 'hello?'
