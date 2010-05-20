#!/usr/bin/env python
import time
import sys
import os
from mojo import Mojo, deviceTypes
from utils.mojoconfig import config





def coolOff(prm,tempHigh):
    prm.goGetTemp()
    time.sleep(1)
    while(prm.reactorTemperature > tempHigh):
                if prm.reactorTemperature > tempHigh:
                    prm.goCoolOn()
                    time.sleep(1)
                    prm.goHeaterOff()
                    time.sleep(1)
                    prm.goGetTemp()
                    time.sleep(1)
                print "Waiting for temp to get below %f" % tempHigh
                time.sleep(5)
    else:
        print "Temp has dropped"
        time.sleep(1)
        prm.goCoolOff()
    
def heatProfile(finalTemp, prm, duration):
    time.sleep(1)
    prm.goGetTemp()
    time.sleep(1)
    print "Temp setpoint: %f" % finalTemp
    prm.goSetpoint(finalTemp)
    time.sleep(1)
    prm.goHeaterOn()
    print "Waiting 15 minutes"
    time.sleep(60*duration)
    print "Turing cooling on and heater off"
    prm.goSetpoint(30.0)
    time.sleep(1)
    prm.goHeaterOff()
    time.sleep(1)
    prm.goCoolOn()
    time.sleep(1)
    prm.goGetTemp()
    time.sleep(1)
    
    

if __name__ == "__main__":
    temps = [100,125,135]#range(175,265,10)
    mojo=Mojo()
    mojo.makeConnection(config)
    time.sleep(2)
    devices = mojo.getDevices()
    mojo.stopDeviceUpdating()
    prms = [prm for prm in mojo.devices.values() if prm.deviceType == "PRM"]
    
    
    for prm in prms:
        count = 0
        for temp in temps:
            prm.goMoveZUp()
            time.sleep(5)
            coolOff(prm,30.0)
            if count % 5 == 0:
                raw_input("Pause for thermocouple datalogger reset")
            time.sleep(1)
            heatProfile(temp, prm, 25)
            count = count+1
        time.sleep(1)
        coolOff(prm,30.0)
        time.sleep(1)
        prm.goHeaterOff()
        
        