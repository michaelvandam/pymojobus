import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from utils.mojodeviceview import DeviceView
import logging
        
errlog = logging.getLogger("mojo.error")
log = logging.getLogger()

class PRMView(DeviceView):
    deviceType = "PRM"
    def __init__(self, prmModel=None, parent=None, *args, **kwargs):
        DeviceView.__init__(self, parent=parent, deviceModel=prmModel)            
        
        
        # Temperature Controls
        tempGroup = QGroupBox("Temperature")
        
        #tempStatusGroup = QGroupBox("Status")
        #tempStatusLayout = QGridLayout()
        #tempStatusGroup.setLayout(tempStatusLayout)
        tempLayout = QGridLayout()
        tempGroup.setLayout(tempLayout)
        #heatGroup = QGroupBox("Heat")
        #heatLayout = QGridLayout()
        #heatGroup.setLayout(heatLayout)
        coolGroup = QGroupBox("Cool")
        coolLayout = QGridLayout()
        coolGroup.setLayout(coolLayout)
        #tempLayout.addWidget(tempStatusGroup)
        #tempLayout.addWidget(heatGroup)
        tempLayout.addWidget(coolGroup)
        tempGroup.setCheckable(True)
        
        #currentTempLabel = QLabel("Current Temperature:")
        #self.currentTempLabel = QLabel("25\xB0C")
        #currentTempLabel.setBuddy(self.currentTempLabel)
        #tempStatusLayout.addWidget(currentTempLabel, 0, 0)
        #tempStatusLayout.addWidget(self.currentTempLabel, 0,1)
        
        #setPointLayout  = QHBoxLayout()
        #tempDial = QDial()
        #tempDial.setNotchesVisible(True)
        #tempDial.setNotchTarget(20)
        #self.tempSpinbox = QDoubleSpinBox()
        #self.tempSpinbox.setRange(25.0,200.0)
        #tempDial.setRange(25.0,200.0)
        #self.tempSpinbox.setSingleStep(0.5)
        #self.tempSpinbox.setSuffix(u"\xB0C")
        #self.connect(tempDial, SIGNAL('valueChanged(int)'), self.tempSpinbox.setValue)
        #self.connect(self.tempSpinbox, SIGNAL('valueChanged(int)'), tempDial.setValue)
        #setPointLayout.addWidget(tempDial)
        #setPointLayout.addWidget(self.tempSpinbox)
        
        #onHeatLabel = QLabel("On")
        #offHeatLabel = QLabel("Off")
        #heatOnOffGroup = QGroupBox()
        #heatOnOffLayout = QHBoxLayout()
        #heatOnOffGroup.setLayout(heatOnOffLayout)
        #heatOnButton = QRadioButton()
        #heatOffButton = QRadioButton()
        #heatOffButton.setChecked(True)
        #heatOnOffLayout.addWidget(onHeatLabel)
        #heatOnOffLayout.addWidget(heatOnButton)
        #heatOnOffLayout.addWidget(offHeatLabel)
        #heatOnOffLayout.addWidget(heatOffButton)
        
        onCoolLabel = QLabel("On")
        offCoolLabel = QLabel("Off")
        coolOnOffGroup = QGroupBox()
        coolOnOffLayout = QHBoxLayout()
        coolOnOffGroup.setLayout(coolOnOffLayout)
        self.coolOnButton = QRadioButton()
        self.coolOffButton = QRadioButton()
        self.coolOffButton.setChecked(True)
        coolOnOffLayout.addWidget(onCoolLabel)
        coolOnOffLayout.addWidget(self.coolOnButton)
        coolOnOffLayout.addWidget(offCoolLabel)
        coolOnOffLayout.addWidget(self.coolOffButton)
        
        
        #heatLayout.addLayout(setPointLayout,0,0)
        #heatLayout.addWidget(heatOnOffGroup,1,0)
        coolLayout.addWidget(coolOnOffGroup)
        
        
        
        #Stir Controls
        stirGroup = QGroupBox("Stir")
        stirGroup.setCheckable(True)
        stirLayout = QHBoxLayout()
        stirGroup.setLayout(stirLayout)
        stirDial = QDial()
        stirDial.setNotchesVisible(True)
        stirDial.setNotchTarget(50)
        self.stirSpeedSpinBox = QSpinBox()
        self.stirSpeedSpinBox.setSuffix("")
        stirDial.setRange(0,255)
        self.stirSpeedSpinBox.setRange(0,255)
        stirLayout.addWidget(stirDial)
        stirLayout.addWidget(self.stirSpeedSpinBox)
        self.connect(stirDial, SIGNAL('valueChanged(int)'), self.stirSpeedSpinBox.setValue)
        self.connect(self.stirSpeedSpinBox, SIGNAL('valueChanged(int)'), stirDial.setValue)
        self.stirButton = QPushButton("Set Speed")
        stirLayout.addWidget(self.stirButton)
        
        #Motion Controls
        motionGroup = QGroupBox("Motion")
        #motionGroup.setExclusive(True)
        motionLayout = QVBoxLayout()
        zGroup = QGroupBox("Up/Down")
        #zGroup.setExclusive(True)
        zLayout = QHBoxLayout()
        zGroup.setLayout(zLayout)
        xGroup = QGroupBox("Positions")
        #xGroup.setExclusive(True)
        xLayout = QHBoxLayout()
        xGroup.setLayout(xLayout)
        #rGroup = QGroupBox()
        #rLayout = QHBoxLayout()
        #rGroup.setLayout(rLayout)
        
        motionLayout.addWidget(zGroup)
        motionLayout.addWidget(xGroup)
        #motionLayout.addWidget(rGroup)
        motionGroup.setLayout(motionLayout)
        layout = QGridLayout()
        
    
        #Transfer Control Group
        transferLayout = QGridLayout()
        transferGroup = QGroupBox("Transfer")
        onTransferLabel = QLabel("On")
        offTransferLabel = QLabel("Off")
        transferOnOffLayout = QHBoxLayout()
        transferGroup.setLayout(transferOnOffLayout)
        self.transferOnButton = QRadioButton()
        self.transferOffButton = QRadioButton()
        self.transferOffButton.setChecked(True)
        transferOnOffLayout.addWidget(onTransferLabel)
        transferOnOffLayout.addWidget(self.transferOnButton)
        transferOnOffLayout.addWidget(offTransferLabel)
        transferOnOffLayout.addWidget(self.transferOffButton)
        transferLayout.addWidget(transferGroup)
        
        layout.addWidget(motionGroup,0,0)
        layout.addWidget(transferGroup,1,0)
        layout.addWidget(tempGroup,2,0)
        layout.addWidget(stirGroup,3,0)
        
        # Motion Buttons
        self.sealButton = QPushButton("Seal")
        self.sealButton.setAutoExclusive(True)
        self.openButton = QPushButton("Open")
        self.openButton.setAutoExclusive(True)
        zLayout.addWidget(self.openButton)
        zLayout.addWidget(self.sealButton)
        
        self.position1Button=QPushButton("1")
        self.position1Button.setAutoExclusive(True)
        self.position2Button=QPushButton("2")
        self.position1Button.setAutoExclusive(True)
        self.position3Button=QPushButton("3")
        self.position1Button.setAutoExclusive(True)
        xLayout.addWidget(self.position1Button)
        xLayout.addWidget(self.position2Button)
        xLayout.addWidget(self.position3Button)
        
        
        #self.resetButton =QPushButton("Reset")
        #rLayout.addWidget(self.resetButton)
        
        self.setLayout(layout)
        
        self.connect(self.position1Button, SIGNAL("clicked()"), self.runMoveXPos1)
        self.connect(self.position2Button, SIGNAL("clicked()"), self.runMoveXPos2)
        self.connect(self.position3Button, SIGNAL("clicked()"), self.runMoveXPos3)
        self.connect(self.openButton, SIGNAL("clicked()"), self.runMoveZDown)
        self.connect(self.sealButton, SIGNAL("clicked()"), self.runMoveZUp)
        #self.connect(self.resetButton, SIGNAL("clicked()"), self.runReset)
        self.connect(self.transferOnButton, SIGNAL("clicked()"), self.runTransferOn)
        self.connect(self.transferOffButton, SIGNAL("clicked()"), self.runTransferOff)
        self.connect(self.coolOnButton, SIGNAL("clicked()"), self.runCoolOn)
        self.connect(self.coolOffButton, SIGNAL("clicked()"), self.runCoolOff)
        self.connect(self.stirButton, SIGNAL("clicked()"), self.runStir)
        
    #def runReset(self):
    #    self.model.goReset()
    
    def runStir(self):
        speed = int(self.stirSpeedSpinBox.value())
        self.model.goMix(speed)
        
    def runCoolOn(self):
        self.model.goCoolOn()
    
    def runCoolOff(self):
        self.model.goCoolOff()

    def runTransferOn(self):
        self.model.goTransferOn()
    
    def runTransferOff(self):
        self.model.goTransferOff()
    
    def runMoveXPosHome(self):
        self.model.goMoveXHome()
        
    def runMoveXPos1(self):
        self.model.goMoveX(1)
    
    def runMoveXPos2(self):
        self.model.goMoveX(2)
    
    def runMoveXPos3(self):
        self.model.goMoveX(3)
    
    
    def runMoveZUp(self):
        self.model.goMoveZUp()
        
    def runMoveZDown(self):
        self.model.goMoveZDown()
        
    def _allZUp(self):
        self.openButton.setDown(False)
        self.sealButton.setDown(False)
    
    def _allXUp(self):
        self.position1Button.setDown(False)
        self.position2Button.setDown(False)
        self.position3Button.setDown(False)
    
    def _disableZ(self):
        self.openButton.setDisabled(True)
        self.sealButton.setDisabled(True)
    
    def _disableX(self):
        self.position1Button.setDisabled(True)
        self.position2Button.setDisabled(True)
        self.position3Button.setDisabled(True)
    
    def _disableAll(self):
        self._disableX()
        self._disableZ()
        
    def _enableAll(self):
        self.position1Button.setDisabled(False)
        self.position2Button.setDisabled(False)
        self.position3Button.setDisabled(False)
        self.openButton.setDisabled(False)
        self.sealButton.setDisabled(False)
    
    def updateView(self):
        
        
        log.debug("Update view %s" % self.model.name)
        
        self._allXUp()
        self._allZUp()
        
        if self.model.xState == self.model.BUSY:
            log.debug("%s Show X BUSY" % self.model.name)
            self._disableAll()
        elif self.model.zState == self.model.BUSY:
            log.debug("%s Show Z BUSY" % self.model.name)
            self._disableAll()
        else:
            self._enableAll()
            
        # Deal with X Position

        
        if self.model.xState == self.model.XERR:
            log.debug("%s Show XERR" % self.model.name)
            #self._enableAll()
            # Un Grey Buttons!
            
        elif self.model.xState == self.model.HOME:
            log.debug("%s Show HOME" % self.model.name)
            self.position1Button.setDown(True)
            
        elif self.model.xState == self.model.xpositions[1]:
            log.debug("%s Show POS 1" % self.model.name)
            self.position1Button.setDown(True)
            
        elif self.model.xState == self.model.xpositions[2]:
            log.debug("%s Show POS 2" % self.model.name)
            self.position2Button.setDown(True)
            
        elif self.model.xState == self.model.xpositions[3]:
            log.debug("%s Show POS 3" % self.model.name)
            self.position3Button.setDown(True)
    
        # Deal with Z Postion
        
            
        if self.model.zState == self.model.UP:
            log.debug("%s Show UP" % self.model.name)
            self.sealButton.setDown(True)
            self._disableX()
            
        elif self.model.zState == self.model.DOWN:
            log.debug("%s Show DOWN" % self.model.name)
            self.openButton.setDown(True)
            
        elif self.model.zState == self.model.ZERR:
            log.debug("%s Show ZERR" % self.model.name)


def main(argv):
    pass
            
if __name__ == '__main__':
    main(sys.argv)
    app = QApplication([])
    form = PRMView()
    form.show()
    app.exec_()