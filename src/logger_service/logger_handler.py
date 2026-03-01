
import logging

from traits.api import Instance

from server.api import Handler

from dictionary_service.api import SQLDatabase

from logger_service.logger_view import LoggerView

l = logging.getLogger(__name__)


class LoggerHandler(Handler):
    
    logger_view = Instance(LoggerView)
    
    sql_database = Instance(SQLDatabase)
    
    def _url_lookup_default(self):
        lookup = {
                  'details': self._details,
        }
        return lookup
    
    def _details(self, data, session):
        return self.logger_view.details(data, session)
    
    def _logger_view_default(self):
        return LoggerView(sql_database=self.sql_database)
