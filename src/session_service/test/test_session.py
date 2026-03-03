
import ar_logging
import unittest

from session_service.session import Session


class TestSession(unittest.TestCase):
        
    def test_session(self):
        session = Session(user_id=1, password_hash='patience')

        self.assertEquals(session.user_id, 1)
        self.assertEquals(session.password_hash, 'patience')
        self.assertEquals(session.nickname, '')
