
import logging
import sys

import cherrypy

from traits.api import HasTraits, Instance

from server.api import Handler
from dictionary_service.api import disconnect

from server.memory import mem
from server.memory_monitor import start_memory_monitor, stop_memory_monitor

l = logging.getLogger(__name__)


class ControlHandler(Handler):
    
    def _url_lookup_default(self):
        lookup = {
                  'stop': self._stop,
                  'restart': self._restart,
                  'status': self._status,
        }
        return lookup
    
    def _stop(self, data, session=None):
        disconnect()
        sys.exit(0)
        
    def _restart(self, data, session=None):
        l.debug('restarting engine...')
        stop_memory_monitor()
        cherrypy.engine.restart()
        l.debug('restarted')
        start_memory_monitor()
        
    def _status(self, data, session=None):
        memory = mem()
        return \
"""
<html>
<body>
<p>
RSS Memory: %s
</p>
</body>
</html>""" % memory
            

   