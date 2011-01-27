
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
        type = device.deviceType
        # TODO: elegant approach not working?  Go with if/else
        #view = cls.viewClasses[type](device)
        if type == 'PRM':
            return PRMIconView(device)
        elif type == 'RDM':
            return RDMIconView(device)
        else:
            # TODO: Raise exception
            return None
            
        return view
        

class DeviceIconView(QGroupBox):
    """ Base class for view icon representing state of a device
    @ivar device        obj     Device attached to this view
    @ivar address       str     Address of the device
    @ivar layout        obj     Layout containing the elements of the view
    @ivar isActive      bool    True if device is active (running a unit op)
    @ivar isSelected    bool    True if device is selected
    """

    def __init__(self, device, parent=None):
        QGroupBox.__init__(self)
        self.device = device
        self.address = device.address
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Address: %s" % self.address))
        self.layout.addWidget(QLabel("Type: %s" % self.device.deviceType))
        self.isActive = False
        self.isSelected = False

    def setActive(self, bool=True):
        self.isActive = bool
        if bool:
            self.setStyleSheet("background-color: yellow")
        else:
            if self.isSelected:
                self.setStyleSheet("background-color: green")
            else:
                self.setStyleSheet('')
            
    def setSelected(self, bool=True):
        self.isSelected = bool
        if bool:
            self.setStyleSheet("background-color: green")
        else:
            if self.isActive:
                self.setStyleSheet("background-color: yellow")
            else:
                self.setStyleSheet('')

    def updateView(self):
        # TODO: link this method to state update of underlying device
        pass

# TODO: implement some dummy view (real RDM implementation not needed now)        
class RDMIconView(DeviceIconView):
    def __init__(self,device,parent=None):
        DeviceIconView.__init__(self, device)

# TODO: finish from Henry's PRMView code
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

