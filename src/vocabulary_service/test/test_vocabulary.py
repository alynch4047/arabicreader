
import ar_logging
import unittest

from dictionary_service.test.test_word_database import create_test_word_database
from session_service.api import Session, MIN_GUEST_ID

from vocabulary_service.vocabulary import Vocabulary


class TestVocabulary(unittest.TestCase):
    
    def setUp(self):
        self.word_database = create_test_word_database()
        
    def test_guest_get_all_words(self):
        guest_session = Session(user_id=MIN_GUEST_ID)
        vocabulary = Vocabulary(session=guest_session,
                                word_database=self.word_database,
                                sql_database=self.word_database.sql_database)
        res = vocabulary.get_all_words()
        self.assertEquals(len(res), 0)
        vocabulary.add_word(1)
        res = vocabulary.get_all_words()
        self.assertEquals(len(res), 1)
        
    def test_guest_add_word(self):
        guest_session = Session(user_id=MIN_GUEST_ID)
        vocabulary = Vocabulary(session=guest_session,
                                word_database=self.word_database,
                                sql_database=self.word_database.sql_database)
        word = vocabulary.word_database.words_by_id[1]
        res = vocabulary.add_word(word.id)
        
    def test_non_guest_get_all_words(self):
        session = Session(user_id=1)
        vocabulary = Vocabulary(session=session,
                                word_database=self.word_database,
                                sql_database=self.word_database.sql_database)
        res = vocabulary.get_all_words()
        self.assertEquals(len(res), 0)
        vocabulary.add_word(1)
        res = vocabulary.get_all_words()
        self.assertEquals(len(res), 1)
        
      
        
        
        

