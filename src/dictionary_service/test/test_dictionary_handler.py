
import ar_logging
import unittest

from data.unicode_data import *
from sarf_service.test.test_words import *

from server.api import URL

from dictionary_service.test.test_dictionary import create_test_dictionary
from dictionary_service.dictionary_handler import DictionaryHandler


class TestDictionaryHandler(unittest.TestCase):
    
    def setUp(self):
        self.handler = DictionaryHandler(dictionary=create_test_dictionary())
        
    def test_get_words_of_same_root(self):
        word_text = KATABA
        res = self.handler._get_words_of_same_root(word_text, None)
        first_root_words = res[0]
        root, words_data = first_root_words
        self.assertEquals(root, KTB)
        self.assert_(len(words_data) > 0)
        for word_data in words_data:
            self.assertEquals(word_data[3], KTB)
        
        res = self.handler._json_and_wrap_error(self.handler._get_words_of_same_root, word_text, None)
        
        url = URL()
        unquoted_url = url._unquote('%u0627%u0644%u0631%u0651%u064E%u062D%u0650%u064A%u0645%u0650')
        res = self.handler._json_and_wrap_error(self.handler._get_words_of_same_root, unquoted_url, None)
        
    def test_get_meanings_for_word(self):
        res = self.handler._json_and_wrap_error(self.handler._get_meanings_for_word, KITAAB, None)
        
    def test_get_words_of_root(self):
        res = self.handler._get_words_of_root(KTB, None)
      
        
        
        

