
# TODO: where should we store operations that belong to the 'system'? Probably should not be associated
# with individual devices.  Example operations:
#   - Pause (create a popup; useful for debuggging)
#   - StartRun (open a file, beginning logging sensor data)
#   - FinishRun (close file, generate report)
#   - etc.

from operation.unitoperationqthread import *

# Unit operation threads

class MasterPauseOperation(UnitOperationThread):

    def __init__(self, device, operation, pollInterval=100):
        UnitOperationThread.__init__(self, device, operation, pollInterval)

    def run(self):
        UnitOperationThread.run(self)
        #print self.operation.params
        message = self.operation.getParam('message')
        self.setStatusMessage("Waiting for time... 2 sec")
        self.waitForTime(2)
        self.setStatusMessage("Waiting for user input...")
        message = "test message, testing 123"
        self.waitForInput(message)
        # Exit out of the event loop
        self.finish()
        
        