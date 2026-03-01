
import cherrypy

import logging

l = logging.getLogger(__name__)

def set_cookie_data(key, value):
    l.debug('set cookie %s to %s', key, value)
    cookie = cherrypy.response.cookie
    cookie[key] = value
    cookie[key]['path'] = '/'
    cookie[key]['max-age'] = 500*24*60*60 # 500 days
    cookie[key]['version'] = 1
    
def delete_cookie(key):
    cherrypy.response.cookie[key]['expires'] = 0
    
def get_cookie_data(key):
    if key in cherrypy.request.cookie:
        return cherrypy.request.cookie[key].value
    else:
        return None