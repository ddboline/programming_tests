#!/usr/bin/python3

import sys
from PyKDE4.kdecore import KAboutData, KCmdLineArgs, ki18n
from PyKDE4.kdeui import KApplication

appName = "python-kde-tutorial"
catalog = ""
programName = ki18n("PyKDE Tutorial")
version = "1.0"
description = ki18n("A Small Qt WebKit Example")
license = KAboutData.License_GPL
copyright = ki18n("(c) 2008 Canonical Ltd")
text = ki18n("none")
homePage = "www.kubuntu.org"
bugEmail = ""
 
aboutData = KAboutData(appName, catalog, programName, version, description,
license, copyright, text, homePage, bugEmail)
 
KCmdLineArgs.init(sys.argv, aboutData)
app = KApplication()
#sys.exit(app.exec_())
