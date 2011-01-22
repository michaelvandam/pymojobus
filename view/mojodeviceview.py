import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logging

log = logging.getLogger()
errlog = logging.getLogger("mojo.error")

class DeviceView(QDialog):
        deviceType = "Default"
        def __init__(self, deviceModel=None, parent=None, *args, **kwargs):
            QDialog.__init__(self, parent)
            self.model = deviceModel
            self.connect(self, SIGNAL("updateDevice"), self.updateDevice)
            
            if self.model:
                self.setWindowTitle(self.model.name)
                self.attachSignal()
            else:
                self.setWindowTitle(self.deviceType)
                
            self.connect(self, SIGNAL("updateDevice"), self.updateView)
            
        def attachSignal(self):
            log.debug("Attach updateDevice signal to %s" % self.model.name)
            self.model.processResponse1 = self.model.processResponse
            def f(*args):
                self.model.processResponse1(*args)
                log.debug("Emit updateDevice signal for %s" % self.model.name)
                self.emit(SIGNAL("updateDevice"))
            
            self.model.processResponse = f
                
        def updateDevice(self):
            pass
            #self.statusLabel.setText(self.deviceModel.stateText)
        
        def insertProcessResponse(self):
            pass
            #self.emit(SIGNAL("updateDevice"))
        
        def getName(self):
            if self.model:
                return "%s @ %s" % (self.deviceType, self.model.address)
            else:
                return self.deviceType
        
        def updateView(self):
            log.debug("Update view for %s" % self.model.name)
        
        name = property(getName)
        
        
def main(argv):
    app = QApplication(argv)
    form = DeviceView()
    form.show()
    app.exec_()
            
if __name__ == '__main__':
    main(sys.argv)