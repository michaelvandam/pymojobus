
from operation.prm_operations import *

class UnitOperationThreadFactory():

    def __init__(cls):
        pass
        
    @classmethod    
    def getThread(cls, device, operation, abortInterval):
        className = device.deviceType + operation.name + "Operation"
        thread = globals()[className](device, operation, abortInterval)
        return thread


 