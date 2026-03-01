import logging

from traits.api import HasTraits, Interface, implements, Any, Str, List
from traits.api import TraitString, Int, Instance

from sarf_service.constants import *
from sarf_service.root import RootMeaning, IRootMeaning
from sarf_service.word_mangler import (strip_harakaat, arabic_string_matches,
                                       to_canonical_letters, to_core_letters)
from sarf_service.transliterate import transliterate_to_gb

l = logging.getLogger(__name__)


class IWord(Interface):
    
    # the id of the word in the database (KALVAR_ID)
    id = Int
    
    # the canonical spelling of the word which should include harakaat
    text = Str
    
    # noun, verb, preposition etc
    word_type = Int
    
    # past or present
    tense = Int
    
    # singular, dual or plural
    number = Int
    
    # masculine or female
    gender = Int
    
    # pointer to other known variations of the word, e.g. plural, feminine, or mudari` 
    kalima_id = Int
    
    # the root (usally 3 letters)
    root = Str
    
    # the meaning of the word, in English
    meaning = Str
    
    # the canonical form of the word, ie. with standardised unicode chars, for
    # textual representation
    canonical_form = Str
    
    # the core form, used for matching. All hamzas and yaas, for instance, are unified
    core_form = Str
    
    # the user who created the word
    creator_id = Int
    nickname = Str
    
    def matches(self, word):
        """ If the passed-in word could be this word 
        (e.g. passed in word has no harakaat) then return True"""
        
    def is_noun(self):
        """ Return true if the word is a noun"""
    

class Word(HasTraits):
    
    implements(IWord)
    
    id = Int
    text = Str
    word_type = Int
    tense = Int
    number = Int
    gender = Int
    kalima_id = Int 
    root = Str
    meaning = Str
    canonical_form = Str
    core_form = Str
    creator_id = Int
    nickname = Str
    
    _word_no_harakaat = Str
    
    def matches(self, word_string):
        """ If the passed-in word could be this word 
        (e.g. passed in word has no harakaat) then return True. word_string
        should be canonical"""
        assert(self.text), 'text is empty for kalvar_id %s' % self.id
        assert word_string == to_canonical_letters(word_string) 
        if arabic_string_matches(to_core_letters(word_string), self.core_form,
                                 allow_omitted_shadda_in_a=True,
                                 alif_can_be_hamza=True):
            return True
        # TODO: does this belong here?? - 
        if self.canonical_form[-1] == ALIF_MAQSURA:
            # could be alif maqsuura for instance
            if arabic_string_matches(word_string, self.canonical_form[:-1] + ALIF,
                                     allow_omitted_shadda_in_a=True,
                                     alif_can_be_hamza=True):
                return True
        if self.canonical_form[-1] == TAA_MARBUTA:
            # sometimes the word string ends in haa' but means taa' marbuTa
            if arabic_string_matches(word_string, self.canonical_form[:-1] + HAA,
                                     allow_omitted_shadda_in_a=True,
                                     alif_can_be_hamza=True):
                return True
        return False
    
    def break_out(self):
        return [self.id, self.text, self.meaning,
                self.word_type, self.number, self.tense, self.kalima_id]
    
    def _canonical_form_default(self):
        return to_canonical_letters(self.text)
    
    def _core_form_default(self):
        return to_core_letters(self.text)
        
    def __word_no_harakaat_default(self):
        return strip_harakaat(self.text)
    
    def __repr__(self):
        return '<Word %s: %s %s %s>' % \
                (self.id, transliterate_to_gb(self.text), self.word_type, id(self))

    

    
    