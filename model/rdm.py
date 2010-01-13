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
    STANDBY = "Standby"
    GO = "GO"
    
    def __init__(self, *args, **kwargs):
        super(RDM,self).__init__(*args,**kwargs)
        reservoirNum = self.config['DeviceSettings'][self.deviceType]['reservoirNum']
        self.reservoirs = Reservoirs(int(reservoirNum))
        self.state = self.STANDBY
        self.selectedReservoir = None
        
        self.addResponseCallback("Load", self.loadRespond)
        self.addResponseCallback("Standby", self.standbyRespond)
        self.addResponseCallback("Deliver", self.deliverRespond)
        
    def goLoad(self, reagentNames=None):
        self.goCommand("Load", self.GO)
        
    def loadRespond(self, param):
        
        if param == "TRUE" or param == "DONE" :
            self.state = self.LOAD
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
        
    def deliverRespond(self, param):
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
        
        

       
    def setReagentName(self, reservoirIndex, name):
        self.reservoirs[reservoirIndex].reagentName=name
        
        
       
    
    