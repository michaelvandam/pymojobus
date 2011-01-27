
from mojo import Mojo
from utils.mojodevicefactory import MojoDeviceFactory
from utils.mojodevices import MojoDevices
from utils.mojoconfig import *

class MockMojo(Mojo):

    def __init__(self, config=config):
        Mojo.__init__(self, config)
        
    def getDeviceFactory(self):
        self.deviceFactory = MockMojoDeviceFactory(self.conn)    

    def getDevices(self):
        self.getDeviceFactory()
        self.devices = self.deviceFactory.enumerateDevices()
        #self.conn.startMonitor(self.devices)
        return self.devices
        
        
class MockMojoDeviceFactory(MojoDeviceFactory):
    
    def __init__(self, mojoconn):
        MojoDeviceFactory.__init__(self, mojoconn)

    def enumerateDevices(self):
        self.devices['a'] = self.devices.getDevice('a', 'PRM', '0.1', self.mojoconn)
        self.devices['b'] = self.devices.getDevice('b', 'PRM', '0.1', self.mojoconn)
        self.devices['c'] = self.devices.getDevice('c', 'PRM', '0.1', self.mojoconn)
        return self.getDevices()