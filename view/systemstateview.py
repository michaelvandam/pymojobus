
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from deviceiconview import *
from view.util.clickable import *

class SystemStateView(QGroupBox):

    """ View of the system state
    @ivar deviceViews       dict    Dictionary of views representing devices
                                    (indexed by device address)
    @ivar devicesLayout     obj     Layout that holds device views
    @ivar activeDevice      str     Address of active device or None
    @ivar activeOperation   obj     Active operation or None
    @ivar selectedDevice    str     Address of selected device or None
    @ivar statusWidget      str     Widget displaying the status
    """
      
    def __init__(self, parent=None):
        QGroupBox.__init__(self)
        self.deviceViews = {}
        self.activeDevice = None
        self.selectedDevice = None
        self.activeOperation = None
        self.setTitle("System State")
        layout = QVBoxLayout()
        self.setLayout(layout)
        # TODO: Replace with more extensive display of connection status
        layout.addWidget(QLabel("Connection Status"))
        self.devicesLayout = QHBoxLayout()
        layout.addLayout(self.devicesLayout)
        # TODO: Replace with widget that will display current activity of active device
        self.statusWidget = QLabel()
        layout.addWidget(self.statusWidget)
            
    def clearDevices(self):
        # Assume there is no active operation
        self.setSelectedDevice(None)
        for view in self.deviceViews.values():
            self.devicesLayout.removeWidget(view)
            view.setParent(None)        # Needed to actually remove
        self.deviceViews.clear()
    
    def loadDevices(self, devices={}):
        self.devices = devices
        for address,device in self.devices.items():
            deviceView = DeviceIconViewFactory().getView(device)
            self.deviceViews[address] = deviceView
            # NOTE: 'clickable' is from view/util
            # Lambda function details here:
            # http://stackoverflow.com/questions/4578861/connecting-slots-and-signals-in-pyqt4-in-a-loop
            clickable(deviceView).connect(lambda address=address: self.slotSelectDevice(address))
            self.devicesLayout.addWidget(deviceView)

    # Signal handlers

    def slotStatusChanged(self, status):
        self.statusWidget.setText("Status: " + status)
    
    def slotSelectDevice(self, address):
        """ Send a signal to the MainWindow that the active device has changed
        """
        #if self.selectedDevice != address:  # Removed to always update
        self.emit(SIGNAL('deviceSelected(PyQt_PyObject)'),address)

    def setSelectedDevice(self, address):
        #if self.selectedDevice != address:  # Removed to force redraw always
            if self.selectedDevice != None:
                self.deviceViews[self.selectedDevice].setSelected(False)
            if address != None:
                self.deviceViews[address].setSelected(True)
            self.selectedDevice = address            
            
    def slotOperationStarted(self, operation):
        self.activeOperation = operation
        self.activeDevice = operation.device['address']
        self.deviceViews[self.activeDevice].setActive(True)
    
    def slotOperationFinished(self, operation):
        if self.activeOperation != operation:
            # TODO: Raise exception
            print "ERROR(SystemStateView): finished operation != active operation"
        self.deviceViews[self.activeDevice].setActive(False)
        self.activeOperation = None
        self.activeDevice = None
