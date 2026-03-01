
import ar_logging
import unittest


from session_service.session_store import SessionStore
from session_service.session_handler import SessionHandler


class TestSessionHandler(unittest.TestCase):
    
    def setUp(self):
        session_store = SessionStore()
        self.session_handler = SessionHandler(session_store=session_store)
        
    def test_make_password(self):
        password = self.session_handler._make_password()
        print password
        self.assert_(len(password), 6)
        
    def test_register(self):
        pass
        #self.session_handler._add_user('a1@gmail.com', 'pt1', 'nick1')
        


