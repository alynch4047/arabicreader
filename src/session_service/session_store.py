
import logging
import threading

from traits.api import HasTraits, Dict, Instance

from dictionary_service.api import SQLDatabase

l = logging.getLogger(__name__)
_lock = threading.Lock()


class SessionStore(HasTraits):
    
    sessions = Dict  # user_id -> session
    
    sql_database = Instance(SQLDatabase)
    
    def add_session(self, user_id, password_hash):
        _lock.acquire()
        session = None
        try:
            from session_service.session import Session
            session = Session(user_id=user_id, password_hash=password_hash,
                              sql_database=self.sql_database)
            l.debug('add session for %s to store %s', user_id, id(self))
            self.sessions[str(user_id)] = session
        finally:
            _lock.release()
        return session
    
    def get_session(self, user_id):
        """ If the session for that user_id is already in sessions then return
        that, else create a new session for that user_id if it is a valid id,
        else return None"""
    
        if user_id in self.sessions:
            return self.sessions[user_id]
        else:
            user_details = self.sql_database.get_user_details(user_id)
            l.debug('user details are %s', user_details)
            if user_details:
                return self.add_session(user_details['user_id'],
                                        user_details['password_hash'])
            else:
                return None
            

            