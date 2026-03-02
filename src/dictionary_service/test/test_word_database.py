
import ar_logging
ar_logging.add_std_out()

import unittest

from data.unicode_data import *
from sarf_service.test.test_words import *
from sarf_service.api import constants, Word

from dictionary_service.sql_database.test.test_sql_database import create_test_sql_database

from dictionary_service.word_database import WordDatabase
 
import logging
l = logging.getLogger(__name__)

def create_test_word_database():
    sql_database = create_test_sql_database()
    word_database = WordDatabase(sql_database=sql_database)
    return word_database


class TestWordDatabase(unittest.TestCase):
    
    def setUp(self):
        self.test_word_database = create_test_word_database()
        
#    def test_add_word(self):
#        writer = Word(text=KAATIB, meaning='writer',
#                    root_meaning=root_meaning_ktb,
#                    word_type=word_type_1)
#        self.test_word_database.add_word(writer)
#        self.assert_(writer in self.test_word_database.words)
#        self.assert_(
#             writer in self.test_word_database.words_by_root_meaning[root_meaning_ktb])
        

    def test_words_by_initial_letter(self):
       words_starting_kaaf = self.test_word_database._words_by_letter[KAAF]
       l.debug('kaaf words are %s', words_starting_kaaf)
       self.assertEquals(set([1,3,4]), set([word.id for word in words_starting_kaaf]))
       words_starting_hamza = self.test_word_database._words_by_letter[HAMZA]
       l.debug('hamza words are %s', words_starting_hamza)
       self.assertEquals(set([9, 10]), set([word.id for word in words_starting_hamza]))
       
    def test_words_possibly_matching(self):
        word_text = KAAF + TAA + BAA
        possible_matches = self.test_word_database.words_possibly_matching(word_text)
        self.assertEquals(set([1,3,4]), set([word.id for word in possible_matches]))
        word_text = ALIF + LAAM + ALIF_MAQSURA
        possible_matches = self.test_word_database.words_possibly_matching(word_text)
        self.assert_(9 in [word.id for word in possible_matches])
        
    def test_words_by_root(self):
       database = self.test_word_database
       ktb_words = database.words_by_root[KTB]
       self.assertEquals(len(ktb_words), 4)
       no_root_words = database.words_by_root['']
       self.assertEquals(len(no_root_words), 3)
       
    def test_words_of_kalima_id(self):
        database = self.test_word_database
        words = database.words_of_kalima_id(1)
        self.assertEquals(len(words), 2)
        word_texts = [word.text for word in words]
        self.assert_(KAAF + TAA + BAA in word_texts)
        
    def test_get_next_kalima_id(self):
        next_id = self.test_word_database.get_next_kalima_id(2)
        self.assertEquals(next_id, 3)
        
    def test_get_previous_kalima_id(self):
        next_id = self.test_word_database.get_previous_kalima_id(2)
        self.assertEquals(next_id, 1)
        
    def test_words_by_id(self):
        word_3 = self.test_word_database.words_by_id[3]
        self.assertEquals(word_3.id, 3)
        
    def test_add_and_remove_word(self):
        word = Word(id=1000,
                    kalima_id=500,
                    root=KTB,
                    text=KITAAB,
                    meaning='book',
                    number=1)
        word2 = Word(id=1001,
                    kalima_id=500,
                    root=KTB,
                    text=KUTUB,
                    meaning='book',
                    number=3)
        num_words = len(self.test_word_database.words)
        self.test_word_database.add_word(word, 1, 'alynch')
        self.test_word_database.add_word(word2, 1, 'alynch')
        self.assert_(word in self.test_word_database.words)
        self.assertEquals(len(self.test_word_database.words), num_words + 2)
        self.assert_(word in self.test_word_database.words_by_root[KTB])
        self.assertEquals(word, self.test_word_database.words_by_id[1000])
        self.assert_(word in self.test_word_database.words_by_kalima[500])
        
        self.test_word_database.remove_word(word)
        self.assert_(word not in self.test_word_database.words)
        self.assertEquals(len(self.test_word_database.words), num_words + 1)
        self.assert_(1000 not in self.test_word_database.words_by_id)
        self.assert_(word not in self.test_word_database.words_by_kalima[500])
        self.assert_(word not in self.test_word_database.words_by_root[KTB])
        
        self.assert_(1001 in self.test_word_database.words_by_id)
        self.assert_(word2 in self.test_word_database.words_by_kalima[500])
        self.assert_(word2 in self.test_word_database.words_by_root[KTB])
        
                
       
        
        

