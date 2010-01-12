# mojomessages.py 
# Classes for parsing received messages and creating messages for transport on the bus

# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!

import re
from mojoerrors import *
from mojoconfig import config

#ENDCHAR = '\r'
ENDCHAR = '$'

    
class MojoCommand(object):
    def __init__(self, cmdStr=None, cmd=None, param=None):
        self.cmdStr=cmdStr
        self.cmd=cmd
        self.param=param
        
        if not self.cmdStr is None:
            self.__parseCmd()
            
    
    def __parseCmd(self):  
        #print self.cmdStr
        tmp = self.cmdStr.split(config['MojoSettings']['paramSep'])
        self.cmd = tmp[0]
        try:
            self.param = tmp[1]
        except IndexError:  
            self.param = None     
        
    def __str__(self):
        s = self.cmd
        if self.param:
            s+= config['MojoSettings']['paramSep'] + self.param
        return s
    
    def __eq__(self, other):
        return self.cmd.replace("*","") == other.cmd.replace("*","")
            
    
    def __repr__(self):
        return 'MojoCommand("%s")' % self.cmdStr
    
class MojoCommands(list):
    def __init__(self, cmdsStr=None):
        self.cmdsStr = cmdsStr
        
        if not cmdsStr is None:
            self.__parseCommands()
        
    def __parseCommands(self):
        self.extend([MojoCommand(cmd) for cmd in self.cmdsStr.split(config['MojoSettings']['commandSep']) if not cmd == ""])
    

    def __str__(self):
        return config['MojoSettings']['commandSep'].join([str(cmd) for cmd in self])
    
    def __repr__(self):
        return 'MojoCommand("%s")' % self.cmdsStr
    
class MojoAddress(object):
    def __init__(self, addrStr=None, sender=None, receiver=None):
        self.sender=sender
        self.receiver=receiver
        self.addrStr = addrStr
        
        if not addrStr is None:
            self.__parseAddress()
    
    def __parseAddress(self):
        s = re.compile("^(?P<senderAddress>[\w\d])%(addressSep2)s(?P<receiverAddress>[\w\d]$)" % config['MojoSettings'])
        p = s.search(self.addrStr)
        if p:
            self.receiver = p.group('senderAddress')
            self.sender = p.group('receiverAddress')
        else:
            raise MojoInvalidAddress, "Message has improper address syntax" 
    
    def swap(self):
        self.receiver, self.sender = self.sender, self.receiver
        
    def __str__(self):
        return self.receiver + config['MojoSettings']['addressSep2'] + self.sender
        
    def __repr__(self):
        return 'MojoAddress("%s")' % self.addrStr
        

class MojoMessage(object):
    def __init__(self):
        self.cmds = MojoCommands()
        self.address = MojoAddress()

    def parseMsgStr(self):
        s =  re.compile("%(startChar)s%(startChar)s(?P<address>[\w,]+)%(addressSep)s(?P<commands>[\w\d\s;,=*-.?]+)" % config['MojoSettings'])
        p = s.search(self.msgStr)
        if p:
            self.__parseAddress(p.group('address'))
            self.__parseCommands(p.group('commands'))
        else:
            raise MojoInvalidMessage("Message is invalid, could not locate address or commands (MSG: %s)" % self.msgStr)
            
    def __parseCommands(self, cmdsStr):
        self.cmds = MojoCommands(cmdsStr)
        
    def __parseAddress(self, addrStr):
        self.address = MojoAddress(addrStr)
    
    def __checkAddress(self, address):
        if len(address) != 3:
            raise MojoInvalidAddress, "Message has improper address syntax"
        if address[1]!=config['MojoSettings']['addressSep2']:
            raise MojoInvalidAddress, "Message address missing separator"
    
    def __generateMsgStr(self):
        return config['MojoSettings']['startChar'] * 2 + str(self.address) + \
                config['MojoSettings']['addressSep'] + str(self.cmds) + ENDCHAR
    
    def __str__(self):
        return self.__generateMsgStr()
    
    def __eq__(self, other):
        if self.cmds == other.cmds:
            return True
        else:
            return False
    
    def clearCommands(self):
        self.cmds = MojoCommands()
        
class MojoSendMessage(MojoMessage):

    def __init__(self, address):
        MojoMessage.__init__(self)
        self.address=address
        
    def addCommand(self, cmd, param=None):
        c = MojoCommand(cmd=cmd,param=param)
        self.cmds.append(c)
        
    def __repr__(self):
        return 'MojoSendMessage("%s")' % str(self).strip()

        
class MojoReceivedMessage(MojoMessage):

    def __init__(self, msgStr):
        self.msgStr = msgStr.strip()
        self.parseMsgStr()
    
    def __repr__(self):
        return 'MojoReceivedMessage("%s")' % self.msgStr
    
    

    
