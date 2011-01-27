
from operation.unitoperationthreadfactory import UnitOperationThreadFactory

class UnitOperation():

    """ Base class for unit operations.
        
    @ivar opname        str     Name of operation
    @ivar device        obj     Device connected to this unit operation
    @ivar params        dict    Dictionary of parameter values (indexed by param name)
    @ivar config        dict    Dictionary of config information about unit operation
                                (e.g. ['Params'] gives meta information about parameters)

    #TOREMOVE:                         
    @ivar complete      bool    Flag set by thread to indicate completion
    @ivar statusMessage str     Status message updated by thread

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

        #TOREMOVE: 
        self.complete = False
        self.statusMessage = ''

    def getLabel(self):
        return self.config['label']
        
    def getParams(self):
        return self.params

    def setParams(self, params):
        self.params = params
        
    def getParam(self, name):
        return self.params[name]
        
    def setParam(self, name, value):
        self.params[name] = value
        
    def setDefaultParams(self):
        self.params = {}
        for name,meta in self.config['Params'].items():
            self.params[name] = meta['default']
            
    def _startThread(self, abortInterval):
        thread = UnitOperationThreadFactory.getThread(self.device, self, abortInterval)
        thread.start()
        # TODO: change to actually reflect thread creation/start status
        return True
    
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

