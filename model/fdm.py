# prm.py 
# PRM MojoDevice code

# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!

import time
from threading import Event
from utils.mojodevice import MojoUpdatingDevice
from utils.mojomessages import MojoReceivedMessage, MojoSendMessage, MojoAddress
from utils.mojoconfig import masterAddress
from utils.mojorecorder import MojoRecorder
from utils.mojothread import MojoThread
import logging

errlog = logging.getLogger("mojo.error")
log = logging.getLogger()


class FDMOperationThread(MojoThread):
    def __init__(self, device, *args, **kwargs):
        MojoThread.__init__(self, *args, **kwargs)
        self.device = device

class FDMCleanThread(FDMOperationThread):
    def __init__(self, device, *args, **kwargs):
        FDMOperationThread.__init__(self, device,*args, **kwargs)
        self.location = self.device.CLEANLOC
        self.runClean = Event()
        self.runClean.clear()
        self.delayAfterClean = 0
        self.pressure = 5000
        self.dryPressure = 10000
        self.repeat = 1
        self.volume=0
        self.speed=15
        self.cleanSelect = self.device.H2OPOS
        self.delay = 3
        self.cleanDelay = 3
        self.dryDelay = 3
        self.repeat = 3
        
    def run(self):
        while(not self.stop_event.isSet()):
            if self.runClean.isSet():
                if (not self.location is None):
                    self.runClean.clear()
                    self.device.sleepWhileMoving()
                    self.device.goWaitMoveZUp()
                    log.info("Begin Clean Routine")
                    log.info("Clean @ %s" % self.location)
                    self.device.goWaitMove2Position(self.location)
                    log.info("Lower Z @ %s" % self.location)
                    self.device.goWaitMoveZDown()
                    self.device.goWaitSyringeCommand("S%dIA0R" % (self.speed))
                    for i in range(self.repeat):
                        log.info("****Cleaning On %d******" % i)
                        #print "*****Cleaning ON******"
                        self.device.goClean(self.cleanSelect, self.pressure)
                        log.info("Delay for %f sec" % self.cleanDelay)
                        time.sleep(self.cleanDelay)
                        self.device.goCleanOff()
                        for j in range(3000,self.dryPressure,500):
                            log.info("Ramp pressure %d" % j)
                            time.sleep(5)
                            self.device.goBlow(j)
                        log.info("Delay for %f sec" % self.dryDelay)
                        time.sleep(self.dryDelay)
                        self.device.goBlow(0)
                    self.device.goCleanOff()
                    log.info("Shut off needle" )
                    log.info("Raise Z")
                    self.device.goWaitMoveZUp()
                    log.info("Dispense Complete")
            else:
                self.device.sleep()
    
    def setRepeat(self, repeat):
        self.repeat=repeat
        
    def setVolume(self, volume):
        self.volume = volume
        
    def setLocation(self,location):
        self.location = location
    
    def setDelay(self,delay):
        self.cleanDelay = delay
    
    def setDryDelay(self,delay):
        self.dryDelay = delay
        
    def setPressure(self,pressure):
        self.pressure = pressure
        
    def setDryPressure(self,pressure):
        self.dryPressure = pressure
        
    
    def go(self):
        self.runClean.set()

    def setSpeed(self, speed):
        self.speed = speed

    def setCleanFluid(self, POS):
        self.cleanSelect=POS
    
    def isActive(self):
        if self.runClean.set():
            return True

        
