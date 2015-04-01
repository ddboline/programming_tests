#!/usr/bin/python

import sys
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication

appName     = "tempKDEapp"
catalog     = ""
programName = ki18n ("tempKDEapp")
version     = "1.0"
description = ki18n ("test KDE Application")
license     = KAboutData.License_GPL
copyright   = ki18n ("(c) 2012 Daniel Boline")
text        = ki18n ("none")
homePage    = ""
bugEmail    = "ddboline@gmail.com"

aboutData   = KAboutData (appName, catalog, programName, version, description,
                        license, copyright, text, homePage, bugEmail)

KCmdLineArgs.init (sys.argv, aboutData)

app = KApplication ()
print dir(app)
