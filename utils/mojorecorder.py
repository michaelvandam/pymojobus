import time
import logging

log = logging.getLogger()
recorderLog = logging.getLogger("mojo.recorder")


def MojoRecorder(command):
    def wrapper(f):
        def new(self, *args, **kws):
            recorderLog.info("Command: %s" % command)
            recorderLog.info("Device: %s" % self)
            recorderLog.info("Address: %s" % self.address)
            recorderLog.info("Type: %s" % self.deviceType)
            return f(self, *args, **kws)
        return new
    return wrapper