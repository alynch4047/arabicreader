
import logging
import threading
import time

import cherrypy

from session_service.email import send_email
from server.memory import mem

MAX_MEMORY = 512 #megabytes

l = logging.getLogger(__name__)

memory_monitor = None

def start_memory_monitor():
    global memory_monitor
    if not memory_monitor:
        l.debug('starting memory monitor')
        memory_monitor = MemoryMonitor()
        memory_monitor.setDaemon(True)
        memory_monitor.start()
    else:
        l.debug('not starting memory monitor - still exists')
    
def stop_memory_monitor():
    l.debug('stopping memory monitor')
    global memory_monitor
    memory_monitor.stop()
    memory_monitor = None
    

class MemoryMonitor(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = False
    
    def run(self):
        while not self._stop:
            time.sleep(180)
            memory = mem()
            l.debug('memory is %s', memory)
            if memory > (MAX_MEMORY*1000):
                self._restart_engine(memory)
                break
        l.debug('exiting memory monitor')
            
    def stop(self):
        l.debug('stop memory monitor')
        global memory_monitor
        self._stop = True
        memory_monitor = None
            
    def _restart_engine(self, memory):
        l.debug('restarting engine in 10 seconds because memory is %s', memory)
        time.sleep(10)
        cherrypy.engine.restart()
        l.debug('engine restarted')
        try:
            send_email('alynch4047@googlemail.com',
                   'restarted arabicreader because memory is %s' % memory,
                   'restarted arabicreader' )
        except:
            l.error('sending restarted email failed')
        l.debug('queue relaunch of memory monitor')
        