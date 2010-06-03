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


class TransferController(OnOffSwitch):
    def __init__(self,title="Transfer",parent=None):
        OnOffSwitch.__init__(self,title,parent)

class AUXController(OnOffSwitch):
    def __init__(self,title="AUX",parent=None):
        OnOffSwitch.__init__(self,title,parent)
    

class WasteController(OnOffSwitch):
    def __init__(self,title="Waste",parent=None):
        OnOffSwitch.__init__(self,title,parent)
        self.setOn()


class StirController(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self,parent)
        self.setTitle("Stir Speed")
        layout = QGridLayout()
        self.setLayout(layout)
        self.values = [0,115,120,130,140,160,180,200,220,240,255]
        self.dial = QDial()
        self.dial.setFixedSize(60,60)
        self.dial.setNotchesVisible(True)
        self.dial.setNotchTarget(1)
        self.dial.setRange(0,10)
        self.stirLabel = QLabel("0")
        layout.addWidget(self.dial,0,0)
        layout.addWidget(self.stirLabel,0,1)
        self.connect(self.dial,SIGNAL('valueChanged(int)'), self.stirChanged)
        self.setFixedSize(100,100)
    def getValue(self):
        return self.values[int(self.dial.value())]
        
    def getDialValue(self):
        return int(self.dial.value())
        
    def stirChanged(self):
        self.stirLabel.setText("%d" % self.getDialValue())
        self.emit(SIGNAL('stirSpeedChanged'))
        

class TimeSelector(QGroupBox):
    def __init__(self, parent=None, *args, **kwargs):
        QGroupBox.__init__(self, parent)
        
        layout = QGridLayout()
        self.setLayout(layout)
        self.setTitle("Timer")
        
        self.time = QTime()
        
        self.clockStart = Event()
        
        hourLabel = QLabel("Hours")
        self.hours = QSpinBox()
        self.hours.setRange(0,300)
        minLabel = QLabel("Minutes")
        self.minutes = QSpinBox()
        self.minutes.setRange(0,60)
        secLabel = QLabel("Seconds")
        self.seconds = QSpinBox()
        self.seconds.setRange(0,60)
        self.resetTimeButton = QPushButton("Set Time")
        
        self.currentTime = QLabel()
        self.currentTime.setAlignment(Qt.AlignHCenter)
        self.startButton = QPushButton("Start")
        self.stopButton = QPushButton("Stop")
        self.tempTimer = QTimer()
        self.tempTimer.setInterval(1000)
        self.tempTimer.stop()

        self.status = QLabel("Stopped")
        self.status.setAlignment(Qt.AlignHCenter)
        
        timeGroup = QGroupBox("Timer")
        layout.addWidget(self.status,0,0,1,3)
        layout.addWidget(self.currentTime,1,0,1,3)
        layout.addWidget(hourLabel,2,0)
        layout.addWidget(minLabel,2,1)
        layout.addWidget(secLabel,2,2)
        layout.addWidget(self.hours,3,0)
        layout.addWidget(self.minutes,3,1)
        layout.addWidget(self.seconds,3,2)
        layout.addWidget(self.resetTimeButton,4,2)
        layout.addWidget(self.startButton,4,0)
        layout.addWidget(self.stopButton,4,1)
        
        
        self.connect(self.tempTimer, SIGNAL("timeout()"), self.showTime);
        self.connect(self.startButton, SIGNAL("clicked()"), self.start);
        self.connect(self.stopButton, SIGNAL("clicked()"), self.stop);
        self.connect(self.resetTimeButton, SIGNAL("clicked()"), self.resetTime)

        self.resetTime()
        self.tempTimer.stop()
    
    def resetTime(self):
        hours = int(self.hours.value())
        minutes = int(self.minutes.value())
        seconds = int(self.seconds.value())
        self.time.setHMS(hours,minutes,seconds,0)
        self.updateTime()
    
    def updateTime(self):
        timeString = self.time.toString("hh:mm:ss")
        self.currentTime.setText(timeString)
    
    def showTime(self):
        
        self.updateTime()
        h = self.time.hour()
        m = self.time.minute()
        s = self.time.second()
        
        if not(h == 0 and m == 0 and s == 0):
            if self.clockStart.isSet():
                self.time = self.time.addSecs(-1)
            else:
                self.emit(SIGNAL("waitingForTemp"))
        else:
            self.emit(SIGNAL("timesup"))
            self.stop()
            self.resetTime()
            
    def heaterStart(self):
        self.emit(SIGNAL("heaterStart"))
    
    def start(self):
        self.emit(SIGNAL("timerStart"))
        self.tempTimer.start()

    def stop(self):
        self.emit(SIGNAL("timerStop"))
        self.tempTimer.stop()
        self.clockStart.clear()
    
    def startClock(self):
        self.clockStart.set()
        
    def setStatus(self, s):
        self.status.setText(s)
    
