
# TODO: implement a progress bar or countdown timer to show progress of operations
#   Could use another timer that calls setStatusMessage periodically?

# TODO: check that we don't have race conditions that might allow two waitLoop.exit()
#   calls in a row

import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class UnitOperationThread(QObject):

    """ Base class for executing unit operations.  The object will be moved to a QThread
        context which runs an event loop and thus allows communication via SIGNALs and
        SLOTs to the main program.  Note that the thread should not block the event loop
        or communication will not work.
        
        NOTE: This class could be implemented as a subclass of QThread and started
        directly, but apparently this is not recommended.  Among other reasons, it is
        confusing because anything (e.g. member variables and timers) defined before
        the 'run' method are not available in the thread.
        
    @ivar device            obj     Device on which operation is being executed
    @ivar operation         obj     Unit operation being executed
    @ivar timeoutEvent      obj     Threading.Event flag for timer to user
    @ivar conditionEvent    obj     Threading.Event flag for condition met
    @ivar abortRequested    bool    Abort signal was requested
    @ivar pollInterval      int     Interval (in msec) between checking device state
    @ivar eventLoop         obj     Local event loop for signalling with locally-created
                                    timers, etc.
    @ivar abortLoop         obj     Local event loop to wait after 'abort' until thread
                                    is terminated
                                    
    @slot abortRequested()      Request aborting the current operation
    @signal abortAck()          Response that thread is aborting.  Awaiting termination
                                form outside.  (Hangs if do QThread.currentThread().terminate().)
    @signal requestInput(str)   Request user input from the main program.  Display str as a prompt
    @slot inputReceived()       Response from user (for now, no data; assume just OK button)

    """

    def __init__(self, device, operation, pollInterval=100):
        QObject.__init__(self)
        self.device = device
        self.operation = operation
        self.waitLoop = QEventLoop(self)
        self.abortLoop = QEventLoop(self)
        
    def run(self):
        # Set up timeout timer
        self.timeoutTimer = QTimer(self)
        self.timeoutTimer.setSingleShot(True)
        self.connect(self.timeoutTimer, SIGNAL('timeout()'), self._slotTimeout)
        # Set up timer for periodically checking state of system
        self.conditionTimer = QTimer(self)
        self.connect(self.conditionTimer, SIGNAL('timeout()'), self._slotConditionCheck)
        
    def setStatusMessage(self,message):
        """ Send signal with status message to GUI
        """
        self.emit(SIGNAL('status(PyQt_PyObject)'), message)

    def waitForInput(self, prompt):
        """ Since a QThread cannot directly update the GUI, emit a signal to the GUI
            requesting user input.
            
        @param prompt   string      Prompt to be displayed to the user
        """
        self.emit(SIGNAL('requestInput(PyQt_PyObject)'), prompt)
        # Enter event loop and wait for 'inputReceived' signal from GUI
        self.waitLoop.exec_()

    def slotInputReceived(self):
        print "UnitOperationThread: INPUTRECEIVED"
        # Exit from event loop, i.e. return from call to waitForInput
        self.waitLoop.exit()
        
    def waitForTime(self, time_in_seconds):
        self.timeout = False
        self.timeoutTimer.start(1000 * time_in_seconds)
        # Enter event loop and wait for 'timeout' signal from timer
        self.waitLoop.exec_()

    def _slotTimeout(self):
        print "UnitOperationThread: TIMEOUT"
        self.timeout = True
        self.timeoutTimer.stop()
        # Exit from current event loop
        self.waitLoop.exit()

    def _slotConditionCheck(self):
        print ":"
        if self._compare(self.operation.device[property], state, comparison):
            self.conditionMet = True
            self.conditionTimer.stop()
            self.waitLoop.exit()

    def slotAbort(self):
        """ Slot to receive signal from the GUI to abort the thread
        """
        print "UnitOperationThread: ABORT"
        # Cleanup, stop timers, sever connected SIGNALs and SLOTs
        self.timeoutTimer.stop()
        self.conditionTimer.stop()
        # Emit signal to GUI, ready to abort (we do this because calling
        # terminate from within the thread causes program to hang)
        self.emit(SIGNAL('abortAck()'))
        # Block here until thread terminated
        self.abortLoop.exec_()        

    def waitForState(self, timeout_in_seconds, property, state, comparison="="):
        """ Wait for a particular device state to be achieved.
        @param timeout      float   Timeout (seconds) before give up monitoring
        @param property     str     Name of device property to monitor
        @param state        str     Desired value/state of property
        @param comparison   str     Comparison operator to use
        @return             bool    True if condition met; False if timeout
        """
        self.conditionMet = False
        self.timeout = False
        self.timeoutTimer.start(1000 * timeout_in_seconds)
        self.conditionTimer.start(self.pollInterval)
        # Wait in event loop for condition met or timeout
        self.waitLoop.exec_()
        # At this point, timeout or conditionMet is True.
        self.timeoutTimer.stop()
        self.conditionTimer.stop()
        if self.conditionMet:
            return True
        elif self.timeout:
            return False
        else:
            print "ERROR: should never get here"
            
    def finish(self):
        # Must be called at the end of run
        # Call 'exit' on the current thread context (to escape from event loop)
        QThread.currentThread().exit()
        
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
            