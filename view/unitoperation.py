
# TODO: Probably should be moved to 'model' directory

import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class UnitOperation():
    """ Base class for unit operations.  Similar to the way devices
        and deviceViews are handled, the operation is contained within views
        rather than using subclassing.
    @ivar name          str     Name of operation
    @ivar label         str     Human-readable label for operation
    @ivar params        dict    Dictionary of params (stored as dicts)
                                (indexed by param name)
    @ivar device        obj     Device connected to this unit operation
    @ivar deviceAddress str     Address of device
    """
    
    def __init__(self, device=None):
        self.device = device
        self.deviceAddress = None
        if device != None:
            self.deviceAddress = device['address']
        self.params = {}
        
    def addParam(self, name, label, value, min=0, max=100):
        param = {'name':name, 'label':label, 'value':value, 'min':min, 'max':max}
        self.params[name] = param
    
    def setParamValue(self, name, value):
        self.params[name]['value'] = value
        
    def getParamValue(self, name):
        return self.params[name]['value']
        
    def execute(self):
        # TODO: Launch operation manager thread 
        # Temporary
        time.sleep(2)

    # TODO: need a re-entrant method that is called when the OperationManager
    # has completed

    
# PRM Unit operations
# TODO: how to handle default values for operations?

class PRMReactOperation(UnitOperation):
    def __init__(self, device=None):
        UnitOperation.__init__(self, device)
        self.name = 'React'
        self.label = 'Perform Reaction'
        self.addParam('react_temp', 'Reaction temperature setpoint (C)', 100, 0, 200)
        self.addParam('react_time', 'Reaction time (min)', 5, 0, 120)
        self.addParam('cool_temp', 'Cooling temperature setpoint (C)', 40, 0, 200)
        self.addParam('stir_speed', 'Stirring speed', 1, 0, 9)

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
