
# TODO: how to handle default values for operations?

import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import Thread, Timer, Event

# Base class for unit operations

class UnitOperation():

    """ Base class for unit operations.
        
    @ivar name          str     Name of operation
    @ivar label         str     Human-readable label for operation
    @ivar params        dict    Dictionary of params (stored as dicts)
                                (indexed by param name)
    @ivar device        obj     Device connected to this unit operation
    @ivar complete      bool    Flag set by thread to indicate completion
    @ivar statusMessage str     Status message updated by thread

    """
    
    def __init__(self, device):
        self.device = device
        self.params = {}
        self.complete = False
        self.thread = None
        self.statusMessage = ''
        
    def addParam(self, name, label, value, min=0, max=100):
        param = {'name':name, 'label':label, 'value':value, 'min':min, 'max':max}
        self.params[name] = param

    # Helper methods to link fields in operationsView to unit operation
    def setParamValue(self, name, value):
        self.params[name]['value'] = value
        
    def getParamValue(self, name):
        return self.params[name]['value']

    def _startThread(self, abortInterval):
        return False
        # Override in subclasses

    def abort(self):
        pass
        # TODO: need to keep track of the thread object so we can call thread.abort()
        
    def execute(self, abortInterval):
        """ Execute the unit operation
        @param abortInterval    float   Desired interval (in seconds) for abort checking
        """
        self.complete = False
        if self._startThread(abortInterval):
            self.isRunning = True
            return True
        return False
        
    def finish(self):
        self.isRunning = False

# Base Class for Unit Operation threads

# Some ideas from Henry's code and from here.  Also borrowed from:
# http://code.activestate.com/recipes/65448-thread-control-idiom/

class UnitOperationThread(Thread):

    """ Base class for threads that execute unit operations
    @ivar device            obj     Device on which operation is being executed
    @ivar operation         obj     Unit operation being executed
    @ivar timeoutEvent      obj     Threading.Event flag for timer to user
    @ivar conditionEvent    obj     Threading.Event flag for condition met
    @ivar abortReq          bool    Abort signal was requested
    @ivar abortInterval     float   Interval (in seconds) between checking for abort signal
    """

    def __init__(self, device, operation, abortInterval=0.1):
        Thread.__init__(self)
        self.device = device
        self.operation = operation
        self.timeoutEvent = Event()
        self.conditionEvent = Event()
        self.abortReq = False
        self.abortInterval = abortInterval

    # NOTE: I don't really like this approach (setting property directly) but it seems
    # these threads cannot call methods on objects in the main thread.  The MainWindow
    # is already polling for thread status (completion) so it also monitors status
    # messages and notifies views if they change.
    def setStatus(self,msg):
        self.operation.statusMessage = msg

    def abort(self):
        self.abortReq = True
        
    def abortRequested(self):
        return self.abortReq

    # TODO: could have calls from here to update status/progress
    def waitForTime(self,time):
        self.timeoutEvent.clear()
        timer = Timer(time, self._timeout)
        timer.start()
        while not self.timeoutEvent.isSet():
            if self.abortRequested():
                self.timeoutEvent.set()
                # TODO: cleanup and abort thread
            self.timeoutEvent.wait(self.abortInterval)
                
    def _timeout(self):
        self.timeoutEvent.set()

    # TODO: could have calls from here to update status/progress
    def waitForState(self, timeout, property, state, comparison="="):
        """ Wait for a particular device state to be achieved.
        @param timeout      float   Timeout (seconds) before give up monitoring
        @param property     str     Name of device property to monitor
        @param state        str     Desired value/state of property
        @param comparison   str     Comparison operator to use
        """
        self.conditionEvent.clear()
        self.timeoutEvent.clear()
        timer = Timer(timeout, self._timeout)
        timer.start()
        while not self.conditionEvent.isSet():
            if self.abortRequested():
                self.conditionEvent.set()
                # TODO: cleanup and abort thread
            if self._compare(self.operation.device[property], state, comparison):
                self.conditoinEvent.set()
            if self.timeoutEvent.isSet():
                self.conditionEvent.set()
                # TODO: respond to timeout
            self.conditionEvent.wait(self.abortInterval)

    def _compare (a, b, operator='='):
        if (operator == '=' or operation == '=='):
            return a == b
        elif (operator == '>'):
            return a > b
        elif (operator == '>='):
            return a >= b
        elif (operator == '<'):
            return a < b
        elif (operator == '<='):
            return a <= b
        else:
            # TODO: raise exception
            print "ERROR(UnitOperationThread): unknown operator %s" % operator
            return False
            
    def run(self):
        pass
        #Override with operation-specific things here
        
    def signalComplete(self):
        # Set a property in the operation object to indicate completion
        self.operation.complete = True
