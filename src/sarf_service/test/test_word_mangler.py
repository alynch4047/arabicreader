
import ar_logging
import unittest
ar_logging.add_std_out()

from data.unicode_data import *
from sarf_service.test.test_words import *

from sarf_service.word_mangler import (strip_harakaat, to_canonical_letters,
                                      get_word_haraka_pairs, arabic_string_matches,
                                      _switch_shaddas, _shaddas_match,
                                      _get_shadda_locations)


class TestWordMangler(unittest.TestCase):
    
    def test_to_canonical_letters(self):
        word = u'\u062a\u0646\u0641\u0651\u0650\u0631\u0648\u0627'
        canonical_word = to_canonical_letters(word)
        self.assertEquals(canonical_word, u'\u062a\u0646\u0641\u0650\u0651\u0631\u0648\u0627')
        
    def test_strip_harakaat(self):
        self.assertNotEquals(KITAAB_, KITAAB)
        self.assertEquals(strip_harakaat(KITAAB_), KITAAB)
        
    def testget_word_haraka_pairs(self):
        word = FAA + FATHA + AYN + KASRA + LAAM
        pairs = get_word_haraka_pairs(word)
        self.assertEquals(pairs, [(FAA, FATHA), (AYN, KASRA), (LAAM, None)])
        
        word = FAA + AYN + KASRA + LAAM
        pairs = get_word_haraka_pairs(word)
        self.assertEquals(pairs, [(FAA, None), (AYN, KASRA), (LAAM, None)])
        
        word = FAA + AYN + LAAM
        pairs = get_word_haraka_pairs(word)
        self.assertEquals(pairs, [(FAA, None), (AYN, None), (LAAM, None)])
        
        word = FAA
        pairs = get_word_haraka_pairs(word)
        self.assertEquals(pairs, [(FAA, None)])
        
    def test_arabic_string_matches(self):
        wordA = FAA + FATHA + AYN + KASRA + LAAM
        wordB = FAA + AYN + KASRA + LAAM
        self.assertEquals(arabic_string_matches(wordA, wordB), True)
        
        wordA = FAA + FATHA + AYN + KASRA + LAAM
        wordB = FAA + AYN + DAMMA + LAAM
        self.assertEquals(arabic_string_matches(wordA, wordB), False)
        
        wordA = FAA + FATHA + AYN + KASRA + LAAM
        wordB = FAA + AYN + LAAM
        self.assertEquals(arabic_string_matches(wordA, wordB), True)
        
        wordA = FAA + AYN + KASRA + LAAM
        wordB = FAA + FATHA + AYN + LAAM
        self.assertEquals(arabic_string_matches(wordA, wordB), True)
        
        wordA = KAAF + AYN + KASRA + LAAM
        wordB = FAA + FATHA + AYN + LAAM
        self.assertEquals(arabic_string_matches(wordA, wordB), False)
        
    def test_arabic_string_matches_ignore_shadda(self):
        wordA = KAAF + TAA + BAA
        wordB = KAAF + TAA + SHADDA + BAA
        self.assertEquals(arabic_string_matches(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), True)
        
        wordA = KAAF + TAA + SHADDA + BAA
        wordB = KAAF + TAA + SHADDA + BAA
        self.assertEquals(arabic_string_matches(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), True)
        
        wordA = KAAF + TAA + SHADDA + BAA
        wordB = KAAF + TAA + SHADDA + BAA + SHADDA
        self.assertEquals(arabic_string_matches(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), True)
        
        wordA = KAAF + SHADDA + TAA + SHADDA + BAA
        wordB = KAAF + TAA + SHADDA + BAA + SHADDA
        self.assertEquals(arabic_string_matches(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), False)
        
        wordA = KAAF + SHADDA + TAA + BAA
        wordB = KAAF + SHADDA + TAA + SHADDA + BAA + SHADDA
        self.assertEquals(arabic_string_matches(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), True)
        
        wordA = KAAF + FATHA + SHADDA + TAA + BAA
        wordB = KAAF + SHADDA + TAA + KASRA + SHADDA + BAA + SHADDA
        self.assertEquals(arabic_string_matches(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), True)
        
        wordA = KAAF + FATHA + SHADDA + TAA + FATHA + BAA
        wordB = KAAF + SHADDA + TAA + KASRA + SHADDA + BAA + SHADDA
        self.assertEquals(arabic_string_matches(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), False)
        
        wordA = BAA + SHIIN + RAA
        wordB = BAA + SHIIN + SHADDA + RAA
        self.assertEquals(arabic_string_matches(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), True)
        
    def test_switch_shaddas(self):
        text = KAAF + TAA + BAA
        changed_text = _switch_shaddas(text)
        self.assertEquals(changed_text, KAAF + TAA + BAA)
        
        text = KAAF + TAA + BAA + SHADDA
        changed_text = _switch_shaddas(text)
        self.assertEquals(changed_text, KAAF + TAA + BAA + SHADDA)
        
        text = KAAF + TAA + FATHA + SHADDA + BAA
        changed_text = _switch_shaddas(text)
        self.assertEquals(changed_text, KAAF + TAA + FATHA + SHADDA + BAA)
        
        text = KAAF + TAA + SHADDA + FATHA + BAA
        changed_text = _switch_shaddas(text)
        self.assertEquals(changed_text, KAAF + TAA + FATHA + SHADDA + BAA)
        
        text = u'\u062a\u0646\u0641\u0651\u0650\u0631\u0648\u0627'
        changed_text = _switch_shaddas(text)
        self.assertEquals(changed_text, u'\u062a\u0646\u0641\u0650\u0651\u0631\u0648\u0627')
        
    def test_shaddas_match(self):
        wordA = KAAF + TAA + BAA
        wordB = KAAF + TAA + SHADDA + BAA
        self.assertEquals(_shaddas_match(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), True)
        
        wordA = KAAF + TAA + BAA
        wordB = KAAF + TAA + SHADDA + BAA
        self.assertEquals(_shaddas_match(wordA, wordB,
                                                allow_omitted_shadda_in_a=False), False)
        
        wordA = KAAF + TAA + SHADDA + BAA
        wordB = KAAF + TAA + SHADDA + BAA
        self.assertEquals(_shaddas_match(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), True)
        
        wordA = KAAF + TAA + SHADDA + BAA
        wordB = KAAF + TAA + BAA
        self.assertEquals(_shaddas_match(wordA, wordB,
                                                allow_omitted_shadda_in_a=True), False)
        
    def test_shadda_locations(self):
        word = KAAF + TAA + SHADDA + BAA
        self.assertEquals(_get_shadda_locations(word), [2])
    
        word = KAAF + TAA + BAA + SHADDA
        self.assertEquals(_get_shadda_locations(word), [3])
    
        word = KAAF + SHADDA + TAA + BAA + SHADDA
        self.assertEquals(_get_shadda_locations(word), [1, 3])  
        
        word = KAAF + SHADDA + TAA + BAA + SHADDA + YAA + SHADDA
        self.assertEquals(_get_shadda_locations(word), [1, 3, 4])         
        