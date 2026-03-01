
import logging
import datetime
import cherrypy

from transactions.transaction_queue import TransactionQueue

from traits.api import HasTraits, Str, Instance

l = logging.getLogger(__name__)

INSERT_SQL = \
"""
insert into log 
(ip_address, request_timestamp, url, message, word, user_id, nickname, service, user_agent)
values
(%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


class DBLogger(HasTraits):
    
    service = Str
    
    transaction_queue = Instance(TransactionQueue, ())
    
    def log(self, session, message, word=None):
        headers = cherrypy.request.headers
        # when behind proxy...
        ip_address = headers.get('X-Forwarded-For') 
        #ip_address = headers['Remote-Addr']
        user_agent = headers['User-Agent']
        time_now = datetime.datetime.now()
        user_id = session.user_id
        nickname = session.nickname
        
        if ip_address is None:
            ip_address = '127.0.0.1'
        
        bind_vars = (ip_address, time_now, '', message, word, user_id, nickname,
                     self.service, user_agent)
        
        self.transaction_queue.add(INSERT_SQL, bind_vars)
        
        