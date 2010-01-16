from sqlalchemy import Table, Column, Integer, String, Boolean, \
                        DateTime, PickleType, MetaData, ForeignKey
from sqlalchemy import asc, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, backref

import datetime

Base = declarative_base()

class Sequence(Base):
    __tablename__= 'sequences'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    requiredDevices = Column(PickleType)
    visible = Column(Boolean, default=True)
    
    def __init__(self, name, author):
        self.name=name
        self.author = author

    def __repr__(self):
        return "<Sequence('%s','%s')>" % (self.name, self.author)



class CommandMessage(Base):
    __tablename__= 'cmdmessages'
    
    id = Column(Integer, primary_key=True)
    command = Column(String)
    deviceType = Column(String)
    deviceAddress = Column(String)
    param = Column(PickleType)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)
    duration = Column(PickleType)
    sequence_id = Column(Integer, ForeignKey("sequences.id"))
    sequence = relation(Sequence, backref=backref("sequences", order_by=id))
    
    
    def __init__(self, command, param, deviceType, deviceAddress):
        self.command=command
        self.deviceType = deviceType
        self.deviceAddress = deviceAddress
        self.param = param

    def __repr__(self):
        return "<Message('%d','%s','%s','%s','%s')>" % (self.id, self.command, self.param,
                                                        self.deviceType, self.deviceAddress)

    def setDuration(self,sess):
        lastEntry = sess.query(CommandMessage).order_by(desc(CommandMessage.created)).first()
        if lastEntry:
            lastEntryDts = lastEntry.created
            lastEntry.duration = datetime.datetime.now() - lastEntryDts
            #print "%s" % (lastEntry.duration)
            #print"*******Last***********"
            #print repr(lastEntry)
            #print "****** Duration *******"
            #print "%s" % (lastEntry.duration)
            sess.commit()
        else:
            pass
        
        self.duration = datetime.timedelta(0)
        sess.commit()

    def durationInSeconds(self):
        return self.duration.seconds+self.duration.days*24*60*60+self.duration.microseconds/1000000.

    delay = property(fget=durationInSeconds)