class FDMDispenseThread(FDMOperationThread):
    def __init__(self, device, *args, **kwargs):
        FDMOperationThread.__init__(self, device,*args, **kwargs)
        self.fromLocation = None
        self.toLocation = None
        self.runDispense = Event()
        self.runDispense.clear()
        self.delayAfterAspirate = 0
        self.delayAfterDispense = 0
        self.pressure = 0
        self.repeat = 1
        self.volume=0
        self.speed=15

    def run(self):
        while(not self.stop_event.isSet()):
            if self.runDispense.isSet():
                if (not self.toLocation is None) \
                    and (not self.fromLocation is None):
                    self.runDispense.clear()
                    self.device.sleepWhileMoving()
                    self.device.goWaitMoveZUp()
                    log.info("Begin Dispense Routine")
                    log.info("Aspirate From %s" % self.fromLocation)
                    self.device.goWaitMove2Position(self.fromLocation)
                    log.info("Lower Z @ %s" % self.fromLocation)
                    self.device.goWaitMoveZDown()
                    self.device.goVentOn()
                    log.info("Aspirate")
                    self.device.goWaitSyringeCommand("S%dOA0S%dIA%dR" %
                                    (self.speed,self.speed, self.volume))
                    time.sleep(self.delayAfterAspirate)
                    log.info("Raise Z")
                    self.device.goWaitMoveZUp()
                    log.info("Dispense to %s" % self.toLocation)
                    self.device.goWaitMove2Position(self.toLocation)
                    log.info("Lower Z")
                    self.device.goWaitMoveZDown()
                    self.device.goVentOff()
                    log.info("Dispense with syringe")
                    self.device.goWaitSyringeCommand("S5OA3000S%dIA0G%dR" % (self.speed, self.repeat))
                    self.device.goBlow(self.pressure)
                    log.info("Dispense with MFC" )
                    log.info("Delay for %f sec" % self.delayAfterDispense)
                    time.sleep(self.delayAfterDispense)
                    self.device.goBlow(0)
                    self.device.sleepWhileSyringe()
                    log.info("Shut off needle" )
                    log.info("Raise Z")
                    self.device.goWaitMoveZUp()
                    log.info("Dispense Complete")
            else:
                self.device.sleep()
                
    def setVolume(self, volume):
        self.volume = volume
        
    def setToLocation(self,toLocation):
        self.toLocation = toLocation
    
    def setFromLocation(self,fromLocation):
        self.fromLocation = fromLocation
    
    def setDelayForAspirate(self,delay):
        self.delayAfterAspirate = delay
        
    def setDelayForDispense(self,delay):
        self.delayAfterDispense = delay
    
    def setSyringeDispenseRepeat(self,repeat):
        self.repeat = repeat
    
    def setPressure(self,pressure):
        self.pressure = pressure
        
    def go(self):
        self.runDispense.set()

    def setSpeed(self, speed):
        self.speed = speed
        
    def isActive(self):
        if self.runDispense.set():
            return True

