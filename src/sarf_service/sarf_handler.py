
import logging

from traits.api import HasTraits, Instance

from server.api import Handler
from sarf_service.word_mangler import to_canonical_letters 

from sarf_service.sarf import Sarf

l = logging.getLogger(__name__)


class SarfHandler(Handler):
    
    sarf = Instance(Sarf, ())
    
    def _url_lookup_default(self):
        lookup = {
                  'possibleroots': self._get_possible_roots,
                  'possiblewordtexts': self._get_possible_word_texts,
        }
        return lookup
    
    def _get_possible_roots(self, word_text, session=None):
        word_text = to_canonical_letters(word_text)
        return self.sarf.get_possible_roots_unknown(word_text)
    
    def _get_possible_word_texts(self, word_text, session=None):
        """ get all possible word_texts for a word by removing all possible
        variations of prefix/suffix etc, whether the word_text is known or not"""
        word_text = to_canonical_letters(word_text)
        l.debug('get possible word text for word %s', repr(word_text))
        return self.sarf.inner_words.get_inner_word_texts(word_text)
            

   