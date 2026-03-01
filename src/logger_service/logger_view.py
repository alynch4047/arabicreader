# -*- coding: utf-8 -*-

import logging

from traits.api import HasTraits

l = logging.getLogger(__name__)

DETAILS_SQL = \
"""
SELECT 
ip_address, request_timestamp, url,
word, message, user_id, nickname, service, user_agent
FROM LOG
WHERE DATE_PART('year', request_timestamp) = 2009
ORDER BY nickname, request_timestamp
"""

class LoggerView(HasTraits):
    
    def details(self, data, session):
       return 'Not implemented'
        