# mojologger.py 
# Reads in the mojologconfig.ini to configure three loggers
# 1 logger for messages
# 1 logger for errors
# 1 root logger

# Copyright (C) 2009 UC Regents
# Author: Henry Herman
# Email: hherman@mednet.ucla.edu
# 
# PyMojobus
# http://code.google.com/p/pymojobus/
# Released Subject to the BSD License
# Comments and Suggestion welcome!

from mojoconfig import config
import logging.config

logging.config.fileConfig(config['Logging']['logconfigpath'])

