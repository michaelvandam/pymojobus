# rdm.py 
# RDM MojoDevice code

# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!

from utils.mojodevice import MojoDevice
from utils.mojoerrors import *
from utils.mojorecorder import MojoRecorder
import logging

errlog = logging.getLogger("mojo.error")
log = logging.getLogger()

class Reservoir(object):
    def __init__(self, id):
        self.id = id+1
        self.reagentName = "Unknown"

class Reservoirs( list ):
    
    def __init__(self, num, *args, **kwargs):
        super(Reservoirs, self).__init__(*args,**kwargs)
        for i in range(num):
            self.append( Reservoir(i) )
           
class RDM(MojoDevice):
    deviceType="RDM"
    
    LOAD = "Loading..."
    DELIVER = "Delivering "
    CLEAN = "Cleaning "
    STANDBY = "Standby"
    PURGE = "Purging"
    GO = "GO"
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    ERR = "Error"
    ALL = "ALL"
    
    def __init__(self, *args, **kwargs):
        super(RDM,self).__init__(*args,**kwargs)
        reservoirNum = self.config['DeviceSettings'][self.deviceType]['reservoirNum']
        self.reservoirs = Reservoirs(int(reservoirNum))
        self.state = self.STANDBY
        self.cleanState = self.STANDBY
        self.selectedReservoir = None
        self.selectedCleanReservoir = None
        self.wasteState= self.OPEN
        self.addResponseCallback("Load", self.loadRespond)
        self.addResponseCallback("Standby", self.standbyRespond)
        self.addResponseCallback("Deliver", self.deliverRespond)
        self.addResponseCallback("Waste", self.wasteRespond)
        self.addResponseCallback("Clean", self.cleanRespond)
        
    def goPurge(self):
        self.goCommand("Deliver", "ALL")
        
    def goLoad(self, reagentNames=None):
        self.goCommand("Load", self.GO)
        
    def loadRespond(self, param):
        
        if param == "TRUE" or param == "DONE" :
            self.state = self.LOAD
            self.cleanState = self.LOAD
            log.debug("%s Going to Load state" % str(self))
        else:
            s = "Device (%s) did not go to load" % str(self)
            errlog.error(s)
            raise MojoCallbackError(s)
        
    def goStandby(self):
        self.goCommand("Standby", self.GO)
        
        
    def standbyRespond(self,param):
        
        if param == "TRUE" or param == "DONE" :
            self.state = self.STANDBY
            log.debug("%s Going to Standby state" % str(self))
        else:
            s = "Device (%s) did not go to standby" % str(self)
            errlog.error(s)
            raise MojoCallbackError(s)
            
    def goDeliver(self, index):
        self.goCommand("Deliver", str(index))
        
    def goClean(self, index):
        self.goCommand("Clean", str(index))
    
    def deliverRespond(self, param):
        if param == self.ALL:
            self.state = self.PURGE
        else:
            try:
                index = int(param)-1
                self.state=self.DELIVER #+ str(index + 1)
                self.selectedReservoir = self.reservoirs[index]
                log.debug("%s Going to deliver state, selected reagent %d" % 
                                (str(self),self.selectedReservoir.id))
                
            except (ValueError, IndexError):
                s = "%s Not delivering, invalid reservoir index" % str(self)
                errlog.error(s)
                raise MojoCallbackError(s)
            
    
    def goWasteOpen(self):
        self.goCommand("Waste", self.OPEN)

    def goWasteClose(self):
        self.goCommand("Waste", self.CLOSE)


    def wasteRespond(self, param):
        if param in (self.CLOSE, self.OPEN):
            self.wasteState = param
        else:
            self.wasteState = self.ERR
       
    def cleanRespond(self, param):
        try:
            index = int(param)-1
            self.cleanState=self.CLEAN #+ str(index + 1)
            
            self.selectedCleanReservoir = self.reservoirs[index]
            log.debug("%s Going to clean state, selected reagent %d" % 
                            (str(self),self.selectedCleanReservoir.id))
            
        except (ValueError, IndexError):
            s = "%s Not cleaning, invalid reservoir index" % str(self)
            errlog.error(s)
            raise MojoCallbackError(s)
       
    def setReagentName(self, reservoirIndex, name):
        self.reservoirs[reservoirIndex].reagentName=name
        
        
       
    
    