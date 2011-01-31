
from operation.unitoperationqthread import *

# Unit operation threads

class PRMReactOperation(UnitOperationThread):

    def __init__(self, device, operation, pollInterval=100):
        UnitOperationThread.__init__(self, device, operation, pollInterval)
        
    def run(self):
        UnitOperationThread.run(self)

        react_temp = self.operation.getParam('react_temp')
        react_time = self.operation.getParam('react_time')
        stir_speed = self.operation.getParam('stir_speed')
        cool_temp = self.operation.getParam('cool_temp')
        
        # Dummy example
        self.setStatusMessage("Waiting (5 sec)...")
        self.waitForTime(5)
        
        # Real commands:
        '''
        self.device.goMoveZDown()
        self.setStatusMessage("Unsealing reactor...")
        if not self.waitForState(10, zState, device.DOWN):
            pass
            # self.abort("Timeout while trying to lower reactor")
        self.device.goMoveX(2)
        self.setStatusMessage("Moving to reaction position...")
        self.waitForState(10, xState, 2)
        self.device.goMoveZUp()
        self.setStatusMessage("Sealing reactor...")
        self.waitForState(10, zState, device.UP)
        self.device.goMix(stir_speed)
        self.device.goSetpoint(react_temp)
        self.device.goHeaterOn()
        self.setStatusMessage("Waiting to reach temperature (%d C)..." % react_temp)
        self.waitForState(5, reactorTemperature, react_temp, '>=')
        self.setStatusMessage("Performing reaction (%f min)..." % react_time)
        self.device.waitForTime(60 * react_time)
        self.device.goHeaterOff()
        self.device.goSetpoint(cool_temp)
        self.device.goCoolOn()
        self.setStatusMessage("Waiting for reactor to cool (to %d C)..." % cool_temp)
        self.waitForState(600, reactorTemperatute, cool_temp, '<=')
        self.device.goCoolOff()
        self.device.goMix(0)
        '''
        self.finish()