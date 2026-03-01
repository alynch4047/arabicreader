
import ar_logging
import unittest

from data.unicode_data import *
from sarf_service.test.test_words import *

from sarf_service.transliterate import transliterate_to_gb


class TestTransliterate(unittest.TestCase):
        
    def test_transliterate_1(self):
        word_1 = ALIF + BAA
        res = transliterate_to_gb(word_1)
        self.assertEquals(res, 'Ab')
        
        word_2 = ALKITAAB
        res = transliterate_to_gb(word_2)
        self.assertEquals(res, 'AlktAb')
        
        word_3 = KITAAB_
        res = transliterate_to_gb(word_3)
        self.assertEquals(res, 'kitAb')
        