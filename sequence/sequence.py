
import os
from configobj import ConfigObj
from validate import Validator
from os import path, listdir
from operation.unitoperation import UnitOperation

class Sequence():

    def __init__(self, devices, config=None):
        self.devices = devices
        self.config = config
        if config == None:
            self.name = ''
            self.version = '1.0'
            self.author = ''
        else:
            self.name = config['name']
            self.version = config['version']
            self.author = config['author']
        self.operations = []
        self._populateOperations()
        
    def _populateOperations(self):
        for opconfig in self.config['Operations'].values():
            op = UnitOperation(self.devices[opconfig['device']], opconfig['name'], opconfig['params'])
            self.operations.append(op)

            
class SequenceManager():

    def __init__(self, devices):
        self.sequencePath = 'sequence/sequences/'
        self.sequenceSpec = 'sequence/sequencespec.ini'
        self.devices = devices
    
    def listSequences(self):
        return os.listdir(self.sequencePath)
    
    def loadSequence(self, filename):
        fullname = self.sequencePath + filename
        if not path.isfile(fullname):
            # TODO: raise exception
            print "ERROR(sequence): invalid sequence name %s" % fullname
        if not path.isfile(self.sequenceSpec):
            # TODO: raise exception
            print "ERROR(sequence): sequence spec file does not exist %s" % self.sequenceSpec
            
        sequenceConfig = ConfigObj(fullname, configspec=self.sequenceSpec)
        validator = Validator()
        result = sequenceConfig.validate(validator)
        
        if result != True:
            # TODO: Raise exception
            print "ERROR(sequence): sequence failed validation"

        return Sequence(devices, sequenceConfig)

