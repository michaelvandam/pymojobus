#!/usr/bin/env python
# mojotask.py 
# Base class for all mojo tasks

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
from threading import Timer
import Queue
from threading import Thread, Event
from mojothread import MojoThread
from mojoerrors import *
from mojoconfig import config, masterAddress
from mojomessages import MojoReceivedMessage, MojoSendMessage, MojoAddress 
from deviceconfig import getDeviceConfig


log = logging.getLogger()
errlog = logging.getLogger("mojo.error")


class MojoTaskNoFxnException(Exception):
    pass

class MojoUnknownParamException(Exception):
    pass

class MojoTimeoutException(Exception):
    pass

class MojoTimer(object):
    "Thread that sets event after a timeout occurs"
    def __init__(self, timeout):
        self.timeout=timeout
        self.completeEvent = Event()
        self.completeEvent.clear()
        
    def start(self):
        self.completeEvent.clear()
        log.debug("MojoTimer started %d sec" % self.timeout)
        timer = Timer(self.timeout,self.__set)
        timer.start()
        
    def __set(self):
        log.debug("MojoTimer complete after %d sec" % self.timeout)
        self.completeEvent.set()
    
    def __call__(self):
        if self.completeEvent.isSet():
            return True
        else:
            return False

class MojoDeviceNotifyTransitionThread(MojoThread):
    """
    Monitor Device For State to Equal Transition,
    end thread and set Event or wait for a timeout
    """
    
    def __init__(self, state, condition, timeout):
        self.state = state
        self.condition = condition
        self.timeout = MojoTime(timeout)
        self.__hasTransitioned =Event()
        self.__hasTransitioned.clear()
        self.__hasTimedout =Event()
        self.__hasTimedout.clear()
        
    def run(self):
        log.debug("Starting Transition Monitor Thread")
        self.timeout.start()
        while(not self.stop_event.isSet()):
            if state==condition:
                self.__hasTransitioned.set()
                self.stop_event.set()
            if timeout():
                self.__hasTimedout.set()
                self.stop_event.set()
    
    def hasTransitioned(self):
        if self.__hasTransitioned.isSet():
            return True
        else:
            return False
    
    def hasTimedout(self):
        if self.__hasTimedout.isSet():
            return True
        else:
            return False


class MojoTask(object):
    """
    MojoTask take in fxn and parameters,
    call it and wait for device state to
    be in a condition or timeout
    """

    def __init__(self, function=None, state=None, condition=None, parameters=None, timeout=0):
        self.device = device
        self.fxn = function
        self.state=state
        self.condition=condition
        self.params = parameters
        self.timeout=timeout
        self.stopEvent = Event()
        self.transMonitorThread = MojoDeviceNotifyTransitionThread(state, condition, timeout)

    def __run(self):
        if self.fxn is None:
            raise MojoTaskNoFxnException
        elif isinstance(self.params, dict):
            self.fxn(**self.params)
        elif isinstance(self.param, list):
            self.fxn(*self.params)
        elif self.param is None:
            self.fxn()
        else:
            raise MojoUnknownParamException
        
        self.transMonitorThread.start()
        while not self.transMonitorThread.hasTimedout() or  not self.transMonitorThread.hasTransitioned():
            raise MojoTimeoutException
        
        