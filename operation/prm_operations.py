
from operation.unitoperationthread import *

# Unit operation threads

class PRMReactOperation(UnitOperationThread):
    def __init__(self, device, operation, abortInterval=0.1):
        UnitOperationThread.__init__(self, device, operation, abortInterval)
        
    def run(self):
        react_temp = self.operation.getParam('react_temp')
        react_time = self.operation.getParam('react_time')
        stir_speed = self.operation.getParam('stir_speed')
        cool_temp = self.operation.getParam('cool_temp')
        
        # Dummy example
        self.operation.statusMessage = "Waiting (5 sec)..."
        self.waitForTime(5)
        self.signalComplete()
        
        # Real commands:
        '''
        self.device.goMoveZDown()
        self.operation.statusMessage = "Unsealing reactor..."
        self.waitForState(10, zState, device.DOWN)
        self.device.goMoveX(2)
        self.operation.statusMessage = "Moving to reaction position..."
        self.waitForState(10, xState, 2)
        self.device.goMoveZUp()
        self.operation.statusMessage = "Sealing reactor..."
        self.waitForState(10, zState, device.UP)
        self.device.goMix(stir_speed)
        self.device.goSetpoint(react_temp)
        self.device.goHeaterOn()
        self.operation.statusMessage = "Waiting to reach temperature (%d C)..." % react_temp
        self.waitForState(5, reactorTemperature, react_temp, '>=')
        self.operation.statusMessage = "Performing reaction (%f min)..." % react_time
        self.device.waitForTime(react_time)
        self.device.goHeaterOff()
        self.device.goSetpoint(cool_temp)
        self.device.goCoolOn()
        self.operation.statusMessage = "Waiting for reactor to cool (to %d C)..." % cool_temp
        self.waitForState(600, reactorTemperatute, cool_temp, '<=')
        self.device.goCoolOff()
        self.device.goMix(0)
        self.signalCompletion()
        '''