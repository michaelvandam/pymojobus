# mojoqueues.py 
# Response and Outbound message queues

# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!


import Queue
import logging

log = logging.getLogger()


log.debug("Creating outbound message queue and response queue")

responses = Queue.Queue()
outboundMessages = Queue.Queue()