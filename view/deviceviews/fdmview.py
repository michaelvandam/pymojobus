import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from utils.mojodeviceview import DeviceView
import logging
from threading import Event
    
errlog = logging.getLogger("mojo.error")
log = logging.getLogger()
class OnOffSwitch(QGroupBox):
    def __init__(self, title, parent=None):
        QGroupBox.__init__(self, title, parent)
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        onLabel = QLabel("On")
        offLabel = QLabel("Off")
        
        self.slide = QSlider()
        self.slide.setOrientation(Qt.Vertical)
        self.slide.setRange(0,1)
        self.slide.setFixedSize(30,25)
        
        layout.addWidget(onLabel,0,0)
        layout.addWidget(offLabel,2,0)
        layout.addWidget(self.slide,1,0)

        self.setFixedSize(80,100)
        
        self.connect(self.slide, SIGNAL("valueChanged(int)"), self.stateChanged)
        
    def stateChanged(self):
        if int(self.slide.value()) == 1:
            self.emit(SIGNAL("turnOn"))
        else:
            self.emit(SIGNAL("turnOff"))
    def setOn(self):
        self.slide.setValue(1)
    
    def setOff(self):
        self.slide.setValue(0)
        
    def lock(self):
        self.slide.setDisabled(True)

    def unlock(self):
        self.slide.setDisabled(False)

        
class FDMView(DeviceView):
    deviceType = "FDM"
    def __init__(self, fdmModel=None, parent=None, *args, **kwargs):
        DeviceView.__init__(self, parent=parent, deviceModel=fdmModel)            
        
    
    def updateView(self):
        log.debug("Update view %s" % self.model.name)
        


            
if __name__ == '__main__':
    main(sys.argv)
    app = QApplication([])
    form = FDMView()
    form.show()
    app.exec_()