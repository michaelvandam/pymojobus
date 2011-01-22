
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class DeviceIconViewFactory():
    """ Factory class for DeviceIconView subclasses.
    @cvar viewClasses   dict    Dictionary of class names
                                (indexed by device type)
    """

    viewClasses = {'PRM':'PRMIconView', 'RDM':'RDMIconView', }
    
    @classmethod
    def getView (cls, device):
        type = device['deviceType']
        # TODO: elegant approach not working?  Go with if/else
        #view = self.viewClasses[type](device)
        if type == 'PRM':
            return PRMIconView(device)
        elif type == 'RDM':
            return RDMIconView(device)
        else:
            # TODO: Raise exception
            return None
            
        return view
        

class DeviceIconView(QWidget):
    """ Base class for view icon representing state of a device
    @ivar device    obj     Device attached to this view
    @ivar address   str     Address of the device
    @ivar layout    obj     Layout containing the elements of the view
    """

    def __init__(self, device, parent=None):
        QWidget.__init__(self)
        self.device = device
        self.address = device['address']
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Address: %s" % self.address))
        self.layout.addWidget(QLabel("Type: %s" % self.device['deviceType']))
        self.unsetActive()

    # TODO: Need a better way to do highlighting!
    def setActive(self):
        self.setStyleSheet("QWidget { background-color: white }")

    # TODO: Need a better way to do highlighting!
    def unsetActive(self):
        self.setStyleSheet('')

    def updateView(self):
        # TODO: link to state update of underlying device
        pass
        
class RDMIconView(DeviceIconView):
    def __init__(self,device,parent=None):
        DeviceIconView.__init__(self, device)

# TODO: model the low-level part from mojodeviceview and specific
# subclasses
        
class PRMIconView(DeviceIconView):
    
    def __init__(self, device, parent=None):
        DeviceIconView.__init__(self, device)
        # State represented
        self.currTemp = 0
        self.setTemp = 0
        self.heaterOn = False
        self.coolerOn = False   
        self.xPosition = 0
        self.zPosition = 0
        self.stirSpeed = 0
        self.xferGasOn = False
        self.evapGasOn = False
        self.cartridgeValve = "Waste"

