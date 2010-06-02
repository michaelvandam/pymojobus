import cherrypy
from mojo import Mojo, config
from mako.template import Template
from mako.lookup import TemplateLookup
import time

lookup = TemplateLookup(directories=['view/deviceviewswww'])


class Devices(object):
    def __init__(self, mojo):
        self.mojo = mojo
    def index(self):
        return str(self.mojo.devices)
    index.exposed=True
    
    def default(self, deviceKey):
        try:
            device = mojo.devices[deviceKey]
            template = lookup.get_template("prm.mako")
            return template.render(prm=device)
        except KeyError:
            return "None"
    default.exposed=True
    
class HelloWorld(object):
    def __init__(self, mojo):
        self.mojo = mojo
        self.devices = Devices(mojo)
        
    def index(self):
        return str(self.mojo.devices)
    index.exposed = True
    
def startweb(mojo):
    cherrypy.quickstart(HelloWorld(mojo))
    
if __name__ == '__main__':
    mojo = Mojo()
    mojo.makeConnection(config)
    time.sleep(2)
    devices = mojo.getDevices()
    #mojo.stopDeviceUpdating()
    startweb(mojo)
    