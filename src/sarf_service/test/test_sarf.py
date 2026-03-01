
import ar_logging
import unittest

from sarf_service.test.test_words import *

from dictionary_service.api import WordDatabase
from dictionary_service.test.test_word_database import create_test_word_database
from sarf_service.constants import *
from sarf_service.sarf import Sarf
from sarf_service.word import Word
from sarf_service.transliterate import transliterate_to_gb

import logging
l = logging.getLogger(__name__)

def matches_a_word(text, words):
    for word in words:
        if word.matches(text):
            return True
    return False


class TestSarf(unittest.TestCase):
    
    def setUp(self):
        word_database = create_test_word_database()
        self.all_words = word_database.words
        self.sarf = Sarf()
        
    def test_get_possible_roots(self):
        roots = self.sarf.get_possible_roots(KITAAB, self.all_words)
        self.assertEquals(roots, [KTB])
        
        roots = self.sarf.get_possible_roots(ALKITAAB, self.all_words)
        self.assertEquals(roots, [KTB])
        
        roots = self.sarf.get_possible_roots(FACALA, self.all_words)
        self.assertEquals(roots, [FCL])
        
    def test_get_possible_roots_unknown(self):
        roots = self.sarf.get_possible_roots_unknown(KITAAB)
        self.assertEquals(roots, [KTB])
        
    def test_get_possible_words(self):
        words = self.sarf.get_possible_words(KITAAB, self.all_words)
        self.assertEquals(len(words), 1)
        self.assertEquals(words[0].text, KITAAB)
        words = self.sarf.get_possible_words(ALKITAAB, self.all_words)
        self.assertEquals(len(words), 1)
        self.assertEquals(words[0].text, KITAAB)
        words = self.sarf.get_possible_words(LILKUTUB, self.all_words)
        self.assertEquals(len(words), 2)
        print words
        self.assertEquals(words[1].text, KUTUB)
        words = self.sarf.get_possible_words(YAKTUBU, self.all_words)
        self.assertEquals(len(words), 1)
        self.assertEquals(words[0].text, YAKTUBU)
        words = self.sarf.get_possible_words(TAKTUBU, self.all_words)
        self.assertEquals(len(words), 1)
        self.assert_(matches_a_word(YAKTUBU, words))
        
    def test_get_past_forms(self):
        word_facala = Word(root=FCL,
                    text=FACALA,
                    word_type=WORD_TYPE_VERB,
                    tense=WORD_TENSE_PAST)
        past_forms = self.sarf.get_past_forms(word_facala)
        FACALTU = FCL + TU
        FACALNAA = FCL + NAA
        FACALUU = FCL + UU
        FACALAHU = FCL + HAA
        facaltu_found = False
        facalnaa_found = False
        facalahu_found = False
        for form in past_forms:
            if form.matches(FACALTU):
                facaltu_found = True
            if form.matches(FACALNAA):
                facalnaa_found = True
            if form.matches(FACALAHU):
                facalahu_found = True
        self.assertEquals(facaltu_found, True)
        self.assertEquals(facalnaa_found, True)
        self.assertEquals(facalahu_found, False)
        
    def test_get_present_forms(self):
        word_yaktubu = Word(root=KTB,
                    text=YAKTUBU,
                    word_type=WORD_TYPE_VERB,
                    tense=WORD_TENSE_PRESENT)
        present_forms = self.sarf.get_present_forms(word_yaktubu)
        TAKTUBU = TA + KTB + DAMMA
       
        taktubu_found = False
        for form in present_forms:
            if form.matches(TAKTUBU):
                
                taktubu_found = True
        self.assertEquals(taktubu_found, True)
