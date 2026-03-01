
import ar_logging
import unittest

from data.unicode_data import *
from sarf_service.test.test_words import *

from sarf_service.api import Word

from dictionary_service.dictionary import Dictionary
from dictionary_service.word_database import WordDatabase
from dictionary_service.test.test_word_database import create_test_word_database

import logging
l = logging.getLogger(__name__)

def create_test_dictionary():
    word_database = create_test_word_database()
    return Dictionary(word_database=word_database)


class TestDictionary(unittest.TestCase):
    
    def setUp(self):
        self.dictionary = create_test_dictionary()
        
    def test_get_words_of_same_root(self):
        words_by_root = self.dictionary.get_words_of_same_root(KITAAB)
        print words_by_root
        self.assertEquals(len(words_by_root[KTB]), 4)
        
#    def test_get_words_of_root(self):
#        words_by_root = self.dictionary.get_words_of_root(KTB)
#        self.assertEquals(len(words_by_root[KTB]), 4)
#       
#    def test_get_word_meaning(self):
#        meanings = self.dictionary.get_meanings_for_word(ALKITAAB)
#        self.assertEquals(len(meanings),1)
#        self.assertEquals(meanings[0][2],'book')
#        meanings = self.dictionary.get_meanings_for_word(TAKTUBU)
#        self.assertEquals(len(meanings), 1)
        
        
        
        

