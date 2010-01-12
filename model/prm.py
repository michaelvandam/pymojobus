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


from utils.mojodevice import MojoUpdatingDevice
from utils.mojomessages import MojoReceivedMessage, MojoSendMessage, MojoAddress
from utils.mojoconfig import masterAddress
import logging

errlog = logging.getLogger("mojo.error")
log = logging.getLogger()


class PRM(MojoUpdatingDevice):
    deviceType="PRM"
    xpositions = (0,1,2,3)
    HOME ="HOME"
    BUSY="BUSY"
    XERR = "?XERR"
    UP = "UP"
    DOWN = "DOWN"
    ZERR = "?ZERR"
    ON = "ON"
    OFF = "OFF"
    ERR = "?ERR"
    
    def __init__(self, *args, **kwargs):
        MojoUpdatingDevice.__init__(self, *args, **kwargs)
        updateMsg = MojoSendMessage(MojoAddress(sender=masterAddress, receiver=self.address))
        updateMsg.addCommand(self._findCommand("MoveX"))
        updateMsg.addCommand(self._findCommand("MoveZ"))
        self.updateMsgs.append(updateMsg)
        self.startUpdating()
        self.xState = self.BUSY
        self.zState = None
        self.coolState = self.OFF
        self.transferState = self.OFF
        self.addResponseCallback("MoveX", self.moveXRespond)
        self.addResponseCallback("MoveZ", self.moveZRespond)
        self.addResponseCallback("Cool", self.coolRespond)
        self.addResponseCallback("Transfer", self.transferRespond)
        self.xposition = 0
    
    def goMoveXHome(self):
        self.goMoveX()
    
    def goMoveX(self, position=0):
        position = str(position)
        cmd = self._findCommand("MoveX")
        self.sendMsg.addCommand(cmd, position)
        self.send()
        self.sendMsg.clearCommands()
    
    def goMoveZDown(self):
        cmd = self._findCommand("MoveZ")
        self.sendMsg.addCommand(cmd, self.DOWN)
        self.send()
        self.sendMsg.clearCommands()
    
    def goMoveZUp(self):
        cmd = self._findCommand("MoveZ")
        self.sendMsg.addCommand(cmd, self.UP)
        self.send()
        self.sendMsg.clearCommands()
    
    def goTransferOn(self):
        cmd = self._findCommand("Transfer")
        self.sendMsg.addCommand(cmd, self.ON)
        self.send()
        self.sendMsg.clearCommands()
    
    
    def goTransferOff(self):
        cmd = self._findCommand("Transfer")
        self.sendMsg.addCommand(cmd, self.OFF)
        self.send()
        self.sendMsg.clearCommands()
    
    def goCoolOn(self):
        cmd = self._findCommand("Cool")
        self.sendMsg.addCommand(cmd, self.ON)
        self.send()
        self.sendMsg.clearCommands()
    
    def goCoolOff(self):
        cmd = self._findCommand("Cool")
        self.sendMsg.addCommand(cmd, self.OFF)
        self.send()
        self.sendMsg.clearCommands()
    
    def moveXRespond(self,param):
        
        if param == 0:
            log.debug("%s Position X Home" % str(self))
            self.xState = int(param)
        elif param == self.BUSY:
            log.debug("%s Moving X Busy... " % str(self))
            self.xState = self.BUSY
        elif param == self.XERR:
            errlog.error("%s Moving X Error" % str(self))
            self.xState = self.XERR
        else:
            try:
                log.debug("%s Position X is %s" % (str(self), param))
                self.xState = int(param)
            except ValueError:
                errlog.error("%s Moving X Error: Bad Return Value" % str(self))
                self.xState=self.XERR
            
    def moveZRespond(self,param):
        if param == self.UP:
            log.debug("%s Position Z %s" % (str(self), self.UP))
            self.zState = self.UP
        elif param == self.DOWN:
            log.debug("%s Position Z %s" % (str(self), self.DOWN))
            self.zState = self.DOWN
        elif param == self.BUSY:
            log.debug("%s Moving Z %s" % (str(self), self.BUSY))
            self.zState = self.BUSY
        else:
            errlog.error("%s Moving Z Error" % str(self))
            self.zState = self.ZERR
    
    def transferRespond(self, param):
        if param == self.ON:
            self.transferState=self.ON
            log.debug("%s Transfer %s" % (str(self), self.transferState))
        elif param == self.OFF:
            self.transferState=self.OFF
            log.debug("%s Transfer %s" % (str(self), self.transferState))
        else:
            self.transferState=self.ERR
        
    
    def coolRespond(self, param):
        if param == self.ON:
            self.coolState=self.ON
            log.debug("%s Cool %s" % (str(self), self.coolState))
        elif param == self.OFF:
            self.coolState=self.OFF
            log.debug("%s Cool %s" % (str(self), self.coolState))
        else:
            self.coolState=self.ERR