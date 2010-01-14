from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbmodel import CommandMessage,Sequence
from utils.mojoconfig import config

defaultdb = config['Sequence']['file']

def generateEngine(dbfile = defaultdb):
    engine = create_engine('sqlite:///%s' % dbfile, echo=True)
    CommandMessage.metadata.create_all(engine)
    Sequence.metadata.create_all(engine)
    return engine

def generateSession(engine):
    Session = sessionmaker(bind=engine)
    return Session