class TempController(QGroupBox):
    def __init__(self, parent=None, *args, **kwargs):
        QGroupBox.__init__(self, parent)
        
        layout = QGridLayout()
        self.setTitle("Temperature Controller")
        self.setLayout(layout)
        
        #Current Temp
        currentTempGroup = QGroupBox("Reactor Temperature")
        currentTempLayout = QGridLayout()
        self.currentTempLabel = QLabel("NA")
        self.currentTempLabel.setAlignment(Qt.AlignHCenter)
        self.currentTemp = 0
        currentTempGroup.setLayout(currentTempLayout)
        currentTempLayout.addWidget(self.currentTempLabel,0,0,1,3)
        
        #Time Selector
        self.setTime = TimeSelector(self)
        #Heater on / off switch
        self.heaterOnOffGroup = OnOffSwitch("Heater")
        self.coolingOnOffGroup = OnOffSwitch("Cooling")
        
        #Set Point selector
        setPointGroup = QGroupBox("Set Point")
        setPointLayout= QHBoxLayout()
        setPointGroup.setLayout(setPointLayout)
        self.tempSpinbox = QDoubleSpinBox()
        self.tempSpinbox.setRange(0,300)
        self.tempSpinbox.setSingleStep(.5)
        self.tempSpinbox.setValue(20.0)
        self.tempSpinbox.setSuffix(u"\xB0C")
        setPointLayout.addWidget(self.tempSpinbox)
        
        
        layout.addWidget(currentTempGroup,0,0,1,3)
        layout.addWidget(self.heaterOnOffGroup,1,0)
        layout.addWidget(self.coolingOnOffGroup,1,1)
        layout.addWidget(setPointGroup,1,2)
        layout.addWidget(self.setTime,2,0,1,3)
        
        self.connect(self.heaterOnOffGroup, SIGNAL("turnOn"), self.turnHeaterOn)
        self.connect(self.heaterOnOffGroup, SIGNAL("turnOff"), self.turnHeaterOff)
        
        self.connect(self.coolingOnOffGroup, SIGNAL("turnOn"), self.turnCoolingOn)
        self.connect(self.coolingOnOffGroup, SIGNAL("turnOff"), self.turnCoolingOff)
        
        self.connect(self.setTime, SIGNAL("timesup"), self.turnHeatOffCoolOn)
        self.connect(self.setTime,SIGNAL("timerStart"), self.timerTurnHeaterOn)
        self.connect(self.setTime,SIGNAL("timerStop"), self.unlock)
        self.connect(self.tempSpinbox,SIGNAL("valueChanged(double)"), self.changeSetpoint)
        self.connect(self.setTime,SIGNAL("waitingForTemp"), self.checkTemp)
    
    def checkTemp(self):
        self.setTime.setStatus("Waiting for temperature to rise...")
        if self.getSetpoint() < self.currentTemp:
            self.setTime.setStatus("Timer running...")
            self.setTime.clockStart.set()
    
    def timerTurnHeaterOn(self):
        self.turnHeaterOn()
        self.turnCoolingOff()
        self.lock()
    
    def turnHeatOffCoolOn(self):
        self.heaterOnOffGroup.setOff()
        self.coolingOnOffGroup.setOn()
        self.unlock()
        #self.emit(SIGNAL("turnHeatOffCoolOn"))
        
    def turnHeaterOn(self):
        self.heaterOnOffGroup.setOn()
        self.emit(SIGNAL("turnOnHeat"))
    
    def turnHeaterOff(self):
        self.emit(SIGNAL("turnOffHeat"))
    
    def turnCoolingOn(self):
        self.coolingOnOffGroup.setOn()
        self.emit(SIGNAL("turnOnCool"))
    
    def turnCoolingOff(self):
        self.coolingOnOffGroup.setOff()
        self.emit(SIGNAL("turnOffCool"))
    
    def lock(self):
        self.coolingOnOffGroup.setDisabled(True)
        self.heaterOnOffGroup.setDisabled(True)
    
    def unlock(self):
        self.setTime.setStatus("Stopped")
        self.coolingOnOffGroup.setDisabled(False)
        self.heaterOnOffGroup.setDisabled(False)
    
    def changeSetpoint(self):
        self.emit(SIGNAL("setpointChanged"))

    def getSetpoint(self):
        temp = float(self.tempSpinbox.value())
        return temp

    def setCurrentTemp(self, temp):
        self.currentTempLabel.setText("%3.0f\xB0C" % temp)
        self.currentTemp=temp
    
    def startTimer(self):
        self.setTime.start()
        
