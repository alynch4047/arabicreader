# coding=utf-8

import logging

from traits.api import (HasTraits, provides,
                                 Dict, Instance, Delegate)

from sarf_service.api import to_canonical_letters

from dictionary_service.i_dictionary import IDictionary
from dictionary_service.i_word_database import IWordDatabase

l = logging.getLogger(__name__)

@provides(IDictionary)
class Dictionary(HasTraits):
    
    words_by_root = Delegate('word_database')
    
    words = Delegate('word_database')
    
    word_database = Instance(IWordDatabase)
    
    sarf = Instance('sarf_service.api.Sarf')
    
    def get_words_of_same_root(self, word_text):
        """ return a dictionary of Root ->[Words] that have the same root
        as the word (there may be more than one possible root)"""
        word_text = to_canonical_letters(word_text)
        words_by_root = {}
        possible_roots = self.sarf.get_possible_roots(word_text,
                                                      self.word_database)
        for root in possible_roots:
            words_by_root[root] = self.words_by_root[root][:]
        return words_by_root
    
    def get_words_of_root(self, root_text):
        return self.words_by_root[root_text][:]
    
    def get_words_matching_text(self, word_text):
        """ get all possible meanings for a word string. Words can be composites
        such as bikitaabihi"""
        word_text = to_canonical_letters(word_text)
        words = self.sarf.get_possible_words(word_text,
                                            self.word_database)
        words = set(words)
        return words
    
    def get_meanings_for_word(self, word_text):
        """ get all possible meanings for a word string. Words can be composites
        such as bikitaabihi"""
        word_text = to_canonical_letters(word_text)
        meanings_for_word = []
        words = self.sarf.get_possible_words(word_text,
                                            self.word_database)
        words = set(words)
        for word in words:
            meanings_for_word.append([word.id, word.text, word.meaning, word.kalima_id])
        return meanings_for_word
    
    def _sarf_default(self):
        from sarf_service.api import Sarf
        return Sarf(word_database=self.word_database)
    

    
    