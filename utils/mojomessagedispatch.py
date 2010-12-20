# mojomessagedispatch.py 
# Thread in charge of dispatching responses from serial com to 
# device code to update state and issue callback functions

# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!



import sys
import threading
import Queue
from threading import Thread
from mojoqueues import responses
from mojoerrors import *
from mojothread import MojoThread
import logging

log = logging.getLogger()
msglog = logging.getLogger("mojo.message")
errlog = logging.getLogger("mojo.error")

class MojoResponseDispatch( MojoThread ):
    
    def __init__(self, devices):
        MojoThread.__init__(self)
        self.responses = responses
        self.devices = devices
        self.setName("Dispatch Thread")
    
    def run(self):
        
        msglog.debug("Starting MojoResponseDispatch Thread")
        while(not self.stop_event.isSet()):
            try:
                response = self.responses.get(False,.2)
                try:
                    device = self.devices[response.address.sender]
                    if not device.lastMessage == response:
                        msglog.info("Device expecting different response, could be update message")
                        
                    log.debug("Dispatch Msg: %s -> Device:%s" % (str(response).strip(),device))
                    try:
                        device.processResponse(response)
                    except:
                        msglog.error("%s -> Device unable to process response" % device)
                except MojoException, e:
                    errlog.error("Error with response dispatch: %s" % e)
                    
                self.responses.task_done()
            except Queue.Empty:
                pass
        
        self.stop_event.clear()
        msglog.info("Dispatch Thread Shutdown")
