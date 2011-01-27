import time
from model import deviceTypes
from utils.mojoconn import ConnectionFactory
from utils.mojoconfig import config
from utils.mojodevicefactory import MojoDeviceFactory
from utils import mojologger


log = mojologger.logging.getLogger()


class Mojo(object):
    def __init__(self,config=config):        
        log.info("*BEGIN MOJO*")
        self.conn = None
        self.deviceFactory=None
        self.devices=None
        self.config=config

    def makeConnection(self,config=config):
        self.conn = ConnectionFactory(config)
        time.sleep(1)
        
    def closeConnection(self):
        self.conn.close()

    def getDeviceFactory(self):
        self.deviceFactory = MojoDeviceFactory(self.conn)

    def getDevices(self):
        self.getDeviceFactory()
        self.devices = self.deviceFactory.enumerateDevices()
        self.conn.startMonitor(self.devices)
        
    def dropDevices(self):
        self.devices

    def stopMonitor(self):
        self.conn.stopMonitor()

    def stopDeviceUpdating(self):
        for device in self.devices.values():
            try:
                device.stopUpdating()
            except AttributeError:
                pass
            
    def shutdown(self):
        self.stopDeviceUpdating()
        self.stopMonitor()
        self.conn.close()
    
def main():
    pass

if __name__=='__main__':
    mojo=Mojo()
    mojo.makeConnection(config)
    time.sleep(2)
    devices = mojo.getDevices()
    mojo.stopDeviceUpdating()
    