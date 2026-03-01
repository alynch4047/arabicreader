
import ar_logging
import unittest
import simplejson

from sarf_service.test.test_words import *
from sarf_service.word import Word
from sarf_service.constants import *


class TestWord(unittest.TestCase):
        
    def test_match_word(self):
        word_kitaab = Word(root=KTB,
                    text=KITAAB,
                    number=WORD_NUMBER_SINGULAR,
                    gender=WORD_GENDER_MASCULINE,
                    word_type=WORD_TYPE_NOUN)
        
        self.assertEquals(word_kitaab.matches(KITAAB), True)
        self.assertEquals(word_kitaab.matches(ALKITAAB), False)
        
    def test_serialise_word(self):
        word = Word(root=KTB,
                    text=KITAAB,
                    number=WORD_NUMBER_SINGULAR,
                    gender=WORD_GENDER_MASCULINE,
                    word_type=WORD_TYPE_NOUN)
        res = simplejson.dumps([word.text, word.meaning], check_circular=True)
        
    def test_canonical_form(self):
        word = Word(text=AHAD,
                    word_type=WORD_TYPE_NOUN,
                    gender=WORD_GENDER_MASCULINE)
        self.assertEquals(HAMZA + HAA_ + DAAL, word.canonical_form)
        word = Word(text=AHAD_,
                    word_type=WORD_TYPE_NOUN,
                    gender=WORD_GENDER_MASCULINE)
        self.assertEquals(HAMZA + FATHA + HAA_ + DAAL + DAMMATAAN, word.canonical_form)
        
        