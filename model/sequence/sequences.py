#!/usr/bin/env python

import setupdb
from setupdb import generateEngine, generateSession
from utils.mojoconfig import config
import tempfile
import os

defaultdb = config['Sequence']['file']

class Sequences(object):
    def __init__(self, filepath=None, openPrevious=True):
        
        if openPrevious==True:
            if os.path.exists(defaultdb):
                self.filepath = defaultdb
                print "Should not run"
            else:
                self.generateNewDbName()
        else:
            if filepath is None or filepath == "":
                self.generateNewDbName()
        
        self.engine = generateEngine(self.filepath)
        self.Session = generateSession(self.engine)
        
    
    def generateNewDbName(self):
        self.filepath = tempfile.mktemp(suffix=".db", prefix="ARCSeq",dir=os.path.curdir)
        config['Sequence']['file'] = self.filepath
        config.write()
    
    def loadDb(self, filepath):
        sess = self.Session()
        sess.close_all()
        self.engine.dispose()
        self.engine = generateEngine(filepath)
        self.Session = generateSession(self.engine)
        config['Sequence']['file'] = filepath
        config.write()
    
sequences = Sequences()

