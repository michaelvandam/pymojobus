# mojodevice.py 
# Base class for all mojo devices
# Contains code for sending and receiving communication from the bus
# Deals with callbacks and searching config files for proper commands
 
# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!
import time
import copy
import logging
import sys
import threading
import Queue
from threading import Thread
from mojoerrors import *
from mojoconfig import config, masterAddress
from mojomessages import MojoReceivedMessage, MojoSendMessage, MojoAddress 
from deviceconfig import getDeviceConfig
from mojothread import MojoThread

log = logging.getLogger()
errlog = logging.getLogger("mojo.error")

class MojoDevice(object):
    deviceType="Default"
    def __init__(self, address, connection, version=0):
        
        
        self.config = getDeviceConfig(self.deviceType)
        self.connection = connection
        self.address = address
        log.info("Initiailizing Device: %s  @ %s" % (self.deviceType, self.address))
        self.version=version
        self.sendMsg = MojoSendMessage(MojoAddress(sender=masterAddress, receiver=self.address))
        self.responseCallbacks = dict()
        self.resp = None
        self.lastMessage = copy.copy(self.sendMsg)
        self.addResponseCallback("Blink", self.blinkRespond)
        
    
    def addResponseCallback(self, friendlyCommandName, fxn):
        self.responseCallbacks[self._findCommand(friendlyCommandName)] = fxn
        
    
    def _findCommand(self, prettyName):
        try:
            cmd = self.config['DeviceSettings']['Commands'][prettyName]['cmd']
        except (NameError, KeyError), e:
            raise MojoBadCommand("Could not retrieve command from configuration")
        return cmd
        
    def send(self):
        self.lastMessage = copy.copy(self.sendMsg)
        self.connection.mojoSend(self.lastMessage)
        self.sendMsg.clearCommands()
        # To be removed when I add message checking
        #print self.connection.mojoRead()

    def sendUpdate(self, m):
        self.lastMessage = copy.copy(m)
        self.connection.mojoSend(self.lastMessage)

    def who(self):
        cmd = self._findCommand("Who")
        self.sendMsg.addCommand(cmd)
        self.send()
        
    def blink(self):
        cmd = self._findCommand("Blink")
        self.sendMsg.addCommand(cmd)
        self.send()
        
    def blinkRespond(self, param=None):
        print ";)"
        
    def __repr__(self):
        return "%s(address='%s')" % (self.__class__.__name__,self.address)
        
    def __str__(self):
        return self.__repr__()
        
    def processResponse(self, msg):
        log.debug("%s processing response '%s'" % (str(self),msg))
        self.resp = msg
        
        if not self.resp==self.lastMessage:
            errlog.info("Response does not match last message")
        for cmd in msg.cmds:
            f = self.responseCallbacks.get(cmd.cmd[1:],(lambda x: None))
            f(cmd.param)
    
    def getDeviceName(self):
        if hasattr(self, "_prettyName"):
            return self._prettyName
        else:
            return "%s @ %s" % (self.deviceType, self.address) 
    
    def setDeviceName(self, prettyName):
        self._prettyName = prettyName
        
        
    name = property(getDeviceName, setDeviceName)



class MojoDeviceUpdateThread( MojoThread ):
    
    def __init__(self, device):
        MojoThread.__init__(self)
        self.device=device
        self.refreshRate=self.device.refreshRate
        self.setName("UpdateThread %s" % self.device.name)
        log.debug("Initializing Update Thread for %s" % self.device.name)
        
    
    def run(self):
        log.debug("Starting UpdateThread for %s" % self.device.name)
        while(not self.stop_event.isSet()):
            time.sleep(self.refreshRate)
            for msg in self.updateMessages:
                self.device.connection.mojoSend(msg)
        
        self.stop_event.clear()
        msglog.info("Update %s Thread Shutdown" % self.device.name)
    
    def start(self, updateMessages):
        self.updateMessages = updateMessages
        MojoThread.start(self)


class MojoUpdatingDevice(MojoDevice):
    def __init__(self, *args, **kwargs):
        MojoDevice.__init__(self, *args, **kwargs)
        self.refreshRate = self.config['DeviceSettings']['refreshRate']
        self.updateThread = MojoDeviceUpdateThread(self)
        self.updateMsgs = []
        log.debug("This is an updating device! %s" % self.name)
        
        
    def startUpdating(self):
        self.updateThread.start(self.updateMsgs)
    
    def __del__(self):
        self.updateThread.stop()
        self.updateThread.join()
        
        
    