
import ar_logging
import unittest

from vocabulary_service.vocabulary_handler import VocabularyHandler


class TestVocabularyHandler(unittest.TestCase):
    
    def setUp(self):
        self.handler = VocabularyHandler({})
        
    def test_get_all_words(self):
        res = self.handler._json_and_wrap_error(self.handler._get_all_words, '', None)
        
      
        
        
        

