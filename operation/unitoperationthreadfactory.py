
from operation.prm_operations import *
from operation.common_operations import *

class UnitOperationThreadFactory():

    def __init__(cls):
        pass
        
    @classmethod    
    def getThread(cls, device, operation, pollInterval):
        className = operation.config['threadClass']
        #className = device.deviceType + operation.name + "Operation"
        thread = globals()[className](device, operation, pollInterval)
        return thread

