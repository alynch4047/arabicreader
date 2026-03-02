
import logging

from traits.api import Instance

from transactions.api import TransactionQueue
from server.api import Handler
from sarf_service.api import to_canonical_letters

from dictionary_service.dictionary import IDictionary

l = logging.getLogger(__name__)


class DictionaryHandler(Handler):
    
    dictionary = Instance(IDictionary)
    
    transaction_queue = Instance(TransactionQueue)
    
    def _url_lookup_default(self):
        lookup = {
                  'wordsofsameroot': self._get_words_of_same_root,
                  'wordsofroot': self._get_words_of_root,
                  'unknownwords': self._unknown_words,
                  'wordsetsmatchingtext': self._word_sets_matching_text,
        }
        return lookup
    
    def _get_words_of_root(self, root_text, session):
        root_text = to_canonical_letters(root_text)
        l.debug('_get_words_of_root for root %s', repr(root_text))
        words_of_same_root = self.dictionary.get_words_of_root(root_text)
        word_sets_data = self._get_word_sets(words_of_same_root)
        return [(root_text, word_sets_data)]
    
    def _get_words_of_same_root(self, word_text, session):
        """ Return a list of wordsets by root """
        l.debug('_get_words_of_same_root (a) for word %s', repr(word_text))
        word_text = to_canonical_letters(word_text)
        l.debug('_get_words_of_same_root for word %s', repr(word_text))
        words_of_same_root = self.dictionary.get_words_of_same_root(word_text)
        data = []
        for root in words_of_same_root:
            word_sets_data = self._get_word_sets(words_of_same_root[root])
            data.append((root, word_sets_data))
        return data
            
    def _get_word_sets(self, words):
        """ Return a list of word sets based on the passed-in list of words"""
        from vocab_db_service.api import make_word_set_from_words
        # words can come from disparate kalima
        data = []
        words_by_kalima_id = self._categorise_by_kalima(words)
        for kalima_id in words_by_kalima_id:
            words_of_kalima_id = words_by_kalima_id[kalima_id]
            data.append(make_word_set_from_words(words_of_kalima_id).get_data_for_json())
        return data
    
    def _categorise_by_kalima(self, word_list):
        words_by_kalima = {}
        for word in word_list:
            if word.kalima_id not in words_by_kalima:
                words_by_kalima[word.kalima_id] = []
            words_by_kalima[word.kalima_id].append(word)
        return words_by_kalima
    
    def _word_sets_matching_text(self, word_text, session):
        word_text = to_canonical_letters(word_text)
        words = self.dictionary.get_words_matching_text(word_text)
        return self._get_word_sets(words)
    
    def _get_meanings_for_word(self, word_text, session):
        word_text = to_canonical_letters(word_text)
        return self.dictionary.get_meanings_for_word(word_text)

    def _unknown_words(self, data, session, words=[]):
        unknown_words = {}
        for word_text in words:
            canonical_word_text = to_canonical_letters(word_text)
            try:
                meanings = self.dictionary.get_meanings_for_word(canonical_word_text)
                if len(meanings) == 0:
                    unknown_words[word_text] = True
            except Exception as ex:
                l.error('checking unknown words')
        return unknown_words
    

            
            
    