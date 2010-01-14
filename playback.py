import time
import operator
from model import sequence
from model.sequence.dbmodel import CommandMessage
from model.sequence.sequences import sequences
from model import deviceTypes
from utils.mojoconn import ConnectionFactory
from utils.mojoconfig import config
from utils.mojodevicefactory import MojoDeviceFactory
from utils.mojoviewfactory import mojoViewFactory
from utils import mojologger
from view import deviceViewTypes
from utils.mojorecorder import turnRecordingOn
from utils.mojorecorder import turnRecordingOff
from sqlalchemy import desc, asc
from mojo import Mojo

log = mojologger.logging.getLogger()

log.info("*BEGIN MOJO PLAYBACK*")
    

def playBack(mojo):
    turnRecordingOff()
    mojo.stopDeviceUpdating()
    
    session = sequences.Session()
    cmds = session.query(CommandMessage).order_by(asc(CommandMessage.created)).all()
    #cmds.sort(key=operator.attrgetter("created"))
    
    for cmd in cmds:
        print cmd.created, cmd.delay
        mojo.devices[cmd.deviceAddress].goCommand(cmd.command, str(cmd.param))
        print cmd
        print "Sleeping %s " % cmd.delay
        time.sleep(cmd.delay)

def main():
    pass

if __name__=='__main__':
    mojo = Mojo()
    config['SerialSettings']['port']=9
    mojo.makeConnection(config)
    time.sleep(2)
    mojo.getDevices()
    while(1):
        playBack(mojo)
    
