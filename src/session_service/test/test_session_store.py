
import ar_logging
import unittest

from session_service.session_store import SessionStore


class TestSessionStore(unittest.TestCase):
        
    def test_session_store(self):
        session_store = SessionStore()
        session_store.add_session(1, 'password')
        session = session_store.sessions['1']
        self.assertEquals(session.password_hash, 'password')
        

        

        
