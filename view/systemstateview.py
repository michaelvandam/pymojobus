
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from deviceiconview import *
from viewutil import *

class SystemStateView(QGroupBox):
    """ View of the system state
    @ivar deviceViews   dict    Dictionary of views representing devices
                                (indexed by device address)
    @ivar devicesLayout obj     Layout that holds device views
    @ivar activeDevice  str     Address of active device or None
    """
      
    def __init__(self, parent=None):
        QGroupBox.__init__(self)
        self.deviceViews = {}
        self.activeDevice = None
        self.setTitle("System State")
        layout = QVBoxLayout()
        self.setLayout(layout)
        # TODO: Replace with more extensive display of connection status
        layout.addWidget(QLabel("Connection Status"))
        self.devicesLayout = QHBoxLayout()
        layout.addLayout(self.devicesLayout)
        # TODO: Replace with widget that will display current activity
        # of active device
        layout.addWidget(QLabel("Status Message"))
            
    def clearDevices(self):
        self.setActiveDevice(None)      # Do this first to avoid pointer errors
        for address, view in self.deviceViews.items():
            self.devicesLayout.removeWidget(view)
            view.setParent(None)        # Needed to actually remove
        self.deviceViews.clear()
    
    def loadDevices(self, devices={}):
        self.devices = devices
        for address,device in self.devices.items():
            deviceView = DeviceIconViewFactory().getView(device)
            self.deviceViews[address] = deviceView
            # NOTE: 'clickable' is from viewutil
            # Lambda function details here:
            # http://stackoverflow.com/questions/4578861/connecting-slots-and-signals-in-pyqt4-in-a-loop
            clickable(deviceView).connect(lambda address=address: self.slotSelectDevice(address))
            self.devicesLayout.addWidget(deviceView)
            
    def slotSelectDevice(self, address):
        """ Send a signal to the MainWindow that the active device has changed
        """
        if self.activeDevice != address:
            self.emit(SIGNAL('activeDeviceChanged(PyQt_PyObject)'),address)
            # NOTE: we are passing 'address' as a str object
            # http://www.riverbankcomputing.com/static/Docs/PyQt4/pyqt4ref.html#the-pyqt-pyobject-signal-argument-type
        
    def setActiveDevice(self, address):
        if self.activeDevice != address:
            if self.activeDevice != None:
                self.deviceViews[self.activeDevice].unsetActive()
            if address != None:
                self.deviceViews[address].setActive()
            self.activeDevice = address