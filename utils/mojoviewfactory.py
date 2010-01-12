from mojoerrors import * 
from mojomessages import MojoReceivedMessage, MojoSendMessage, MojoAddress
from mojoconfig import config
import time
import logging

log = logging.getLogger()

def mojoViewFactory( devices, deviceViewTypes):
    deviceViews = {}
    for device in devices.values():
        deviceViews[device.address] = deviceViewTypes[device.deviceType](device)
        
    return deviceViews