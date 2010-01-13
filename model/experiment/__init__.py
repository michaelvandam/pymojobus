from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from commandmessage import CommandMessage


engine = create_engine('sqlite:///arc-p.db',echo=True)
CommandMessage.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()