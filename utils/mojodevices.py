# mojodevices.py 
# mojodevices object which is a subclass of a dictionary
# and therefore capable of device lookups!

# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!

from mojoerrors import *
from mojoconfig import config, masterAddress
from mojomessages import MojoReceivedMessage, MojoSendMessage, MojoAddress 
from model import deviceTypes
import logging

log = logging.getLogger()

class MojoDevices(dict):
    def __init__(self,  *args, **kwargs):
        super(MojoDevices,self).__init__(*args,**kwargs)
        log.debug("Creating MojoDevices container")
        
    def getDevice(self, address, deviceType, version, conn, ignoreBadDevice=False):
        try:
            #import pdb
            #pdb.set_trace()
            return deviceTypes[deviceType](address, conn, version)
                
        except NameError:
            #import pdb
            #pdb.set_trace()
            if ignoreBadDevice is True:
                return None
            else:
                raise MojoBadDevice("Device '%s' is not implemented" % deviceType)
        return None
    
    def addDeviceFromAnnc(self, msg, conn):
        address, deviceType, version = self.parseDeviceAnnc(msg)
        
        device = self.getDevice(address, deviceType, version , conn)
        if device:
            self[address]=device
        else:
            pass
    
    def parseDeviceAnnc(self, msg):
        address = msg.address.sender
        for cmd in msg.cmds:
            if cmd.cmd == "*ANNC":
                try:
                    deviceType,version = cmd.param.split(config['MojoSettings']['versionSep'])
                except ValueError,e :
                    raise MojoBadAnnc("Device did not return valid ANNC string")
        return address, deviceType, version
      
    def addresses(self):
        return self.keys()

    def devices(self):
        return self.values()
        
        