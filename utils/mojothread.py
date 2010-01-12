import sys
import threading
from threading import Thread, Event

class MojoThread(Thread):
    incomingMessage = Event()
    def __init__(self):
        Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()