#!/usr/bin/env python
import time
import sys
import os
from mojo import Mojo, deviceTypes
from utils.mojoconfig import config


temps = [(215,155),(215,150),(215,145),(215,140),(215,135)]

def heaterOnDuration(targetTemp):
    A = 0.0001
    B = -0.0318
    C = 3.0926
    D = -60.895
    
    t = A * targetTemp**3 + B* targetTemp**2 + C*targetTemp + D
    return t

def getToTemp(prm, temp):
    t = heaterOnDuration(temp)
    prm.goHeaterMax()
    time.sleep(t)
    prm.goHeaterOff()
    
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
    
def heatProfile(onTime, finalTemp, prm):
    print "Ramping heater for %d" % onTime
    prm.goHeaterMax()
    time.sleep(onTime) #Heater Rise Time
    prm.goGetTemp()
    time.sleep(1)
    print "Attempting to level off temperature %f" % finalTemp
    prm.goSetpoint(finalTemp)
    time.sleep(1)
    prm.goHeaterOn()
    print "Waiting 15 minutes"
    time.sleep(60*15)
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
    mojo=Mojo()
    mojo.makeConnection(config)
    time.sleep(2)
    devices = mojo.getDevices()
    mojo.stopDeviceUpdating()
    prms = [prm for prm in mojo.devices.values() if prm.deviceType == "PRM"]
    
    
    for prm in prms:
        try:
            for temp in temps:
                prm.goMoveZUp()
                time.sleep(5)
                coolOff(prm,30.0)
                time.sleep(1)
                heatProfile(temp[1], temp[0], prm)
            time.sleep(1)
            coolOff(prm,30.0)
            time.sleep(1)
            prm.goHeaterOff()
        except:
            print "Error occured! Cool off!"
            prm.goHeaterOff()
            time.sleep(1)
            coolOff(prm,30.0)