class FDM(MojoUpdatingDevice):
    deviceType="FDM"
    rotaryValvePositions = range(1,10)
    HOME ="HOME"
    BUSY="BUSY"
    XERR = "?XERR"
    ZERR = "?ZERR"
    YERR = "?YERR"
    SYRERR = "?SYRERR"
    UP = "UP"
    DOWN = "DOWN"
    ON = "ON"
    FREE = "FREE"
    OFF = "OFF"
    ERR = "?ERR"
    GO = "GO"
    READY = "READY"
    MOVING = "MOVING"
    CLEANLOC = 'Manifold 1'
    REG0PIN = 1
    AIRVALVE = 1
    CLEANMAXPRESS = 10000
    H2OPOS = 1
    
    def __init__(self, *args, **kwargs):
        MojoUpdatingDevice.__init__(self, *args, **kwargs)        
        updateMsg = MojoSendMessage(MojoAddress(sender=masterAddress, receiver=self.address))
        updateMsg.addCommand(self.findCommand("MoveX"))
        updateMsg.addCommand(self.findCommand("MoveY"))
        updateMsg.addCommand(self.findCommand("MoveZ"))
        updateMsg.addCommand(self.findCommand("Syringe"))
        self.updateMsgs.append(updateMsg)
        
        self.positions = self.config['DeviceSettings']['FDM']['Positions']
        
        self.startUpdating()

        self.addResponseCallback("MoveX", self.moveXRespond)
        self.addResponseCallback("MoveY", self.moveYRespond)
        self.addResponseCallback("MoveZ", self.moveZRespond)
        self.addResponseCallback("Syringe", self.syringeRespond)
        
        
        self.xState = self.BUSY
        self.yState = self.BUSY
        self.zState = self.DOWN
        self.syringeState = self.BUSY
        self.rotaryValvePosition = self.rotaryValvePositions[0]
        self.dispensingThread = FDMDispenseThread(self)
        self.cleanThread = FDMCleanThread(self)
        self.dispensingThread.start()
        self.cleanThread.start()
        
    def goMoveXHome(self):
        self.goMoveX()
    
    def goMoveX(self, position=0):
        position = str(position)
        self.goCommand("MoveX", position)
    
    def goMoveY(self, position=0):
        position = str(position)
        self.goCommand("MoveY", position)
    
    def goPosXY(self,coords):
        self.goMoveX(coords[0])
        self.goMoveY(coords[1])
    
    def goMoveXY(self, coords=None):
        xcmd = self.findCommand("MoveX")
        ycmd = self.findCommand("MoveY")
        if not coords is None:
            xposition = str(coords[0])
            yposition = str(coords[1])
            self.sendMsg.addCommand(xcmd, xposition)
            self.sendMsg.addCommand(ycmd, yposition)
        else:
            self.sendMsg.addCommand(xcmd)
            self.sendMsg.addCommand(ycmd)
        self.send()
        self.sendMsg.clearCommands()
        self.xState=self.BUSY;self.yState=self.BUSY
    
    def goMove2Position(self, position):
        xypos = self.positions[position]
        xp = xypos['xcoord']
        yp = xypos['ycoord']
        self.goMoveXY((xp,yp))
    
    def goMoveZDown(self):
        self.zState=self.BUSY
        self.goCommand("MoveZ", self.DOWN)
    
    def goMoveZUp(self):
        self.zState=self.BUSY
        self.goCommand("MoveZ", self.UP)
    
    def goMoveZFree(self):
        self.zState=self.BUSY
        self.goCommand("MoveZ", self.FREE)
    
    def goReset(self):
        self.goCommand("Reset",None)
    
    def goRotaryValve(self, selectedPosition):
        self.rotaryValvePosition = selectedPosition
        selectedPosition = str(selectedPosition)
        self.goCommand("RotaryValve", selectedPosition)
        
    def goAirValveOn(self, airValveId):
        for i in range(1,9):
            self.goAirValveOff(i)
        airValveId = str(airValveId)
        prettyName = "AirValve" + airValveId
        self.goCommand(prettyName,self.ON)
    
    def goAirValveOff(self, airValveId):
        airValveId = str(airValveId)
        prettyName = "AirValve" + airValveId
        self.goCommand(prettyName,self.OFF)
        
    def goSyringeCommand(self, s):
        self.syringeState = self.BUSY
        self.goCommand("Syringe", s)
        
    def goSyringe2RotaryValve(self):
        self.goSyringeCommand("BR")
    
    def goSyringe2Needle(self):
        self.goSyringeCommand("IR")
        
    def goSyringe2Vent(self):
        self.goSyringeCommand("OR")
    
    def goVentOn(self):
        self.goCommand("Vent", self.ON)
    
    def goVentOff(self):
        self.goCommand("Vent", self.OFF)
    
    def goDac0(self,pin,value):
        self.goCommand("DAC0","%d,%d" % (pin,value))
    
    def goClean(self,pos,pressure):
        if (pressure<self.CLEANMAXPRESS+1):
            self.goVentOff()
            self.goDac0(self.REG0PIN,pressure)
            self.goCleanValve(pos)
            self.goSyringe2RotaryValve();
        else:
            log.info("PRESSURE %d TO HIGH" % pressure)
    
    def goCleanOff(self):
        self.goDac0(self.REG0PIN,0)
        for i in range(1,9):
            self.goAirValveOff(i)
    
    def goCleanValve(self,pos):
        self.goAirValveOn(pos)
        self.goRotaryValve(pos)
        
    def moveXRespond(self,param):
        if param == 0:
            log.info("%s Position X Home" % str(self))
            self.xState = int(param)
        elif param == self.BUSY or param == self.MOVING:
            log.info("%s Moving X Busy... " % str(self))
            self.xState = self.BUSY
        elif param == self.XERR:
            errlog.error("%s Moving X Error" % str(self))
            self.xState = self.XERR
        else:
            try:
                log.info("%s Position X is %s" % (str(self), param))
                self.xState = int(param)
            except ValueError:
                errlog.error("%s Moving X Error: Bad Return Value" % str(self))
                self.xState=self.XERR

    def moveYRespond(self,param):
        
        if param == 0:
            log.info("%s Position Y Home" % str(self))
            self.yState = int(param)
        elif param == self.BUSY or param == self.MOVING:
            log.info("%s Moving Y Busy... " % str(self))
            self.yState = self.BUSY
        elif param == self.XERR:
            errlog.error("%s Moving Y Error" % str(self))
            self.xState = self.YERR
        else:
            try:
                log.info("%s Position Y is %s" % (str(self), param))
                self.yState = int(param)
            except ValueError:
                errlog.error("%s Moving Y Error: Bad Return Value" % str(self))
                self.yState=self.YERR
            
    def moveZRespond(self,param):
        if param == self.UP:
            log.info("%s Position Z %s" % (str(self), self.UP))
            self.zState = self.UP
        elif param == self.DOWN:
            log.info("%s Position Z %s" % (str(self), self.DOWN))
            self.zState = self.DOWN
        elif param == self.BUSY:
            log.info("%s Moving Z %s" % (str(self), self.BUSY))
            self.zState = self.BUSY
        else:
            errlog.error("%s Moving Z Error" % str(self))
            self.zState = self.ZERR
    
    def syringeRespond(self,param):
        if param == self.BUSY:
            log.info("%s Syringe %s" % (str(self), self.BUSY))
            self.syringeState = self.BUSY
        elif param == self.READY:
            log.info("%s Syringe %s" % (str(self), self.READY))
            self.syringeState = self.READY
        elif param == self.SYRERR:
            log.info("%s Syringe Error" % str(self))
            self.syringeState = self.SYRERR
        else:
            log.info("%s Sent syringe command" % str(self))
            self.syringeState = self.BUSY
            
    def isUp(self):
        if self.zState == self.UP:
            return True
        return False
    
    def isDown(self):
        if self.zState == self.DOWN:
            return True
        return False
                    
    def isBusy(self):
        if self.xState == self.BUSY or self.yState == self.BUSY or self.zState==self.BUSY:
            return True
        return False
    
    def isSyringeBusy(self):
        if self.syringeState == self.READY:
            return False
        else:
            return True
    
    def sleep(self):
        time.sleep(self.refreshRate)
        
    def sleepWhileMoving(self):
        self.sleep()
        self.sleep()
        while self.isBusy():
            self.sleep()
            
    def sleepWhileSyringe(self):
        while self.isSyringeBusy():
            self.sleep()
            
    def goWaitMoveZDown(self):
        self.zState=self.BUSY
        while(self.zState!=self.DOWN):
            self.goMoveZDown()
            self.sleepWhileMoving()
            
    def goWaitMoveZUp(self):
        self.zState=self.BUSY
        while(self.zState!=self.UP):
            self.goMoveZUp()
            self.sleepWhileMoving()
            
    def goWaitMove2Position(self, position):
        self.xState=self.BUSY
        self.yState=self.BUSY
        while(self.xState==self.BUSY and self.yState==self.BUSY):
            self.goMove2Position(position)
            self.sleepWhileMoving()
    
    def goWaitSyringeCommand(self,command):
        self.syringeState=self.BUSY
        while(self.syringeState==self.BUSY):
            self.goSyringeCommand(command)
            self.sleepWhileSyringe()
            
    def goBlow(self,pressure):
        self.goDac0(1,pressure)
        self.goRotaryValve(8)
        self.goAirValveOn(8)
        self.goSyringe2RotaryValve()