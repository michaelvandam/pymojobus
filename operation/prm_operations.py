
from unitoperation import UnitOperation, UnitOperationThread

# Unit operation classes

class PRMReactOperation(UnitOperation):
    def __init__(self, device=None):
        UnitOperation.__init__(self, device)
        self.name = 'React'
        self.label = 'Perform Reaction'
        self.addParam('react_temp', 'Reaction temperature setpoint (C)', 100, 0, 200)
        self.addParam('react_time', 'Reaction time (min)', 5, 0, 120)
        self.addParam('cool_temp', 'Cooling temperature setpoint (C)', 40, 0, 200)
        self.addParam('stir_speed', 'Stirring speed', 1, 0, 9)
        
    def _startThread(self,abortInterval):
        thread = PRMReactOperationThread(self.device, self, abortInterval)
        thread.start()
        return True  # Change to actually reflect thread creation/start status

class PRMEvapOperation(UnitOperation):
    def __init__(self, device=None):
        UnitOperation.__init__(self,device)
        self.name = 'Evaporate'
        self.label = 'Perform Solvent Evaporation'
        self.addParam('evap_temp', 'Evaporation temperature setpoint (C)', 100, 0, 200)
        self.addParam('evap_time', 'Evaporation time (min)', 5, 0, 120)
        self.addParam('cool_temp', 'Cooling temperature setpoint (C)', 40, 0, 200)
        self.addParam('stir_speed', 'Stirring speed', 1, 0, 9)

class PRMReagentOperation(UnitOperation):
    def __init__(self, device=None):
        UnitOperation.__init__(self,device)
        self.name = 'Reagent'
        self.label = 'Add Reagent'

class PRMXferTrapOperation(UnitOperation):
    def __init__(self, device=None):
        UnitOperation.__init__(self,device)
        self.name = 'Xfer Trap'
        self.label = 'Transfer to Catridge (Trap)'

class PRMXferEluteOperation(UnitOperation):
    def __init__(self, device=None):
        UnitOperation.__init__(self, device)
        self.name = 'Xfer Trap'
        self.label = 'Transfer to Catridge (Elute)'

class PRMXferHPLCOperation(UnitOperation):
    def __init__(self, device=None):
        UnitOperation.__init__(self, device)
        self.name = 'Xfer HPLC'
        self.label = 'Transfer to HPLC'

class PRMAccessOperation(UnitOperation):
    def __init__(self, device=None):
        UnitOperation.__init__(self, device)
        self.name = 'Access vial'
        self.label = 'Move vial to Accessible position'

# Unit operation threads

class PRMReactOperationThread(UnitOperationThread):
    def __init__(self, device, operation, abortInterval=0.1):
        UnitOperationThread.__init__(self, device, operation, abortInterval)
        
    def run(self):
        react_temp = self.operation.getParamValue('react_temp')
        react_time = self.operation.getParamValue('react_time')
        stir_speed = self.operation.getParamValue('stir_speed')
        cool_temp = self.operation.getParamValue('cool_temp')
        
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