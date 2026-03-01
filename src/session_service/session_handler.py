
import logging
import random
import smtplib
import hashlib
import pickle

from traits.api import Instance

from dictionary_service.api import SQLDatabase
from server.api import Handler
from server.memory import mem

from session_service.email import send_email
from session_service.session_store import SessionStore

ERROR_EMAIL_ALREADY_IN_USE = 'ERROR_EMAIL_ALREADY_IN_USE'

l = logging.getLogger(__name__)


class SessionHandler(Handler):
    
    session_store = Instance(SessionStore)
    
    sql_database = Instance(SQLDatabase)
    
    def _url_lookup_default(self):
        lookup = {
                  'logon': self._logon,
                  'signup': self._signup,
                  'change_password': self._change_password,
                  'deregister': self._deregister,
                  'reset_password': self._reset_password,
                  'session_info': self._session_info,
                  'get_preferences': self._get_preferences,
                  'set_preferences': self._set_preferences,
                  
        }
        return lookup
    
    def _session_info(self, data, session):
        l.debug('mem A %s', mem())
        user_details = self.sql_database.get_user_details(session.user_id)
        email_address = user_details['email_address']
        nickname = user_details['nickname']

        num_words_added = self.sql_database.get_vocabulary_count(session.user_id)
        return email_address, nickname, num_words_added
    
    def _logon(self, data, session):
        try:
            email_address, password_hash = data.split('/')
        except Exception:
            raise Exception('You must enter the username and password.')
        user_id, db_password_hash = self._get_user_details_for_email_address(email_address)
        if user_id is None:
            raise Exception("Sorry - that username is not recognised.")
        else:
            l.debug('user id is %s', user_id)
            if db_password_hash != password_hash:
                l.debug('%s != %s',db_password_hash, password_hash)
                raise Exception("Sorry - the password is incorrect.")
            session = self.session_store.add_session(user_id, password_hash)
            return ''
        
    def _reset_password(self, data, session):
        email_address = data;
        if not self._email_already_registered(email_address):
            raise Exception("Sorry - that email address (%s) is not recognised." % email_address)
        user_id, old_password_hash = self._get_user_details_for_email_address(email_address)
        password = self._make_password()
        password_hash = self._hash_password(password)
        l.debug('password hash is %s', password_hash)
        l.debug('reset password is %s', password)
        self.sql_database.set_password_hash(user_id, password_hash)
        message = \
"""

Your ArabicReader password has been reset to %s.

After logging on with your new password you can then change it to the password you
prefer by going to the My Reader section and clikcing on Change Password.

regards

Abdulhaq
Administrator
""" % password
      
        send_email(email_address, message, 'Your ArabicReader password has been reset')
        return ''
    
    def _get_preferences(self, data, session):
        if not session.authenticated:
            raise Exception('Cannot get preferences - you must log on first.')
        user_details = self.sql_database.get_user_details(session.user_id)
        if user_details is not None and user_details['preferences_pickle'] is not None :
            pickle_data = user_details['preferences_pickle']
            l.debug('user prefs pickle data is %s', pickle_data)
            preferences = pickle.loads(pickle_data)
        else:
            preferences = {}
        l.debug('preferences is %s', preferences)
        return preferences
        
    def _set_preferences(self, data, session, preferences={}):
        if not session.authenticated:
            raise Exception('Cannot set preferences - you must log on first.')
        l.debug('set preferences to %s', preferences)
        preferences_pickle = pickle.dumps(preferences)
        self.sql_database.set_preferences(session.user_id, preferences_pickle)
        return True
        
    def _deregister(self, data, session):
        if not session.authenticated:
            raise Exception('Cannot deregister - you must log on first.')
        if session.user_id == 1:
            raise Exception('Cannot deregister the system administrator!')
        old_password = data
        if old_password != session.password_hash:
            raise Exception("The old password is incorrect!")
        self.sql_database.deregister_user(session.user_id)
        return ''
            
    def _signup(self, data, session):
        email_address, nickname = data.split('/')
        if self._email_already_registered(email_address):
            raise Exception(ERROR_EMAIL_ALREADY_IN_USE)
        if self._nickname_already_used(nickname):
            raise Exception("This nickname is already in use. Please choose another one.")
        password = self._make_password()
        l.debug('password is %s', password)
        self._add_user(email_address, password, nickname)
        self._email_registration_details(email_address, password, nickname)
        return ''
    
    def _change_password(self, data, session):
        if not session.authenticated:
            raise Exception('Cannot change password - you must log on first.')
        old_password, new_password = data.split('/')
        if old_password != session.password_hash:
            raise Exception("The old password is incorrect!")
        self.sql_database.set_password_hash(session.user_id, new_password)
        return ''
        
    def _nickname_already_used(self, nickname):
        return self.sql_database.nickname_already_used(nickname)
    
    def _email_already_registered(self, email_address):
        return self.sql_database.email_already_registered(email_address)
    
    def _email_registration_details(self, email_address, password, nickname):
        headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % \
                ('abdulhaq@arabicreader.net', email_address, 'ArabicReader registration')
        message = """

Thanks for registering with ArabicReader. Your details are:

Username: %s
Password: %s
Nickname: %s

Now that you have registered, you can add new entries to the database and can
download pdfs of your vocabulary list. See the help page on the site for more
information.

If you wish you can change your password and nickname by logging on and going to the MyReader page.

regards
Abdulhaq
Administrator
        """ % (email_address, password, nickname)
        
        server = smtplib.SMTP('localhost')
        server.set_debuglevel(1)
        server.sendmail('abdulhaq@arabicreader.net',
                        [email_address, 'alynch4047@gmail.com'],
                         headers + message)
        server.quit()
        
    def _hash_password(self, password):
        md5 = hashlib.md5()
        password_hash = md5.update(password)
        password_hash = md5.hexdigest()
        return password_hash
    
    def _add_user(self, email_address, password, nickname):
        password_hash = self._hash_password(password)
        self.sql_database.add_user(email_address, password_hash, nickname)

    def _make_password(self):
        password = ''
        for i in range(2):
            # 97-122 a-z
            # 65-90 A-Z
            # 48-57 0-9
            char_code = random.randint(97, 122)
            password += chr(char_code)
            char_code = random.randint(65, 90)
            password += chr(char_code)
            char_code = random.randint(48, 57)
            password += chr(char_code)
        return password
        
    def _get_user_details_for_email_address(self, email_address):
        user_details = self.sql_database.get_user_details(None, email_address=email_address)
        if user_details is None:
            return None, None
        else:
            l.debug('user id, hash is %s, %s', user_details['user_id'], user_details['password_hash'])
            return user_details['user_id'], user_details['password_hash']
    
