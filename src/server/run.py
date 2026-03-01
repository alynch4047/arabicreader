
import os
import logging
import cherrypy

import ar_logging
ar_logging.add_std_out()

from server import configuration
from server.root import Root
from server.memory_monitor import start_memory_monitor

logger = logging.getLogger(__name__)

        
def run():
    
    # Site-wide (global) config
    cherrypy.config.update({'server.socket_host':  '0.0.0.0',
                            'server.socket_port':  configuration.port,
                        })
        
    # application config
    root = Root()
    
    dispatcher = cherrypy.dispatch.MethodDispatcher()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, '../static')
    apps_dir = os.path.join(static_dir, 'applications')
    third_party_dir = os.path.join(current_dir, '../third_party')
    
    config = {
             '/'            : {
                              #'environment'            : 'production',
                              'request.dispatch'       : dispatcher,
                              #'tools.sessions.on'      : True,
                              #'tools.sessions.timeout' : 60,
                              #'tools.staticdir.root'   : apps_dir
                             },
             '/static'       : {'tools.staticdir.on'     : True,
                                'tools.staticdir.dir'    : static_dir,
                             },
             '/third_party'  : {'tools.staticdir.on': True,
                                'tools.staticdir.dir'    : third_party_dir
                             },
             '/proxy'        : {'tools.encode.on':True,
                                'tools.encode.encoding':'utf8', 
                               }
            }
    
    ar_logging.remove_std_out()
    
    start_memory_monitor()
    
    cherrypy.tree.mount(root, "/", config)
    cherrypy.engine.start() 
    cherrypy.engine.block()
    
