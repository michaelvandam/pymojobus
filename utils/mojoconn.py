# mojoconn.py 
# Code that manages connections and communication threads

# device code to update state and issue callback functions
# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!

import serial
import sys
import time

from mojoconfig import config
from mojomessages import MojoReceivedMessage, MojoSendMessage
from mojoerrors import *
from mojomessagethread import MojoRXMonitor, MojoTXMonitor
from mojomessagedispatch import MojoResponseDispatch
from mojoqueues import responses, outboundMessages
import logging

log = logging.getLogger()
errlog = logging.getLogger("mojo.error")

ENDCHAR = '$'

class MojoConnection(serial.Serial):
    def __init__(self, serialconfig):
        super(MojoConnection, self).__init__(**serialconfig)
        self.config = serialconfig


    def startMonitor(self, devices):
        self.rxmon = MojoRXMonitor(self) 
        self.txmon = MojoTXMonitor(self)
        log.debug("MojoConnection object starting monitor threads")
        self.rxmon.start()
        self.txmon.start()
        log.debug("MojoConnection object starting dispatch thread")
        self.dispatcher = MojoResponseDispatch(devices)
        self.dispatcher.start()
        
    def mojoRead(self, pause=0):
        responses = []
        time.sleep(pause)
        while(self.inWaiting()):
            s = self.readline(eol=ENDCHAR)
            log.debug("Response: %s" % s)
            try:
                responses.append(MojoReceivedMessage(s))
            except MojoInvalidMessage,e:
                errlog.error("Could not parse message(%s): %s" % (e,s))
        #import pdb
        #pdb.set_trace()
        return responses
    
    
    def mojoSend(self, msg):
        self.txmon.addMessage(msg)
        
    def _mojoWrite(self, msg):
        self.write(str(msg))
    
    def stopMonitor(self):
        self.rxmon.stop()
        self.rxmon.join()
        self.txmon.stop()
        self.txmon.join()
        self.dispatcher.stop()
        self.dispatcher.join()
        


def ConnectionFactory(config = config):
    return MojoConnection(serialconfig=config["SerialSettings"])
    
        
if __name__=='__main__':
    con = ConnectionFactory()
    