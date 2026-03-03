# coding=utf-8

import ar_logging
import logging
import unittest

from data.unicode_data import *
from sarf_service.test.test_verbs import *
from sarf_service.test.test_words import *

from dictionary_service.test.test_word_database import create_test_word_database
from sarf_service.transliterate import out_in_gb
from sarf_service.inner_words import InnerWords, SWITCH_TAA_MARBUTA, SUFFIX_HU
from sarf_service.word_mangler import to_canonical_letters, arabic_string_matches

def print_matches(matches):
    print()
    for text, ops in matches:
        print('matches', out_in_gb(text), ops)


class TestInnerWords(unittest.TestCase):
    
    def setUp(self):
        word_database = create_test_word_database()
        self.inner_words = InnerWords(word_database=word_database)
        
    def test_verbs(self):
        text = KATABTU
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 5)
        self.assert_(KATABA in [match[0] for match in matches])
        
        text = KATABTI
        matches = self.inner_words.get_inner_word_texts(text)
        self.assert_(KATABA in [match[0] for match in matches])
        
        text = KATABAT
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 12)
        self.assert_(KATABA in [match[0] for match in matches])
        
        text = KATABA
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 4)
        self.assert_(KATABA in [match[0] for match in matches])
        
        text = KATABNAA
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 10)
        self.assert_(KATABA in [match[0] for match in matches])
        
        text = KATABUU
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 11)
        self.assert_(KATABA in [match[0] for match in matches])
        
        text = AKTUBU
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 2)
        self.assert_(YAKTUB in [match[0] for match in matches])
        
        text = TAKTUBU
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 2)
        self.assert_(YAKTUBU in [match[0] for match in matches])
        
        text = NAKTUBU
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 2)
        self.assert_(YAKTUB in [match[0] for match in matches])
        
        text = YAKTUBUUNA
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 5)
        self.assert_(YAKTUB in [match[0] for match in matches])
        
        text = TAKTUBUUNA
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 7)
        self.assert_(YAKTUB in [match[0] for match in matches])
        
    def test_verb_amr(self):
        text = UKTUB
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 2)
        self.assert_(YAKTUB in [match[0] for match in matches])      
        
        text = UKTUBUU
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 6)
        self.assert_(YAKTUB in [match[0] for match in matches])  
        
        text = TBSHSHRUU
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 8)
        self.assert_(any(
                [arabic_string_matches(match, YUBASHSHIRU) for match, reason in matches]))
        
        text = to_canonical_letters(TUBASHSHIRUU)
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 8)
        self.assert_(any(
                [arabic_string_matches(match, YUBASHSHIRU) for match, reason in matches]))
        
#        text = BASHSHIRUU
#        matches = self.inner_words.get_inner_word_texts(text)
#        print_matches(matches)
#        self.assertEquals(len(matches), 4)
#        self.assert_(any(
#                [arabic_string_matches(match, YUBASHSHIRU) for match, reason in matches]))
        
        
    def test_prefixes(self):
        text = ALKITAAB
        matches = self.inner_words.get_inner_word_texts(text)

        self.assertEquals(len(matches), 3)
        self.assert_(KITAAB in [match[0] for match in matches])
        
        text = BILKITAAB
        matches = self.inner_words.get_inner_word_texts(text)

        self.assertEquals(len(matches), 4)
        self.assert_(KITAAB in [match[0] for match in matches])
        
        text = LILKITAAB
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 3)
        self.assert_(KITAAB in [match[0] for match in matches])
        
        text = LILKUTUB
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 3)
        self.assert_(KUTUB in [match[0] for match in matches])
        
        text = SAYAKTUB
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 3)
        self.assert_(YAKTUB in [match[0] for match in matches])
        
    def test_suffixes(self):
        text = KITAABUHU
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 8)
        self.assert_(KITAAB in [match[0] for match in matches])
        
        text = KITAABII
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 8)
        self.assert_(KITAAB in [match[0] for match in matches])
        
        text = KITAABATUHU
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 20)
        self.assert_(KITAABA in [match[0] for match in matches])
        self.assert_([SUFFIX_HU, SWITCH_TAA_MARBUTA]  in [match[1] for match in matches])
        
        text = KITAABUHAA
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 12)
        self.assert_(KITAAB in [match[0] for match in matches])
        
        text = KUTUBUHUM
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 2)
        self.assert_(KUTUB in [match[0] for match in matches])
        
        text = KUTUBUKA
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 3)
        self.assert_(KUTUB in [match[0] for match in matches])
        
        text = KUTUBUKI
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 3)
        self.assert_(KUTUB in [match[0] for match in matches])
        
        text = KUTUBUKUM
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 2)
        self.assert_(KUTUB in [match[0] for match in matches])
        
        text = KITAABAAN
        matches = self.inner_words.get_inner_word_texts(text)
        self.assert_(KITAAB in [match[0] for match in matches])
        
        text = KITAABAYN
        matches = self.inner_words.get_inner_word_texts(text)
        self.assert_(KITAAB in [match[0] for match in matches])
        
    def test_feminine_adjective(self):
        text = MUSLIMA
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 2)
        self.assert_(MUSLIM in [match[0] for match in matches])
        
        text = MUSLIMAAT
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 7)
        self.assert_(MUSLIM in [match[0] for match in matches])
        self.assert_(MUSLIMA in [match[0] for match in matches])
        
    def test_ending_an(self):
        text = RAJULAN
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 2)
        self.assert_(RAJUL in [match[0] for match in matches])
        
    def testing_iya(self):
        text = ISLAMIYA
        matches = self.inner_words.get_inner_word_texts(text)
        self.assert_(ISLAM in [match[0] for match in matches])
        text = ISLAMIYA2
        matches = self.inner_words.get_inner_word_texts(text)
        self.assert_(ISLAM in [match[0] for match in matches])
        
        
    def test_al_plus_shadda(self):
        text = to_canonical_letters(ADDIIN)
        matches = self.inner_words.get_inner_word_texts(text)
        self.assert_(DIIN in [match[0] for match in matches])
        
        text = to_canonical_letters(ADDIIN2)
        matches = self.inner_words.get_inner_word_texts(text)
        self.assert_(DIIN2 in [match[0] for match in matches])
        
    def test_other_words(self):
        text = u"الهم"
        matches = self.inner_words.get_inner_word_texts(text)
        self.assertEquals(len(matches), 6)
        
    def test_ending_in_kasra(self):
        text = to_canonical_letters(u'كتبتِ')
        matches = self.inner_words.get_inner_word_texts(text)
        self.assert_(KATABA in [match[0] for match in matches])
        
        text = to_canonical_letters(u'كَتَبَت')
        matches = self.inner_words.get_inner_word_texts(text)
        self.assert_(KATABA_ in [match[0] for match in matches])
        
        text = to_canonical_letters(u'كَتَبَتِ')
        matches = self.inner_words.get_inner_word_texts(text)
        print('matches', matches)
        self.assert_(KATABAT_ in [match[0] for match in matches])
        
        
        