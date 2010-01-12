from mojodevices import MojoDevices
from mojoerrors import * 
from mojomessages import MojoReceivedMessage, MojoSendMessage, MojoAddress
from mojoconfig import config
import time
import logging

log = logging.getLogger()

class MojoDeviceFactory( object ):
    
    def __init__(self, mojoconn):
        self.mojoconn = mojoconn
        self.devices = MojoDevices()

    def enumerateDevices(self):
        
        msg = MojoSendMessage(
                        MojoAddress(
                        sender=config['MojoSettings']['masteraddress'],
                        receiver=config['MojoSettings']['broadcastaddress']
                        )
                    )
        msg.addCommand("ANNC")
        log.debug("Sending Announce to bus: '%s'" % str(msg).strip())
        self.mojoconn._mojoWrite(msg)
        
        responses = self.mojoconn.mojoRead(pause=2)
        for response in responses:
            log.debug("Received WHO from bus: '%s'" % str(response).strip())
            self.devices.addDeviceFromAnnc(response, self.mojoconn)
        
        return self.getDevices()
        
    def getDevices(self):
        log.debug("Retreiving devices")
        return self.devices