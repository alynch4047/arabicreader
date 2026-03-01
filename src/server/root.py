
import logging
import cherrypy
import simplejson
import urllib
import random

random.seed()

from server import configuration
from server.handlers import handlers_factory
from server.server_output import server_out
from server.cookies import get_cookie_data

logger = logging.getLogger(__name__)


class Root(object):
    
    exposed = True
    
    def __init__(self):
        self.handlers, self.session_store = handlers_factory()
        
    def _remove_cache_buster(self, url):
        if url.endswith('cb'):
            return '_'.join(url.split('_')[:-1])
        else:
            return url
        
    def _get_handler_for_url(self, path):
        if path[0] == 'services':
            path = path[1:]
        if path[0] not in self.handlers:
            raise cherrypy.NotFound('Invalid Service Name for URL %s' % repr(path))
        
        handler = self.handlers[path[0]]()
        URL = '/'.join(path[1:])
        return handler, URL
    
    def _get_use_json(self, url):
        """ Find the 'json' flag in the URL and remove it if it is found """
        use_json = False
        if url.endswith('/json'): 
            url = url[:-5]
            use_json = True
        elif url.find('/json?') != -1:
            loc = url.find('/json?')
            url = url[:loc] + url[loc+5:]
            use_json = True
        return url, use_json
    
    def GET(self, *path, **kwargs):
#        logger.debug('mem is %s', mem())
        if len(path) == 0:
            return 'Welcome to Arabic Reader'
            
        handler, url = self._get_handler_for_url(path)
        
        url = self._remove_cache_buster(url)
        url, use_json = self._get_use_json(url)

        if kwargs:
            for key, value in kwargs.iteritems():
                kwargs[key] = self._remove_cache_buster(value)
                    
        resp = self._get(handler, url, use_json, **kwargs)
#        logger.debug('mem 2 is %s', mem())
        return resp
        
    def POST(self, *path, **kwargs):
        if len(path) == 0:
            return 'Welcome to Arabic Reader'
        
        handler, url = self._get_handler_for_url(path)
        
        url, use_json = self._get_use_json(url)
        handler, url = self._get_handler_for_url(path)
        
        for key, value in kwargs.items():
            if key == 'post_data':
                # AJAX requests send their post data like this
                assert(len(kwargs) == 1)
                kwargs_unicode_keys = simplejson.loads(value)
                kwargs = {}
                for key, value in kwargs_unicode_keys.items():
                    # convert key to str
                    kwargs[str(key)] = value
            
        return self._post(handler, url, use_json, **kwargs)
        
    def _unquote(self, url):
        url = urllib.unquote(url)
        url = url.replace('\n','')
        url = url.replace('\t','')
        url = url.replace('\r','')
        return url
    
    def _get(self, handler, url, use_json, **kwargs):
        #logger.debug('GET: %s from %s', url, self.__class__.__name__)
        try:
            #logger.debug('quoted url is %s', url)
            url = self._unquote(url)
            for key, value in kwargs.iteritems():
                value = self._unquote(value)
                kwargs[key] = unicode(value, encoding='utf-8')
            url = unicode(url, encoding='utf-8')
            #logger.debug('unquoted url is %s', url)
            session = self._get_session()
            #logger.debug('get data for session %s', session)
            return server_out(handler.get_url(url, use_json, session=session, **kwargs))
        except Exception, ex:
            logger.exception('processing service')
            
    def _post(self, handler, url, use_json, **kwargs):
        try:
            #logger.debug('quoted url is %s', url)
            url = self._unquote(url)
            url = unicode(url, encoding='utf-8')
            #logger.debug('unquoted url is %s', url)
            session = self._get_session()
            url, use_json = self._get_use_json(url)
            #logger.debug('get data for session %s', session)
            return server_out(handler.get_url(url, use_json, session=session, **kwargs))
        except Exception, ex:
            logger.exception('processing service')
            
    def _get_session(self):
        from session_service.api import MIN_GUEST_ID, MAX_GUEST_ID
        user_id = get_cookie_data('user_id')
        logger.debug('cookie user_id is %s', user_id)
        session = self.session_store.get_session(user_id)
        if not session:
            # invent username and create session
            user_id =  random.randrange(MIN_GUEST_ID, MAX_GUEST_ID)
            logger.debug('create session with user_id %s', user_id)
            session = self.session_store.add_session(user_id, password_hash='anonymous')
        else:
            session.check_password()
            
        if configuration.session_always_authenticated:
            session.authenticated = True
            session.user_id = 1
            session.nickname = 'alynch'
            
        return session
