# arc-p2.py 
# Application Entry

# Copyright (C) 2011 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!
import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from view.mainview import MainWindow
from utils.mojoconfig import *
from mojo import Mojo
from mock_mojo import MockMojo

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("UCLA Pharmacology")
    app.setOrganizationDomain("mednet.ucla.edu")
    app.setApplicationName("ARC-P Modular Chemistry System Controller")
    app.setApplicationVersion("2.0 'Elixys'")
    #turnRecordingOn()
    # mojo = Mojo()
    mojo = MockMojo(config)
    form = MainWindow(mojo=mojo, config=mojo.config)
    form.show()
    app.exec_() 
    mojo.shutdown()
    return form


if __name__=='__main__':
    f = main()
