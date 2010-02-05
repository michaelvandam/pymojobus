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
    cmds = sequences.getCommandsInSequence()
    print cmds
    #cmds.sort(key=operator.attrgetter("created"))
    previouscmd = None
    for cmd in cmds:
        if not previouscmd is None:
            print cmd.created
            print previouscmd.created
            delay = cmd.getDurationInSeconds(previouscmd)
        else:
            delay = 0
        mojo.devices[cmd.deviceAddress].goCommand(cmd.command, str(cmd.param))
        print cmd
        print "Sleeping %s " % delay
        time.sleep(delay)
        previouscmd = cmd

def main():
    pass

if __name__=='__main__':
    mojo = Mojo()
    mojo.makeConnection(config)
    time.sleep(2)
    mojo.getDevices()
    while(1):
        playBack(mojo)
    
