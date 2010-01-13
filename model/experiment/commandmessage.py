from sqlalchemy import Table, Column, Integer, String, PickleType, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CommandMessage(Base):
    __tablename__= 'cmdmessages'
    
    id = Column(Integer, primary_key=True)
    command = Column(String)
    deviceType = Column(String)
    deviceAddress = Column(String)
    param = Column(PickleType)
    
    def __init__(self, command, param, deviceType, deviceAddress):
        self.command=command
        self.deviceType = deviceType
        self.deviceAddress = deviceAddress
        self.param = param

    def __repr__(self):
        return "<Message('%s','%s','%s','%s')>" % (self.command, self.param, self.deviceType, self.deviceAddress)

