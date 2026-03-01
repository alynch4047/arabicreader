
import logging

from traits.api import HasTraits, Instance

from data.unicode_data import *

from sarf_service.constants import *
from sarf_service.word import Word
from sarf_service.word_mangler import strip_harakaat, to_canonical_letters
from sarf_service.inner_words import InnerWords

l = logging.getLogger(__name__)


class Sarf(HasTraits):
    """ The Sarf class provides roots of a word"""
    
    inner_words = Instance(InnerWords, ())
    
    def get_possible_roots(self, word_text, word_database):
        """ Get the possible roots of a word, which may have a prefix or suffix.
         A single word could be construed in more than one way, particularly
         as the word may start with fa, wa, bi or
         li for instance, or have a possessive pronoun attached""" 
        roots = []
        words = self.get_possible_words(word_text, word_database)
        for word in words:
            if word.root != '':
                roots.append(word.root)
        return roots
    
    def get_possible_roots_unknown(self, word_text):
        """ The same as get_possible_roots except do not restrict to known words/roots"""
        core_text = strip_harakaat(word_text)
        core_text = to_canonical_letters(core_text)
        if len(core_text) == 3:
            return[core_text]
        possible_roots = []
        added_letters = [TAA_MARBUTA, ALIF, WAAW, YAA, TAA, NUUN, SIIN, HAMZA, MIIM]
        for letter in added_letters:
            if letter in core_text:
                core_text = self._remove_last_letter(core_text, letter)
                if len(core_text) == 3:
                    return [core_text]
        return possible_roots
    
    def _remove_last_letter(self, text, letter):
        assert letter in text
        pos = text.rfind(letter)
        return text[0:pos] + text[pos+1:]
                
    def get_possible_roots_no_prefix_suffix(self, word_text):
        """ Get the possible roots for this word, which has no prefix or suffix"""
        roots = []
        if len(word_text) == 3:
            if word_text in self.roots:
                roots.append(word_text)
        return roots
    
    def get_possible_words(self, word_text, word_database):
        """ word can be a composite word, e.g. starting FAA or LAAM or ALIF+LAAM, or
        ending with a possessive.
        Return a list of all possible words that might be in the original word"""
        assert word_text == to_canonical_letters(word_text) 
        possible_words = []
        possible_inner_word_text_ops = self.inner_words.get_inner_word_texts(word_text)
        possible_inner_word_texts = [text for text, op_list in possible_inner_word_text_ops]
        possible_inner_word_texts = set(possible_inner_word_texts)
        for word_text in possible_inner_word_texts:
            for word in word_database.words_possibly_matching(word_text):
                try:
                    if word.matches(word_text):
                        possible_words.append(word)
                except Exception, ex:
                    l.exception('matching word')
        return possible_words
        
    @staticmethod
    def get_past_forms(verb_madi):
        past_forms = []
        assert(verb_madi.tense == WORD_TENSE_PAST)
        word_text = verb_madi.text
        # remove trailing fatha
        if word_text.endswith(FATHA):
            word_text = word_text[:-1]
        word_type = verb_madi.word_type
        root = verb_madi.root
        suffixes = [(SUKUUN + TU, 'I'),
                    (SUKUUN + TA, 'you (m)'),
                    (SUKUUN + TI, 'you (f)'),
                    (SUKUUN + NA, 'they (f)'),
                    (SUKUUN + UU, 'they (m)'),
                    (SUKUUN + NAA, 'we'),
                    (SUKUUN + TUM ,'you (m, pl)'),
                    (SUKUUN + TUMAA, 'you two'),
                    (AT, 'she'),
                    ]
        for suffix, pronoun in suffixes:
            past_form_text = word_text + suffix
            past_form = Word(word_type=word_type,
                             text=past_form_text,
                             root=root,
                             meaning='%s (%s)' % (verb_madi.meaning, pronoun))
            past_forms.append(past_form)
        return past_forms
    
    @staticmethod
    def get_present_forms(verb_mudari):
        present_forms = []
        assert(verb_mudari.tense == WORD_TENSE_PRESENT)
        word_text = verb_mudari.text
        # remove initial yaa
        if not word_text[0] == YAA:
            l.error('word should start with YAA: %s', verb_mudari.id)
            return []
        word_text = word_text[1:]
        if word_text.endswith(DAMMA):
            word_text = word_text[:-1]

        word_type = verb_mudari.word_type
        root = verb_mudari.root
        prefix_suffixes = [
                    (A, DAMMA, 'I'),
                    (TA, DAMMA, 'you (m)'),
                    (TA, IINA, 'you (f)'),
                    (YA, NA, 'they (f)'),
                    (YA, UUNA, 'they (m)'),
                    (NA, DAMMA, 'we'),
                    (TA, AANI ,'you two'),
                    (TA, UUNA ,'you (m, pl)'),
                    (TA, DAMMA, 'she'),
                    ]
        for prefix, suffix, pronoun in prefix_suffixes:
            present_form_text = prefix + word_text + suffix
            present_form = Word(word_type=word_type,
                             text=present_form_text,
                             root=root,
                             meaning='%s (%s)' % (verb_mudari.meaning, pronoun))
            present_forms.append(present_form)
        return present_forms
    
    def _nouns(self, words):
        return [word for word in words if word.is_noun()]
    
    
            
        