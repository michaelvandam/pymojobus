# cpm.py 
# CPM MojoDevice code

# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!


from utils.mojodevice import MojoDevice
#from utils.reagents import Reagent
from utils.mojoerrors import *
import logging

errlog = logging.getLogger("mojo.error")
log = logging.getLogger()

class CPM(MojoDevice):
    deviceType="CPM"
    
    LOADREAGENTS = "Loading Reagents..."
    LOADSAMPLE = "Loading Sample..."
    TRAP = "Trapping..."
    WASH = "Washing..."
    ELUTE = "Eluting..."
    STANDBY = "Standby"
    
    
    
    def __init__(self, *args, **kwargs):
        super(CPM,self).__init__(*args,**kwargs)
        self.state = self.STANDBY
        
        log.info("Adding callbacks for CPM")
        self.addResponseCallback("Standby", self.standbyRespond)
        self.addResponseCallback("LoadReagents", self.loadReagentsRespond)
        self.addResponseCallback("LoadSample", self.loadSampleRespond)
        self.addResponseCallback("Trap", self.trapRespond)
        self.addResponseCallback("Wash", self.washRespond)
        self.addResponseCallback("Elute", self.eluteRespond)
        
        
        
    def goLoadReagents(self):
        
        cmd = self._findCommand("LoadReagents")
        self.sendMsg.addCommand(cmd)
        self.send()
        self.sendMsg.clearCommands()
        
        
    def loadReagentsRespond(self,param):
        
        if param == "DONE":
            self.state = self.LOADREAGENTS
            log.debug("%s Going to load reagents state" % str(self))
        else:
            s = "Device (%s) did not go to load reagents" % str(self)
            errlog.error(s)
            raise MojoCallbackError(s)
            
        
    def goLoadSample(self):
        
        cmd = self._findCommand("LoadSample")
        self.sendMsg.addCommand(cmd)
        self.send()
        self.sendMsg.clearCommands()
        
        
    def loadSampleRespond(self,param):
        
        if param == "DONE":
            self.state = self.LOADSAMPLE
            log.debug("%s Going to load sample state" % str(self))
        else:
            s = "Device (%s) did not go to load sample" % str(self)
            errlog.error(s)
            raise MojoCallbackError(s)

    def goTrap(self):
        
        cmd = self._findCommand("Trap")
        self.sendMsg.addCommand(cmd)
        self.send()
        self.sendMsg.clearCommands()
        
        
    def trapRespond(self,param):
        
        if param == "DONE":
            self.state = self.TRAP
            log.debug("%s Going to load trap state" % str(self))
        else:
            s = "Device (%s) did not go to trap sample" % str(self)
            errlog.error(s)
            raise MojoCallbackError(s)
    
    def goWash(self):
        
        cmd = self._findCommand("Wash")
        self.sendMsg.addCommand(cmd)
        self.send()
        self.sendMsg.clearCommands()
        
        
    def washRespond(self,param):
        
        if param == "DONE":
            self.state = self.WASH
            log.debug("%s Going to wash state" % str(self))
        else:
            s = "Device (%s) did not go to wash" % str(self)
            errlog.error(s)
            raise MojoCallbackError(s)
        
    def goElute(self):
        
        cmd = self._findCommand("Elute")
        self.sendMsg.addCommand(cmd)
        self.send()
        self.sendMsg.clearCommands()
        
        
    def eluteRespond(self,param):
        
        if param == "DONE":
            self.state = self.ELUTE
            log.debug("%s Going to elute" % str(self))
        else:
            s = "Device (%s) did not go to elute" % str(self)
            errlog.error(s)
            raise MojoCallbackError(s)
    
    def goStandby(self, reagentNames=None):
        
        cmd = self._findCommand("Standby")
        self.sendMsg.addCommand(cmd)
        self.send()
        self.sendMsg.clearCommands()
        
        
    def standbyRespond(self,param):
        
        if param == "DONE":
            self.state = self.STANDBY
            log.debug("%s Going to Standby state" % str(self))
        else:
            s = "Device (%s) did not go to standby" % str(self)
            errlog.error(s)
            raise MojoCallbackError(s)