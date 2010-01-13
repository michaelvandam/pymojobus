import time
import logging
import model.experiment
from threading import Event
from model.experiment import Session
from model.experiment.commandmessage import CommandMessage

RECORDING = Event()



log = logging.getLogger()
recorderLog = logging.getLogger("mojo.recorder")

def turnRecordingOff():
    global RECORDING
    RECORDING.clear()
    
def turnRecordingOn():
    global RECORDING
    RECORDING.set()


def MojoRecorder(fxn):
        def new(self, command, param):
            global RECORDING
            if RECORDING.isSet():
                cmdmsg = CommandMessage(command, param, self.deviceType, self.address)
                session = Session()
                session.add(cmdmsg)
                session.commit()
                recorderLog.info("Command: %s" % command)
                recorderLog.info("Param: %s" % str(param))
                recorderLog.info("Device: %s" % self)
                recorderLog.info("Address: %s" % self.address)
                recorderLog.info("Type: %s" % self.deviceType)
                
            return fxn(self, command, param)
        return new