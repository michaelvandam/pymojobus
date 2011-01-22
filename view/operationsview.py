
# ----------------------------------------------------------------------------
# OperationsView
#
# This file contains a number of classes to build an operations-based control
# window:
#
# - OperationsView:
#   - a single instance handles the main view
#   - instantiates a DeviceOperationsView for each device in the system
#   - controls visibility of DeviceOperationsViews depending on activeDevice
#   - displays empty window if no active device
#
# - DeviceOperationsView:
#   - base class for device-specific operations views
#
# - DeviceOperationsViewFactory:
#   - factory to construct instances of DeviceOperationsView subclasses
#     depending on installed devices
#
# - UnitOperationControlView:
#   - A view for unit operations
# ----------------------------------------------------------------------------

import os
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from unitoperation import *

class OperationsView(QGroupBox):
    """ Displays and controls unit operations for devices in the system.
        The view constructs a DeviceOperationsView for each device in
        the system, showing only the activeDevice.
    @ivar activeDevice  str     Address of active device (or None)
    @ivar devices       dict    Dictionary of all devices
                                (indexed by address)
    @ivar views         dict    Dictionary of all DeviceOperationViews
                                (indexed by address)
    @ivar emptyView     obj     View to display if activeDevice == None
    @ivar layout        obj     Layout that holds DeviceOperationViews
    """
    
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)
        self.devices = {}
        self.views = {}
        self.activeDevice = None
        self.setTitle("Device Operations")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.emptyView = EmptyOperationsView()
        self.layout.addWidget(self.emptyView)

    def enable(self):
        for view in self.views.values():
            view.setEnabled(True);
            
    def disable(self):
        for view in self.views.values():
            view.setDisabled(True);

    def clearDevices(self):
        self.setActiveDevice(None)  # Do this first to avoid any pointer errors
        for address,view in self.views.items():
            self.layout.removeWidget(view)
            view.setParent(None)    # Needed to actually remove
        self.devices.clear()
        self.views.clear()
        self.emptyView.show()
        
    def loadDevices(self, devices={}):
        self.devices = devices
        for address,device in self.devices.items():
            view = DeviceOperationsViewFactory().getView(device)
            view.hide()
            self.views[address] = view
            self.layout.addWidget(view)
            self.connect(view, SIGNAL("startOperation(PyQt_PyObject)"), self.startOperation)
            
    def setActiveDevice(self, address):
        # Add error checking
        if self.activeDevice != address:
            if self.activeDevice != None:
                self.views[self.activeDevice].hide()
            if address != None:
                self.emptyView.hide()
                self.views[address].show()
            else:
                self.emptyView.show()
            self.activeDevice = address

    def startOperation(self, operation):
        """ Notify parent that an operation has been initiated
        """
        self.emit(SIGNAL("startOperation(PyQt_PyObject)"), operation)

class EmptyOperationsView(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setText("No active device selected")
        

class DeviceOperationsViewFactory():
    """ Factory class for DeviceOperationsView subclasses.
    @cvar viewClasses   dict    Dictionary of class names
                                (indexed by device type)
    """

    viewClasses = {'PRM':'PRMOperationsView', 'RDM':'RDMOperationsView', }

    @classmethod
    def getView (cls, device=None):
        """ Return an instance of a DeviceOperationsView subclass corresponding to device
        """
        
        if device == None:
            return None
            
        type = device['deviceType']
        # TODO: elegant approach not working?  Use if/else
        #view = cls.viewClasses[type](device)
        if type == 'PRM':
            return PRMOperationsView(device)
        elif type == 'RDM':
            return RDMOperationsView(device)
        else:
            # TODO: Unknown view, raise exception
            return None
            
        return view

class DeviceOperationsView(QWidget):
    """ Base class for showing/controlling the available operations
        for a device.
    @ivar device    obj     Device connected to this view
    @ivar layout    obj     Layout that holds device operations
    """
    
    def __init__(self, device=None, parent=None):
        QWidget.__init__(self, parent)
        self.device = device
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
    def addOperation(self,operation):
        view = UnitOperationControlView(operation)
        self.layout.addWidget(view)
        self.connect(view, SIGNAL("startOperation(PyQt_PyObject)"), self.startOperation)
        
    def startOperation(self, operation):
        """ Notify parent that an operation has been initiated
        """
        self.emit(SIGNAL("startOperation(PyQt_PyObject)"), operation)

class RDMOperationsView(DeviceOperationsView):
    def __init__(self, device=None, parent=None):
        DeviceOperationsView.__init__(self, device, parent)

class PRMOperationsView(DeviceOperationsView):
    def __init__(self, device=None, parent=None):
        DeviceOperationsView.__init__(self, device, parent)
        # TODO: create method to automatically retrieve list from
        # a config file?
        self.addOperation(PRMReactOperation(self.device))
        self.addOperation(PRMEvapOperation(self.device))
        self.addOperation(PRMReagentOperation(self.device))
        self.addOperation(PRMXferTrapOperation(self.device))
        self.addOperation(PRMXferEluteOperation(self.device))
        self.addOperation(PRMXferHPLCOperation(self.device))
        self.addOperation(PRMAccessOperation(self.device))

class UnitOperationControlView(QGroupBox):
    """ Generic view of unit operation (for starting, and param setting)
    @ivar operation     obj     Unit operation attached to this view
    """

    def __init__(self, operation=None, parent=None):
        QGroupBox.__init__(self, parent)
        self.operation = operation
        paramLayout = QFormLayout()
        layout = QHBoxLayout()
        self.setLayout(layout)
        goButton = QPushButton('Go')
        layout.addLayout(paramLayout)
        layout.addWidget(goButton)
        self.connect(goButton, SIGNAL('clicked()'), self.startOperation)
        self.setTitle(operation.label)
        
        for name,param in operation.params.items():
            # TODO: replace QSpinBox with Kevin's numpad code
            widget = QSpinBox()
            widget.setValue(param['value'])
            widget.setMinimum(param['min'])
            widget.setMaximum(param['max'])
            paramLayout.addRow(QLabel(param['label']), widget)
             

    def startOperation(self):
        """ Notify parent view when operation is started
        """
        self.emit(SIGNAL('startOperation(PyQt_PyObject)'),self.operation)
