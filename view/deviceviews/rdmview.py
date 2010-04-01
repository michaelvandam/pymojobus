import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from utils.mojodeviceview import DeviceView
import logging

errlog = logging.getLogger("mojo.error")
log = logging.getLogger()

NUMOFRESERVOIRS = 4

class Reservoir(object):
    def __init__(self, id):
        self.id = id+1
    def __str__(self):
        return "Reservoir %d" % (self.id)
        
class ReservoirButton(QPushButton):
    def __init__(self, reservoir, parent = None):
        text = str(reservoir)
        super(ReservoirButton, self).__init__(text,parent)
        #self.setCheckable(True)
        #self.setAutoExclusive(True)
        self.reservoir = reservoir

class RDMView(DeviceView):
    deviceType = "RDM"
    def __init__(self, rdmModel=None, parent=None, *args, **kwargs):
        DeviceView.__init__(self, parent=parent, deviceModel=rdmModel)            
        
        self.reservoirs = [Reservoir(i) for i in range(NUMOFRESERVOIRS)]

        self.reservoirButtons = [ReservoirButton(res) for res in self.reservoirs]
        self.reservoirCleanButtons = [ReservoirButton(res) for res in self.reservoirs]
        
        self.buttons = [] + self.reservoirButtons + self.reservoirCleanButtons
        #self.buttonGroup = QButtonGroup()
        #self.buttonGroup.setExclusive(True)
        
        #Deliver Buttons
        deliverGroup = QGroupBox("Deliver")
        deliverLayout = QHBoxLayout()
        for r in self.reservoirButtons:
            deliverLayout.addWidget(r)
            self.connect(r, SIGNAL("clicked()"), self.runDeliver)
            #self.buttonGroup.addButton(r)
        deliverGroup.setLayout(deliverLayout)
        
        #Clean Buttons
        self.cleanGroup = QGroupBox("Clean")
        cleanLayout = QHBoxLayout()
        for r in self.reservoirCleanButtons :
            cleanLayout.addWidget(r)
            self.connect(r, SIGNAL("clicked()"), self.runClean)
            #self.buttonGroup.addButton(r)
        self.cleanGroup.setLayout(cleanLayout)
        self.cleanGroup.setDisabled(True)
        #Load And Done Buttons
        operationGroup = QGroupBox("")
        operationLayout = QHBoxLayout()
        self.loadButton = QPushButton("Load")
        self.buttons.append(self.loadButton)
        #self.buttonGroup.addButton(self.loadButton)
        #self.loadButton.setCheckable(True)
        #self.loadButton.setAutoExclusive(True)
        self.doneButton = QPushButton("Done")
        self.buttons.append(self.doneButton)
        #self.buttonGroup.addButton(self.doneButton)
        #self.doneButton.setCheckable(True)
        #self.doneButton.setAutoExclusive(True)
        operationLayout.addWidget(self.loadButton)
        operationLayout.addWidget(self.doneButton)
        operationGroup.setLayout(operationLayout)
        
        
        onWasteLabel = QLabel("On")
        offWasteLabel = QLabel("Off")
        wasteOnOffGroup = QGroupBox("Waste")
        wasteOnOffLayout = QHBoxLayout()
        wasteOnOffGroup.setLayout(wasteOnOffLayout)
        self.wasteOnButton = QRadioButton()
        self.wasteOffButton = QRadioButton()
        self.wasteOffButton.setChecked(True)
        wasteOnOffLayout.addWidget(onWasteLabel)
        wasteOnOffLayout.addWidget(self.wasteOnButton)
        wasteOnOffLayout.addWidget(offWasteLabel)
        wasteOnOffLayout.addWidget(self.wasteOffButton)
        
        purgeGroup = QGroupBox("")
        purgeLayout = QHBoxLayout()
        self.purgeButton = QPushButton("Purge / Dry")
        self.buttons.append(self.purgeButton)
        purgeLayout.addWidget(self.purgeButton)
        purgeGroup.setLayout(purgeLayout)
        
        layout = QGridLayout()
        layout.addWidget(deliverGroup, 0, 0)
        layout.addWidget(operationGroup, 1, 0)
        layout.addWidget(wasteOnOffGroup,2,0)
        layout.addWidget(self.cleanGroup, 3, 0)
        layout.addWidget(purgeGroup, 4, 0)

        self.setLayout(layout)

        self.connect(self.loadButton, SIGNAL("clicked()"), self.runLoad)
        self.connect(self.doneButton, SIGNAL("clicked()"), self.runDone)
        self.connect(self.wasteOnButton, SIGNAL("clicked()"), self.runWasteOn)
        self.connect(self.wasteOffButton, SIGNAL("clicked()"), self.runWasteOff)
        self.connect(self.purgeButton, SIGNAL("clicked()"), self.runPurge)
        
    def runPurge(self):
        self.model.goPurge()
        
    def runWasteOn(self):
        self.model.goWasteOpen()
    
    def runWasteOff(self):
        self.model.goWasteClose()
    
    def runDone(self):
        self.model.goStandby()
    
    def runLoad(self):
        self.model.goLoad()
    
    def runDeliver(self):
        rid = self.sender().reservoir.id
        self.model.goDeliver(rid)
        
    def runClean(self):
        rid = self.sender().reservoir.id
        self.model.goClean(rid)
        
    def updateView(self):
        log.debug("Update view %s" % self.model.name)
        for b in self.buttons:
            b.setDown(False)
        if self.model.state == self.model.STANDBY:
            self.doneButton.setDown(True)
            self.cleanGroup.setDisabled(False)
        if self.model.state == self.model.LOAD:
            self.loadButton.setDown(True)
            self.cleanGroup.setDisabled(False)
        else:
            self.cleanGroup.setDisabled(True)
            
        if self.model.state == self.model.DELIVER:
            log.debug("Go deliver view! %s" % self.model.name)
            log.debug("Selected reagent %d" % self.model.selectedReservoir.id)
            self.reservoirButtons[self.model.selectedReservoir.id - 1].setDown(True)
        
        if self.model.cleanState==self.model.CLEAN:
            log.debug("Go clean view! %s" % self.model.name)
            log.debug("Selected clean reagent %d" % self.model.selectedCleanReservoir.id)
            self.reservoirCleanButtons[self.model.selectedCleanReservoir.id - 1].setDown(True)
        
        if self.model.state == self.model.PURGE:
            log.debug("Go purge view! %s" % self.model.name)
            log.debug("Selected reagent ALL")
            self.purgeButton.setDown(True)

def main(argv):
    pass
            
if __name__ == '__main__':
    main(sys.argv)
    app = QApplication([])
    form = RDMView()
    form.show()
    app.exec_()