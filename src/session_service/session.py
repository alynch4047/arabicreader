
import logging

from traits.api import HasTraits, Str, Bool, Int, Instance

from server.api import set_cookie_data, get_cookie_data


l = logging.getLogger(__name__)

MIN_GUEST_ID = 1000000
MAX_GUEST_ID = 9999999


class Session(HasTraits):

    user_id = Int

    password_hash = Str

    authenticated = Bool(False)

    email_address = Str

    nickname = Str

    sql_database = Instance('dictionary_service.sql_database.sql_database.SQLDatabase')
    
    def __init__(self, **traits):
        HasTraits.__init__(self, **traits)
        
        set_cookie_data('user_id', self.user_id)
        set_cookie_data('password_hash', self.password_hash)
        
        if self.is_guest():
            self.nickname = 'Guest' + str(self.user_id)[-3:]
        else:
            self.nickname = self._get_nickname(self.user_id)
        l.debug('nickname is %s', self.nickname)
        set_cookie_data('nickname', self.nickname)
        
    def is_guest(self):
        return self.user_id >= MIN_GUEST_ID
        
    def check_password(self):
        """ Check that the cookie password is the same as the database
        password. Update self.authenticated accordingly"""
        l.debug('check password for user %s', self.user_id)
        self.authenticated = False
        user_details = self.sql_database.get_user_details(self.user_id)
        if user_details is None:
            return
        else:
            db_password_hash = user_details['password_hash']
            cookie_password_hash = get_cookie_data('password_hash')
            if db_password_hash == cookie_password_hash:
                l.debug('user has been authenticated')
                self.authenticated = True
    
    def _get_nickname(self, user_id):
        if self.sql_database is None:
            return ''
        user_details = self.sql_database.get_user_details(self.user_id)
        if user_details is None:
            return ''
        else:
            return user_details['nickname']