class PRMView(DeviceView):
    deviceType = "PRM"
    def __init__(self, prmModel=None, parent=None, *args, **kwargs):
        DeviceView.__init__(self, parent=parent, deviceModel=prmModel)            
        
        #Waste Controller
        self.wasteGroup = WasteController()
        
        # Temperature Control Timer
        self.tempTimer = TempController()
        
        #Stir Controller
        self.stirGroup = StirController()
        
        #Transfer Controller
        self.transferGroup = TransferController()
        
        #AUX Controller
        self.auxGroup = AUXController()
        
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
        layout.addWidget(motionGroup,0,0,1,4)
        layout.addWidget(self.transferGroup,1,0,1,1)
        layout.addWidget(self.auxGroup,1,1,1,1)
        layout.addWidget(self.wasteGroup,1,2,1,1)
        layout.addWidget(self.stirGroup,1,3,1,1)
        layout.addWidget(self.tempTimer,2,0,1,4)
        
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
        
        
        self.setLayout(layout)
        
        #Position Signal and Slots
        self.connect(self.position1Button, SIGNAL("clicked()"), self.runMoveXPos1)
        self.connect(self.position2Button, SIGNAL("clicked()"), self.runMoveXPos2)
        self.connect(self.position3Button, SIGNAL("clicked()"), self.runMoveXPos3)
        self.connect(self.openButton, SIGNAL("clicked()"), self.runMoveZDown)
        self.connect(self.sealButton, SIGNAL("clicked()"), self.runMoveZUp)
        
        #Transfer Signals and Slots
        self.connect(self.transferGroup, SIGNAL("turnOn"), self.runTransferOn)
        self.connect(self.transferGroup, SIGNAL("turnOff"), self.runTransferOff)
        
        #Aux Signal and Slots
        self.connect(self.auxGroup, SIGNAL("turnOn"), self.runAuxOn)
        self.connect(self.auxGroup, SIGNAL("turnOff"), self.runAuxOff)
        
        #Waste Signal and Slots
        self.connect(self.wasteGroup, SIGNAL("turnOn"), self.runWasteOn)
        self.connect(self.wasteGroup, SIGNAL("turnOff"), self.runWasteOff)
        
        #Stir Signal and Slots
        self.connect(self.stirGroup, SIGNAL("stirSpeedChanged"), self.runStir)
        
        #Temperature Controller Signal and Slots
        self.connect(self.tempTimer, SIGNAL("turnHeatOffCoolOn"), self.turnOffHeaterAndCoolOn)
        self.connect(self.tempTimer, SIGNAL("turnOnHeat"), self.runHeatOn)
        self.connect(self.tempTimer, SIGNAL("turnOffHeat"), self.runHeatOff)
        self.connect(self.tempTimer, SIGNAL("turnOnCool"), self.runCoolOn)
        self.connect(self.tempTimer, SIGNAL("turnOffCool"), self.runCoolOff)
        self.connect(self.tempTimer, SIGNAL("setpointChanged"), self.setTemp)
        
    def turnOffHeaterAndCoolOn(self):
        self.runHeatOff()
        self.runCoolOn()
    def runWasteOn(self):
        self.model.goWasteOn()
    def runWasteOff(self):
        self.model.goWasteOff()
    def runHeatOn(self):
        self.model.goHeaterOn()
    
    def runHeatOff(self):
        self.model.goHeaterOff()
    
    def setTemp(self):
        temp = self.tempTimer.getSetpoint()
        self.model.goSetpoint(temp)
        
    def runStir(self):
        self.model.goMix(self.stirGroup.getValue())
        
    def runCoolOn(self):
        self.model.goCoolOn()
    def runCoolOff(self):
        self.model.goCoolOff()

    def runTransferOn(self):
        self.model.goTransferOn()
    
    def runTransferOff(self):
        self.model.goTransferOff()
    def runAuxOn(self):
        self.model.goAuxOn()
    def runAuxOff(self):
        self.model.goAuxOff()
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
        
    def _disableCool(self):
        self.coolOffButton.setDisabled(True)
        self.coolOnButton.setDisabled(True)
    
    def _enableCool(self):
        self.coolOffButton.setDisabled(False)
        self.coolOnButton.setDisabled(False)
        
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

        self.tempTimer.setCurrentTemp(self.model.reactorTemperature)
        

def main(argv):
    pass
            
if __name__ == '__main__':
    main(sys.argv)
    app = QApplication([])
    form = PRMView()
    form.show()
    app.exec_()