
import logging
import itertools
from datetime import datetime
from base64 import b64encode, b64decode

from session_service.email import send_email

from sqlalchemy import (MetaData, Table, Integer, Unicode, DateTime, Boolean,
                        Column, func, select, and_)

from sarf_service.api import to_canonical_letters, Word, constants

l = logging.getLogger(__name__)

def disconnect():
    """commit and close all connections"""
    pass


class SQLDatabase(object):
    
    def __init__(self, engine):

        self.engine = engine
        
        self.metadata = MetaData()
        
        self.kalima = Table('kalima', self.metadata, 
            Column('kalima_id', Integer, primary_key=True),
            Column('kalima_jidhr1', Unicode(1)),
            Column('kalima_jidhr2', Unicode(1)),
            Column('kalima_jidhr3', Unicode(1)),
            Column('kalima_meaning', Unicode(255)),
            Column('created_date', DateTime),
            Column('kalima_type', Integer),
            Column('user_id', Integer),
        )
        
        self.kalima_variation = Table('kalima_variation', self.metadata, 
            Column('kalvar_id', Integer, primary_key=True),
            Column('kalima_id', Integer),
            Column('kalvar_text', Unicode(255)),
            Column('kalvar_number', Integer),
            Column('kalvar_tense', Integer),
        )
        
        self.users = Table('users', self.metadata,
                Column('user_id', Integer, primary_key=True),
                Column('nickname', Unicode(200)),
                Column('email_address', Unicode(200)),
                Column('password_hash', Unicode(200)),
                Column('last_logon', DateTime),
                Column('preferences_pickle', Unicode(10000)),
                )
        
        self.links = Table('links', self.metadata,
                    Column('link_id', Integer, primary_key=True),
                    Column('user_id', Integer),
                    Column('url', Unicode(200)),
                    Column('description', Unicode(300)),
                    Column('difficulty', Integer),
                    Column('public', Boolean),
                           )
        
        self.vocabulary = Table('vocabulary', self.metadata,
                    Column('kalima_id', Integer, primary_key=True),
                    Column('user_id', Integer, primary_key=True),
                    Column('click_count', Integer),
                    Column('last_click_datetime', DateTime))
        
        self.metadata.bind = self.engine
        self.metadata.create_all()
        
    def remove_vocabulary_word(self, user_id, kalima_id):
        self.engine.execute(
            self.vocabulary.delete(self.vocabulary.c.user_id==user_id and \
                                           self.vocabulary.c.kalima_id==kalima_id))
        
    def add_vocabulary_word(self, user_id, kalima_id):
        """
        If the word is not already there then add it with a click_count of 1.
        If it is already there then add 1 to the click_count.
        """
        sel = select([self.vocabulary.c.click_count],
            self.vocabulary.c.user_id==user_id and self.vocabulary.c.kalima_id==kalima_id)
        results = self.engine.execute(sel).fetchall()
        if len(results) == 0:
            l.debug('add row')
            # insert new row
            self.engine.execute(self.vocabulary.insert(),
                         kalima_id=kalima_id,
                         user_id=user_id,
                         click_count=1,
                         last_click_datetime=datetime.now()
                         )
        else:
            assert(len(results) == 1)
            # update click_count
            new_click_count = results[0][0] + 1
            l.debug('new click count is %s', new_click_count)
            self.engine.execute(
                    self.vocabulary.update(self.vocabulary.c.user_id==user_id and \
                                           self.vocabulary.c.kalima_id==kalima_id),
                         click_count=new_click_count,
                         last_click_datetime=datetime.now()
                         )
        
    def get_vocabulary_details(self, user_id):
        sel = select([self.vocabulary.c.kalima_id,
                      self.vocabulary.c.click_count,
                      self.vocabulary.c.last_click_datetime],
               self.vocabulary.c.user_id==user_id)
        results = self.engine.execute(sel).fetchall()
        return results
    
    def get_vocabulary_count(self, user_id):
        sel = select([func.count(self.kalima.c.kalima_id)],
                        and_(self.kalima.c.user_id==user_id,
                             self.kalima.c.kalima_id==self.kalima_variation.c.kalima_id))
        count = self.engine.execute(sel).scalar()
        return count
        
    def get_user_details(self, user_id, email_address=None):
        """
        Get the user for the given user_id or email_address if given
        """
        if email_address is None:
            sel = select([self.users.c.user_id, self.users.c.nickname,
                          self.users.c.email_address, self.users.c.password_hash,
                          self.users.c.last_logon, self.users.c.preferences_pickle],
                   self.users.c.user_id==user_id)
        else:
            sel = select([self.users.c.user_id, self.users.c.nickname,
                          self.users.c.email_address, self.users.c.password_hash,
                          self.users.c.last_logon, self.users.c.preferences_pickle],
                   self.users.c.email_address==email_address)
        results = self.engine.execute(sel).fetchall()
        if results:
            user_details = {}
            for key, value in results[0].items():
                user_details[key] = value
            if user_details['preferences_pickle'] is not None:
                try:
                    user_details['preferences_pickle'] = \
                                        b64decode(user_details['preferences_pickle'])
                except:
                    l.exception('decoding preferences')
                    user_details['preferences_pickle'] = None
            return user_details
        else:
            return None
        
    def set_preferences(self, user_id, preferences_pickle):
        l.debug('set prefs pickle to %s', preferences_pickle)
        preferences_pickle_encoded = b64encode(preferences_pickle)
        self.engine.execute(self.users.update(
                    self.users.c.user_id==user_id),
                         preferences_pickle=unicode(preferences_pickle_encoded),
                         )
        
    def set_password_hash(self, user_id, password_hash):
        l.debug('set password hash for %s to %s', user_id, password_hash)
        self.engine.execute(self.users.update(
                    self.users.c.user_id==user_id),
                         password_hash=password_hash,
                         )
        
    def deregister_user(self, user_id):
        self.engine.execute(self.kalima.update(
                    self.kalima.c.user_id==user_id),
                         user_id=1,
                         )
        self.engine.execute(self.users.delete(self.users.c.user_id==user_id))
        
    def nickname_already_used(self, nickname):
        sel = select([func.count(self.users.c.user_id)],
                        self.users.c.nickname==nickname)
        count = self.engine.execute(sel).scalar()
        return count > 0
    
    def email_already_registered(self, email_address):
        sel = select([func.count(self.users.c.user_id)],
                        self.users.c.email_address==email_address)
        count = self.engine.execute(sel).scalar()
        return count > 0
        
    def _get_like_pattern_for_filter(self, filter):
        like_pattern = ''
        for letter in filter:
            if like_pattern:
                like_pattern += '%'
            like_pattern += letter
        like_pattern = '%' + like_pattern + '%'
        l.debug('like pattern is %s', like_pattern)
        return like_pattern
    
    def get_next_kalima_id(self, kalima_id, filter=None):
        if filter:
            like_pattern = self._get_like_pattern_for_filter(filter)
            where_clause = and_(self.kalima_variation.c.kalima_id > kalima_id,
                                self.kalima_variation.c.kalvar_text.like(like_pattern))
        else:
            where_clause = self.kalima_variation.c.kalima_id > kalima_id
        next_id = select([func.min(self.kalima_variation.c.kalima_id)]).where(
                                                                where_clause).scalar()
        return next_id
                            
    def get_last_kalima_id(self):
        return select([func.max(self.kalima.c.kalima_id)]).scalar()
                            
    def get_previous_kalima_id(self, kalima_id, filter=None):
        if filter:
            like_pattern = self._get_like_pattern_for_filter(filter)
            where_clause = and_(self.kalima_variation.c.kalima_id < kalima_id,
                                self.kalima_variation.c.kalvar_text.like(like_pattern))
        else:
            where_clause = self.kalima_variation.c.kalima_id < kalima_id
        return select([func.max(self.kalima_variation.c.kalima_id)]).where(
                                                                where_clause).scalar()
                            
    def delete_kalima(self, kalima_id, user_id):
        send_email('alynch4047@googlemail.com',
                   'attempt to delete kalima (%s) by user %s' % (kalima_id, user_id),
                   'word deleted in arabicreader' )
        self._assert_changes_allowed(kalima_id, user_id)
        self.engine.execute(self.kalima.delete(self.kalima.c.kalima_id == kalima_id))
        self.engine.execute(self.kalima_variation.delete(
                                     self.kalima_variation.c.kalima_id == kalima_id))
        
    def add_word_set(self, word_set, user_id):
        send_email('alynch4047@googlemail.com',
                   'word set added (%s) by user %s' % (word_set, user_id),
                   'new word added to arabicreader by userid %s' % user_id)
        assert(word_set.kalima_id == 0)
        word_set.kalima_id = self._get_kalima_sequence()
        self.engine.execute(self.kalima.insert(),
                         kalima_id=word_set.kalima_id,
                         kalima_jidhr1=unicode(word_set.root_f),
                         kalima_jidhr2=unicode(word_set.root_c),
                         kalima_jidhr3=unicode(word_set.root_l),
                         kalima_meaning=word_set.meaning,
                         kalima_type=word_set.word_type,
                         user_id=user_id,
                         )
        for variation in word_set.variations:
            assert(variation.kalvar_id == 0)
            variation.kalvar_id = self._get_kalvar_sequence()
            self.engine.execute(self.kalima_variation.insert(),
                         kalima_id=word_set.kalima_id,
                         kalvar_id=variation.kalvar_id,
                         kalvar_text=unicode(variation.text),
                         kalvar_number=variation.number,
                         kalvar_tense=variation.tense,
                         )
        return word_set.kalima_id
    
    def _get_word_creator(self, kalima_id):
        sel = select([self.kalima.c.user_id],
               self.kalima.c.kalima_id==kalima_id)
        results = self.engine.execute(sel).fetchall()
        return [row[0] for row in results][0]
    
    def _assert_changes_allowed(self, kalima_id, user_id):
        word_creator_id = self._get_word_creator(kalima_id)
        if user_id != 1 and word_creator_id != user_id:
            l.error('creator %s user %s', word_creator_id, user_id)
            raise Exception('cannot update the database - only the creator of the word can change it')
            
    def update_word_set(self, word_set, user_id):
        send_email('alynch4047@googlemail.com',
                   'word set updated (%s) by user %s' % (word_set, user_id),
                   'word updated in arabicreader by userid %s' % user_id )
        assert(word_set.kalima_id != 0)
        self._assert_changes_allowed(word_set.kalima_id, user_id)
        self.engine.execute(self.kalima.update(
                    self.kalima.c.kalima_id==word_set.kalima_id),
                         kalima_jidhr1=unicode(word_set.root_f),
                         kalima_jidhr2=unicode(word_set.root_c),
                         kalima_jidhr3=unicode(word_set.root_l),
                         kalima_meaning=word_set.meaning,
                         kalima_type=word_set.word_type
                         )
                         
        for variation in word_set.variations:
            if variation.kalvar_id != 0:
                self.engine.execute(self.kalima_variation.update(
                    self.kalima_variation.c.kalvar_id==variation.kalvar_id),
                         kalvar_text=unicode(variation.text),
                         kalvar_number=variation.number,
                         kalvar_tense=variation.tense,
                         )
            else:
                variation.kalvar_id = self._get_kalvar_sequence()
                self.engine.execute(self.kalima_variation.insert(),
                         kalima_id=word_set.kalima_id,
                         kalvar_id=variation.kalvar_id,
                         kalvar_text=unicode(variation.text),
                         kalvar_number=variation.number,
                         kalvar_tense=variation.tense,
                         )
        
        # process deletes of kalvars
        kalvars_in_db = self._get_kalvars_for_kalima_id(word_set.kalima_id)
        kalvars_in_wordset = [variation.kalvar_id for variation in word_set.variations]
        deleted_kalvars = [kalvar for kalvar in kalvars_in_db if
                kalvar not in kalvars_in_wordset]
        for kalvar_id in deleted_kalvars:
            self.engine.execute(self.kalima_variation.delete(
                                     self.kalima_variation.c.kalvar_id == kalvar_id))
        
    def _get_kalvars_for_kalima_id(self, kalima_id):
        sel = select([self.kalima_variation.c.kalvar_id],
               self.kalima_variation.c.kalima_id==kalima_id)
        results = self.engine.execute(sel).fetchall()
        return [row[0] for row in results]
            
    def add_test_user(self, user_id, nickname):
        self.engine.execute(self.users.insert(),
                         user_id=user_id,
                         nickname=unicode(nickname)
                         )
    def add_user(self, email_address, password_hash, nickname):
        user_id = self._get_user_sequence()
        self.engine.execute(self.users.insert(),
                         user_id=user_id,
                         email_address=email_address,
                         password_hash=password_hash,
                         nickname=nickname
                         )
        
    def add_link(self, user_id, url, difficulty, public):
        link_id = self._get_link_sequence()
        self.engine.execute(self.links.insert(),
                        link_id=link_id,
                        user_id=user_id,
                        url=unicode(url),
                        difficulty=difficulty,
                        public=public
                         )
        
    def get_public_links(self):
        sel = select([self.links.c.user_id, self.links.c.url, self.links.c.difficulty],
               self.links.c.public==True)
        results = self.engine.execute(sel).fetchall()
        return results
    
    def get_user_links(self, user_id):
        sel = select([self.links.c.user_id, self.links.c.url, self.links.c.difficulty],
               self.links.c.user_id==user_id)
        results = self.engine.execute(sel).fetchall()
        return results
            
    def get_words(self):
        words = []
        kalima_variations = self.kalima.join(self.kalima_variation,
                            self.kalima_variation.c.kalima_id==self.kalima.c.kalima_id)
        kalima_variations_user = kalima_variations.join(self.users,
                            self.users.c.user_id==self.kalima.c.user_id)
        results = self.engine.execute(kalima_variations_user.select()).fetchall()
        for result in results:
            word = self._create_word(*result)
            if word:
                words.append(word)
        return words
    
    def _get_kalima_sequence(self):
        result = self.engine.execute("""select nextval('kalima_sequence')""").fetchall()[0]
        return result[0]
    
    def _get_kalvar_sequence(self):
        result = self.engine.execute("""select nextval('kalvar_sequence')""").fetchall()[0]
        return result[0]
    
    def _get_user_sequence(self):
        result = self.engine.execute("""select nextval('user_id_sequence')""").fetchall()[0]
        return result[0]
    
    def _get_link_sequence(self):
        result = self.engine.execute("""select nextval('link_sequence')""").fetchall()[0]
        return result[0]
        
    
    def _create_word(self, kalima_id, root_f, root_c, root_l, meaning,
                      created_date, word_type, user_id, 
                      kalvar_id, kalima_id_2, text, number, tense,
                      user_id_2, nickname, email_address, password_hash, last_logon,
                      preferences_pickle):

        root = root_f + root_c + root_l
        
        if text.find(' ') != -1:
            text = text.split(' ')[0]
        
        try:
            text = to_canonical_letters(text)
        except Exception, ex:
            l.exception('error getting text for word of id %s', kalvar_id)
            text = ''
        
        if text == '':
            l.error('empty text for word kalvar_id: %s', kalvar_id)
            return None
        
        if number is None:
            number = 0
        if tense is None:
            tense = 0
        if word_type == constants.WORD_TYPE_VERB:
            assert tense != 0
        if word_type == constants.WORD_TYPE_NOUN:
#            assert number != 0
            if number == 0:
                l.error('number is 0 for word kalvar_id: %s', kalvar_id)
                return None
            
        word = Word(id=kalvar_id,
                    word_type=word_type,
                    text=text,
                    root=root,
                    meaning=meaning,
                    number=number,
                    tense=tense,
                    kalima_id=kalima_id,
                    creator_id=user_id,
                    nickname=nickname)
        return word
    
    
class SQLiteSQLDatabase(SQLDatabase):
    
    def __init__(self, engine):
        SQLDatabase.__init__(self, engine)
        
        self.kalima_sequence = itertools.count(1)
        self.kalvar_sequence = itertools.count(1)
        self.link_sequence = itertools.count(1)
    
    def _get_kalima_sequence(self):
        return self.kalima_sequence.next()
    
    def _get_kalvar_sequence(self):
        return self.kalvar_sequence.next()
    
    def _get_link_sequence(self):
        return self.link_sequence.next()


