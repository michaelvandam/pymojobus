import time

from model import experiment
from model.experiment.commandmessage import CommandMessage
from model.experiment import Session

from model import deviceTypes
from utils.mojoconn import ConnectionFactory
from utils.mojoconfig import config
from utils.mojodevicefactory import MojoDeviceFactory
from utils.mojoviewfactory import mojoViewFactory
from utils import mojologger
from view import deviceViewTypes
from utils.mojorecorder import turnRecordingOn
from utils.mojorecorder import turnRecordingOff

log = mojologger.logging.getLogger()

log.info("*BEGIN MOJO*")

class Mojo(object):
    def __init__(self,config=config):
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
    
    def getDeviceViews(self):
        self.deviceViews = mojoViewFactory(self.devices, deviceViewTypes)

    def dropDevices(self):
        self.devices

    def stopMonitor(self):
        self.conn.stopMonitor()

mojo = Mojo()
    

def playBack(mojo):
    turnRecordingOff()
    for device in mojo.devices.values():
        try:
            device.stopUpdating()
        except AttributeError:
            pass
        
    session = Session()
    for cmd in session.query(CommandMessage).all():
        import pdb
        #pdb.set_trace()
        mojo.devices[cmd.deviceAddress].goCommand(cmd.command, str(cmd.param))
        #time.sleep(1)
    #for device in mojo.devices:
    #    try:
    #        device.startUpdating()
    #    except AttributeError:
    #        pass

def main():
    pass

if __name__=='__main__':
    config['SerialSettings']['port']=9
    mojo.makeConnection(config)
    time.sleep(2)
    mojo.getDevices()
    playBack(mojo)
