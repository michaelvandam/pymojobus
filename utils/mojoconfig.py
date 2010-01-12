# mojoconfig.py 
# Reads config file

# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!

from configobj import ConfigObj
from validate import Validator
from mojoerrors import *
import logging

log = logging.getLogger()

log.debug("Loading Config")
config = ConfigObj("config\mojoconfig.ini", configspec="config\mojoconfigspec.ini")

log.debug("Validating Config")
validator = Validator()

result = config.validate(validator)

if result!=True:
    log.error("Validation failed")
    raise MojoInvalidConfig("Could not validate config")


serialConfig = config["SerialSettings"]
masterAddress = config['MojoSettings']['masteraddress']

