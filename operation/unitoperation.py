
from PyQt4.QtCore import *

from operation.unitoperationthreadfactory import UnitOperationThreadFactory

class UnitOperation():

    """ Base class for unit operations.
        
    @ivar opname        str     Name of operation
    @ivar device        obj     Device connected to this unit operation
    @ivar params        dict    Dictionary of parameter values (indexed by param name)
    @ivar config        dict    Dictionary of config information about unit operation
                                (e.g. ['Params'] gives meta information about parameters)
    """

    def __init__(self, device, opname, params=None):
        self.name = opname
        self.device = device
        # TODO: Error checking
        self.config = device.config['UnitOperations'][self.name]
        if params == None:
            self.setDefaultParams()
        else:
            self.params = params

    def getLabel(self):
        return self.config['label']
        
    def getParams(self):
        return self.params

    def setParams(self, params):
        self.params = params
        
    def getParam(self, name):
        if name in self.params:
            return self.params[name]
        else:
            if self.config['Params'][name]['type'] == 'string':
                return self.config['Params'][name]['default_string']
            else:
                return self.config['Params'][name]['default_value']
        
    def setParam(self, name, value):
        self.params[name] = value
        
    def setDefaultParams(self):
        self.params = {}
        for name,meta in self.config['Params'].items():
            if meta['type'] == 'string':
                self.params[name] = meta['default_string']
            else:
                self.params[name] = meta['default_value']
    
    def getThread(self, abortInterval):
        thread = UnitOperationThreadFactory.getThread(self.device, self, abortInterval)
        return thread

        
class WrapperThread(QThread):
    """ Wrapper thread from unit operation threads.  See comments in unitoperationqthread.py
    """
    def __init__(self):
        super(WrapperThread, self).__init__()

    def run(self):
        self.exec_()
