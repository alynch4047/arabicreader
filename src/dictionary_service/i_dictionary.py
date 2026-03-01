
from traits.api import Interface, List, Dict

from sarf_service.api import IWord


class IDictionary(Interface):
    
    words_by_root = Dict #(key_trait=Root, value_trait=List(Word))
    
    words = List(IWord)

    def get_words_of_same_root(self, word_text):
        """ return a dictionary of Root ->[Words] that have the same root
        as the word (there may be more than one possible root)"""
        
    def get_words_of_root(self, root_text):
        """"""
        
    def get_meanings_for_word(self, word_text):
        """ get all possible meanings for a word string"""