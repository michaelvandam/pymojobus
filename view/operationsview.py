
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
from view.util.clickable import *
from operation.unitoperation import UnitOperation


class OperationsView(QGroupBox):

    """ Displays and controls unit operations for devices in the system.
        The view constructs a DeviceOperationsView for each device in
        the system, showing only the activeDevice.
        
    @ivar activeDevice      str     Address of active device (or None)
    @ivar selectedDevice    str     Address of selected device (or None)
    @ivar activeOperation   obj     Active operation (or None)
    @ivar devices           dict    Dictionary of all devices
                                    (indexed by address)
    @ivar views             dict    Dictionary of all DeviceOperationViews
                                    (indexed by address)
    @ivar emptyView         obj     View to display if activeDevice == None
    @ivar layout            obj     Layout that holds DeviceOperationViews
    
    """
    
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)
        self.devices = {}
        self.views = {}
        self.activeDevice = None
        self.selectedDevice = None
        self.activeOperation = None
        self.selectedOperation = None
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
        self.setSelectedDevice(None)
        for view in self.views.values():
            self.layout.removeWidget(view)
            view.setParent(None)    # Needed to actually remove
        self.devices.clear()
        self.views.clear()
        self.emptyView.show()
        
    def loadDevices(self, devices={}):
        self.devices = devices
        for address,device in self.devices.items():
            view = DeviceOperationsView(device)
            view.hide()
            self.views[address] = view
            self.layout.addWidget(view)
            self.connect(view, SIGNAL("startOperation(PyQt_PyObject)"), self.slotStartOperation)
            self.connect(view, SIGNAL("operationSelected(PyQt_PyObject)"), self.setSelectedOperation)

    def setSelectedDevice(self, address):
        old = self.selectedDevice
        new = address
        if old != new:
            if old != None:
                # Hide previously selected view
                self.views[old].hide()
            if new == None:
                # Show empty view
                self.emptyView.show()
            else:
                # Show newly selected view
                self.emptyView.hide()
                self.views[new].show()
            self.selectedDevice = address

    def setSelectedOperation(self, operation):
        old = self.selectedOperation
        new = operation
        if old != None:
            self.views[old.device.address].setSelectedOperation(operation,False)
        if new != None:
            self.views[new.device.address].setSelectedOperation(operation,True)
        self.selectedOperation = operation
    
    def slotOperationStarted(self, operation):
        if operation != None:
            self.activeOperation = operation
            self.activeDevice = operation.device.address
            self.views[self.activeDevice].slotOperationStarted(operation)
            self.disable()

    def slotOperationFinished(self, operation):
        if operation != self.activeOperation:
            # TODO: raise exception
            print "ERROR(OperationsView): finished operation != started operation"
        self.views[self.activeDevice].slotOperationFinished(operation)
        self.activeOperation = None
        self.activeDevice = None
        self.enable()            

    def slotStartOperation(self, operation):
        """ Notify parent that an operation has been initiated
        """
        self.emit(SIGNAL("startOperation(PyQt_PyObject)"), operation)


class EmptyOperationsView(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setText("No active device selected")


class DeviceOperationsView(QWidget):

    """ Base class for showing/controlling the available operations for a device.
    @ivar device    obj     Device connected to this view
    @ivar layout    obj     Layout that holds device operations
    @ivar views     dict    Dictionary of operation views, indexed by object id
    """
    
    def __init__(self, device, parent=None):
        QWidget.__init__(self, parent)
        self.device = device
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.views = {}
        self._populateOperations()
    
    def _populateOperations(self):
        config = self.device.config['UnitOperations']
        for opname in config.keys():
            self._addOperation(UnitOperation(self.device, opname))
        
    def _addOperation(self,operation):
        view = UnitOperationEditView(operation)
        self.views[operation.name] = view
        self.layout.addWidget(view)
        self.connect(view, SIGNAL("startOperation(PyQt_PyObject)"), self.slotStartOperation)
        clickable(view).connect(lambda operation=operation: self.slotSelectOperation(operation))

    # Signal handlers   

    def slotSelectOperation(self, operation):
        self.emit(SIGNAL('operationSelected(PyQt_PyObject)'), operation)
    
    def setSelectedOperation(self, operation, bool):
        # Note the operation may not be in this particular view
        if (operation != None) and operation.name in self.views:
            self.views[operation.name].setSelected(bool)
        
    def slotStartOperation(self, operation):
        """ Notify parent that an operation has been initiated
        """
        self.emit(SIGNAL("startOperation(PyQt_PyObject)"), operation)

    def slotOperationStarted(self, operation):
        if operation.name in self.views:
            self.views[operation.name].setActive(True)
            
    def slotOperationFinished(self, operation):
        if operation.name in self.views:
            self.views[operation.name].setActive(False)
    
 
class UnitOperationEditView(QGroupBox):
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
        self.setTitle(operation.getLabel())
        
        params = operation.getParams()
        config = operation.config['Params']
        for name in operation.params.keys():
            if config[name]['type'] == "string":
                widget = QLineEdit()
                widget.setText(params[name])
            else:
                # TODO: replace QSpinBox with Kevin's numpad code
                widget = QSpinBox()
                widget.setValue(params[name])
                widget.setMinimum(config[name]['min_value'])
                widget.setMaximum(config[name]['max_value'])
            paramLayout.addRow(QLabel(config[name]['label']), widget)
             

    # TODO: need to implement capturing of the data into the self.operation
    # How to do this?  Use 'Qt.AcceptRole' buttons?
    def startOperation(self):
        """ Capture all the data the user has entered and
            notify parent view to start the operation.
        """
        self.emit(SIGNAL('startOperation(PyQt_PyObject)'),self.operation)

    def setActive(self, bool=True):
        if bool:
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet('')

    def setSelected(self, bool=True):
        if bool:
            self.setStyleSheet("background-color: green")
        else:
            self.setStyleSheet('')
            
