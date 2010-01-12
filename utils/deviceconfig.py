from configobj import ConfigObj
from validate import Validator
from mojoerrors import *
from os import path
from mojoconfig import config

def getDeviceConfig(deviceName):
    deviceconfigfilename= config['MojoSettings']['deviceconfigsdir'] + "%s.ini" % deviceName.lower()
    deviceconfigspec = config['MojoSettings']['deviceconfigspec']
    
    if not path.isfile(deviceconfigfilename):
        raise MojoBadDeviceConfig("Config file does not exist: %s" % deviceconfigfilename)
    
    if not path.isfile(deviceconfigspec):
        raise MojoBadDeviceConfig("Config spec file does not exist: %s" % deviceconfigfilename)
    
    
    devc = ConfigObj(deviceconfigfilename, configspec=deviceconfigspec)

    validator = Validator()

    result = devc.validate(validator)

    if result!=True:
        raise MojoBadDeviceConfig("Config file is invalid: %s" % deviceconfigfilename)
    else:
        return devc
        
    
    
if __name__=='__main__':
    deviceConfigs = [getDeviceConfig('RDM'),
                     getDeviceConfig('PRM'),
                     getDeviceConfig('CPM')]