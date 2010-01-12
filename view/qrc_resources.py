# -*- coding: utf-8 -*-

# Resource object code
#
# Created: Mon Dec 7 18:28:50 2009
#      by: The Resource Compiler for PyQt (Qt v4.4.1)
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore

qt_resource_data = "\
\x00\x00\x00\x00\
\
"

qt_resource_name = "\
\x00\x04\
\x00\x06\xec\x30\
\x00\x68\
\x00\x65\x00\x6c\x00\x70\
\x00\x0a\
\x0c\xba\xf2\x7c\
\x00\x69\
\x00\x6e\x00\x64\x00\x65\x00\x78\x00\x2e\x00\x68\x00\x74\x00\x6d\x00\x6c\
"

qt_resource_struct = "\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
