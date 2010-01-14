#!/usr/bin/env python

from setupdb import Session
from commandmessage import CommandMessage
from sqlalchemy import desc
import datetime

def getDuration():
    sess = Session()
    d = sess.query(CommandMessage.created).order_by(desc(CommandMessage.created)).first().created
    return d