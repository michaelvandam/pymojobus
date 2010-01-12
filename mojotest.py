import time
from model import deviceTypes
from utils.mojoconn import ConnectionFactory
from utils.mojoconfig import config
from utils.mojodevicefactory import MojoDeviceFactory
from utils import mojologger

log = mojologger.logging.getLogger()

log.info("*BEGIN MOJO*")

def main():
    pass

if __name__=='__main__':
    config['SerialSettings']['port']=9
    conn = ConnectionFactory(config)
    factory = MojoDeviceFactory(conn)
    time.sleep(2)
    devices = factory.enumerateDevices()
    conn.startMonitor(devices)