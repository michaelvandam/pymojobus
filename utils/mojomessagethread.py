# mojomessagethread.py 
# Threads for receiving and sending messages to the serial connection
# take care of the act of communicating with the bus
# You should not need to interact with these objects, instead add and retrieve messages
# from the Queue

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
from threading import Thread, Event
import time
from mojoqueues import responses, outboundMessages
import logging
import Queue
from mojothread import MojoThread

log = logging.getLogger()
msglog = logging.getLogger("mojo.message")
errlog = logging.getLogger("mojo.error")

class MojoRXTXMonitor(MojoThread):
    incomingMessage = Event()

class MojoTXMonitor(MojoRXTXMonitor):
    
    def __init__(self, conn):
        MojoThread.__init__(self)
        self.messages=outboundMessages
        self.conn = conn
        self.setName("TX Thread")
        
    def run(self):
        
        log.debug("Starting MojoTXMonitor Thread")
        msglog.info("Starting MojoTXMonitor Thread")
        while(not self.stop_event.isSet()):
            if not self.incomingMessage.isSet():
                try:
                    msg = self.messages.get(True,2)
                    log.info("Sent: %s" % str(msg).strip())
                    msglog.info("Sent: %s" % str(msg).strip())
                    self.conn._mojoWrite(msg)
                    self.incomingMessage.set()
                    self.messages.task_done()
                except Queue.Empty:
                    msglog.debug("No message to send...")
            else:
                msglog.debug("Waiting on reply...")
                
        self.stop_event.clear()
        msglog.info("Shutdown TX Thread")
        #MojoTXMonitor.__init__(self, self.conn)
                
    
    
    def addMessage(self, msg):
        self.messages.put(msg)
            

class MojoRXMonitor(MojoRXTXMonitor):
    
    def __init__(self, conn):
        MojoThread.__init__(self)
        self.responses=responses
        self.conn = conn
        self.setName("RX Thread")
    
    def run(self):
        log.debug("Starting MojoRXMonitor Thread")
        msglog.info("Starting MojoRXMonitor Thread")
        while(not self.stop_event.isSet()):
            if self.incomingMessage.isSet() and self.conn.inWaiting() <= 0:
                time.sleep(.1)
                msglog.debug("Waiting for incoming reply...")
                if self.conn.inWaiting() <= 0:
                    msglog.error("No reply...")
                    self.incomingMessage.clear()
            elif self.incomingMessage.isSet() and self.conn.inWaiting() > 0:
                rs = self.conn.mojoRead()
                if rs:
                    for r in rs:
                        self.responses.put(r)
                        log.info("Received: %s" % str(r).strip())
                        msglog.info("Received: %s" % str(r).strip())
                        self.incomingMessage.clear()        
            else:
                msglog.debug("No incoming message...")
                self.incomingMessage.wait(.1)
                
            
        self.stop_event.clear()
        msglog.info("Shutdown RX Thread")
        #MojoRXMonitor.__init__(self, self.conn)
            