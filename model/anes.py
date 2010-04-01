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
import time
from utils.mojodevice import MojoDevice
from utils.mojoerrors import *
from utils.mojorecorder import MojoRecorder
from utils.mojothread import MojoThread
import SocketServer
import logging

errlog = logging.getLogger("mojo.error")
log = logging.getLogger()

class BreathingTCPHandler(SocketServer.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def setDevice(self, device):
        self.device = device
        
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.rfile.readline().strip()
        log.debug("%s wrote: %s" % (self.client_address[0],self.data))
        
        if 'O?' in self.data:
            self.request.send("O=%s" %self.server.device.oxSetFlow)
        elif 'O=' in self.data:
            val = self.data.split("=")[1]
            try:
                val = int(val)
                if val >= 0 or val <=1000:
                    self.server.device.oxLevel = val
                    self.request.send("O=%d" % val)
                else:
                    self.request.send("BAD")
            except:
                self.request.send("BAD")
        elif 'A?' in self.data:
            self.request.send("A=%s" %self.server.device.anesSetFlow)
        elif 'A=' in self.data:
            val = self.data.split("=")[1]
            try:
                val = int(val)
                if val >= 0 or val <=1000:
                    self.server.device.anesLevel = val
                    self.request.send("A=%d" % val)
                else:
                    self.request.send("BAD")
            except:
                self.request.send("BAD")
        elif 'P?' in self.data:
            self.request.send("P=%s" %self.server.device.perAnes)
        elif 'P=' in self.data:
            val = self.data.split("=")[1]
            #try:
            val = int(val)
            if val >= 0 or val <=100:
                self.server.device.perAnes = val
                self.request.send("P=%d" % val)
            else:
                self.request.send("BAD")
            #except:
            #    self.request.send("BAD")
        else:
            self.request.send("BAD")
        

class BreathingServerThread( MojoThread ):
    
    def __init__(self, device):
        MojoThread.__init__(self)
        self.device=device
        self.setName("BreathingServerThread %s" % self.device.name)
        log.debug("Initializing Breathing Server Thread for %s" % self.device.name)
        HOST, PORT = "localhost", 9999
        self.server = SocketServer.TCPServer((HOST, PORT), BreathingTCPHandler)
        self.server.device = self.device
        
    def run(self):
        log.debug("Starting Breathing Server for %s" % self.device.name)
        while(not self.stop_event.isSet()):
            self.server.serve_forever()
            
        self.stop_event.clear()
        log.info("Update %s Thread Shutdown" % self.device.name)
    
    def start(self):
        MojoThread.start(self)
    
    def stop(self):
        self.server.shutdown()
        MojoThread.stop(self)
        

class AnesUpdateThread( MojoThread ):
    
    def __init__(self, device):
        MojoThread.__init__(self)
        self.device=device
        self.refreshRate=self.device.refreshRate
        self.setName("UpdateThread %s" % self.device.name)
        log.debug("Initializing Update Thread for %s" % self.device.name)
    
    def run(self):
        log.debug("Starting UpdateThread for %s" % self.device.name)
        while(not self.stop_event.isSet()):
            self.device.goQueryOx()
            time.sleep(self.refreshRate)
            self.device.goQueryAnes()
            time.sleep(self.refreshRate)
            self.device.goSetOx(self.device.oxLevel)
            time.sleep(self.refreshRate)
            self.device.goSetAnes(self.device.anesLevel)
            time.sleep(self.refreshRate)
            
        
        self.stop_event.clear()
        log.info("Update %s Thread Shutdown" % self.device.name)
    
    def start(self):
        MojoThread.start(self)



           
class ANES(MojoDevice):
    deviceType="ANES"
    
    ON = "ON"
    OFF = "OFF"
    GO = "GO"
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    ERR = "Error"
    MAX = 1000
    def __init__(self, *args, **kwargs):
        super(ANES,self).__init__(*args,**kwargs)
        self.purgeState = self.OFF
        self.valveState = self.ON
        self.oxLevel = 0
        self.anesLevel = 0
        self.oxActualFlow = "None"
        self.anesActualFlow = "None"
        self.oxSetFlow = "None"
        self.anesSetFlow = "None"
        MojoDevice.__init__(self, *args, **kwargs)
        self.refreshRate = self.config['DeviceSettings']['refreshRate']
        log.debug("This is an updating device! %s" % self.name)
        self.addResponseCallback("QueryAnesthesia", self.anesRespond)
        self.addResponseCallback("QueryOxygen", self.oxRespond)
        self.startUpdating()
        self.startServer()
    
    def calcMax(self):
        return self.oxLevel + self.anesLevel
        
    def setMax(self,val):
        self.anesLevel = val
        self.oxLevel = 0
        
    def calcPerAnes(self):
        if self.maxLevel == 0:
            return 0
        return float(self.anesLevel) / self.maxLevel * 100.0
    
    
    maxLevel = property(calcMax,setMax)
    
    
    def setPerAnes(self, val):
        if self.maxLevel > 1000:
            self.maxLevel = 1000
            
        if val <= 100 or val >=0:
            anes = int(val/100.0 * self.maxLevel)
            ox = self.maxLevel - anes
            self.oxLevel = ox
            self.anesLevel = anes
        else:
            pass
    
    perAnes = property(calcPerAnes, setPerAnes)
    
    def goReset(self):
        self.goCommand("Reset",None)
        
    def goPurgeOn(self):
        self.goCommand("Purge", self.ON)
    
    def goPurgeOff(self):
        self.goCommand("Purge", self.OFF)
        
    def goValveOn(self):
        self.goCommand("Valve", self.ON)
        
    def goValveOff(self):
        self.goCommand("Valve", self.OFF)
        
    def goSetAnes(self,param):
        param = str(param)
        self.goCommand("SetAnesthesia", param)
    
    def goSetOx(self,param):
        param = str(param)
        self.goCommand("SetOxygen", param)
        
    def goQueryOx(self):
        self.goCommand("QueryOxygen", None)
        
    def goQueryAnes(self):
        self.goCommand("QueryAnesthesia", None)
    
    def oxRespond(self, param):
        log.debug("Oxygen values %s" % param)
        self.oxActualFlow, self.oxSetFlow = param.split(",")
        
    def anesRespond(self,param):
        log.debug("Anesthesia values %s" % param)
        self.anesActualFlow,self.anesSetFlow = param.split(",")
        
    def startUpdating(self):
        self.updateThread = AnesUpdateThread(self)
        self.updateThread.start()
    
    def startServer(self):
        self.serverThread = BreathingServerThread(self)
        self.serverThread.start()
    
    def stopUpdating(self):
        self.updateThread.stop()
        self.updateThread.join()
    
    def __del__(self):
        self.updateThread.stop()
        self.updateThread.join()
        





