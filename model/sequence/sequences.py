#!/usr/bin/env python

import setupdb
from setupdb import generateEngine, generateSession
from utils.mojoconfig import config
from dbmodel import Sequence, CommandMessage
import tempfile
import os

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import desc, asc

defaultdb = config['Sequence']['file']

class Sequences(object):
    def __init__(self, filepath=None, openPrevious=True):
        
        if openPrevious==True:
            if os.path.exists(defaultdb):
                self.filepath = defaultdb
            else:
                self.generateNewDbName()
        else:
            if filepath is None or filepath == "":
                self.generateNewDbName()
        
        self.engine = generateEngine(self.filepath)
        self.Session = generateSession(self.engine)
        self.loadDb()
        
    
    def generateNewDbName(self):
        self.filepath = tempfile.mktemp(suffix=".db", prefix="ARCSeq",dir=os.path.curdir)
        config['Sequence']['file'] = self.filepath
        config.write()
    
    def createOrLoadLastSequence(self):
        sess = self.Session()
        lastSequenceName = config['Sequence']['lastsequence']
        sess = self.Session()
        q = sess.query(Sequence).filter(Sequence.name == lastSequenceName)
        try:
            self._selectedSequence = q.one()
            print self._selectedSequence.name
            config['Sequence']['lastsequence'] = self._selectedSequence.name
            config.write()
            
        except (MultipleResultsFound, NoResultFound):
            self.createDefaultSequence()
    
    def createDefaultSequence(self):
        sess = self.Session()
        defaultSequenceName = config['Sequence']['defaultname']
        sess = self.Session()
        q = sess.query(Sequence).filter(Sequence.name == defaultSequenceName)
        try:
            self._selectedSequence = q.one()
            self.loadSequence(self._selectedSequence.name)
            
            config['Sequence']['lastsequence'] = self._selectedSequence.name
            config.write()
            
        except (MultipleResultsFound, NoResultFound):
            self.createAndLoadSequence(defaultSequenceName)
    
    def createAndLoadSequence(self, sequenceName, authorName = config['Sequence']['defaultauthor']):
        sess = self.Session()
        self._selectedSequence = Sequence(sequenceName, authorName)
        sess.add(self._selectedSequence)
        sess.commit()
        config['Sequence']['lastsequence'] = self._selectedSequence.name
        config.write()
    
    def loadSequence(self, sequenceName):
        sess = self.Session()
        q = sess.query(Sequence).filter(Sequence.name == sequenceName)
        try:
            self._selectedSequence = q.one()
            config['Sequence']['lastsequence'] = self._selectedSequence.name
            config.write()
            
        except (MultipleResultsFound, NoResultFound):
            self.createOrLoadLastSequence()
        
        
    
    def getSelectedSequence(self, sess):
        return sess.query(Sequence).filter(Sequence.id == self._selectedSequence.id).one()
    

    def loadDb(self, filepath = config['Sequence']['file']):
        sess = self.Session()
        sess.close_all()
        self.engine.dispose()
        self.engine = generateEngine(filepath)
        self.Session = generateSession(self.engine)
        config['Sequence']['file'] = filepath
        self.filepath = filepath
        self.createOrLoadLastSequence()
        config.write()
    
    def deleteSelectedSequence(self):
        sess = self.Session()
        seq = self.getSelectedSequence(sess)
        seq.visible=False
        sess.commit()
        
    def getSequences(self, sess):
        return sess.query(Sequence).filter(Sequence.visible==True).all()
    
    def getCommandsInSequence(self):
        sess = self.Session()
        seq = self.getSelectedSequence(sess)
        return seq.commands
    
sequences = Sequences()

