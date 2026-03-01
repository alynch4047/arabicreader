import logging

import simplejson

from traits.api import HasTraits, Instance

from dictionary_service.api import IDictionary, IWordDatabase
from server.api import Handler

from vocab_db_service.vocab_db import WordAdder

l = logging.getLogger(__name__)


class VocabDBHandler(Handler):
    
    dictionary = Instance(IDictionary)
    
    word_database = Instance(IWordDatabase)
    
    word_adder = Instance(WordAdder)
    
    def _url_lookup_default(self):
        lookup = {
                  'addwordset': self._add_word_set,
                  'getvariation': self.get_variations_for_kalima_id,
                  'getvariationforkalvarid': self._get_variation_for_kalvar_id,
                  'updatewordset': self._update_word_set,
                  'getnextkalima': self._get_next_kalima_id,
                  'getpreviouskalima': self._get_previous_kalima_id,
                  'getlastkalima': self._get_last_kalima_id,
                  'deletekalima': self._delete_kalima,
        }
        return lookup
    
    def _word_adder_default(self):
        return WordAdder(dictionary=self.dictionary,
                         word_database=self.word_database)
            
    def _add_word_set(self, url, session, **kwargs):
        if not session.authenticated:
            raise Exception('cannot change database - not authenticated')
        return self.word_adder.add_word_set(url, session, **kwargs)
    
    def _update_word_set(self, url, session, **kwargs):
        if not session.authenticated:
            raise Exception('cannot change database - not authenticated')
        return self.word_adder.update_word_set(url, session, **kwargs)
    
    def get_variations_for_kalima_id(self, url, session):
        return self.word_adder.get_variations_for_kalima_id(url)

    def _get_variation_for_kalvar_id(self, url, session):
        return self.word_adder.get_variation_for_kalvar_id(url)
    
    def _delete_kalima(self, url, session):
        if not session.authenticated:
            raise Exception('cannot change database - not authenticated')
        return self.word_adder.delete_kalima(url, session)
    
    def _get_next_kalima_id(self, url, session, **kwargs):
        return [self.word_adder.get_next_kalima_id(url, **kwargs)]
    
    def _get_last_kalima_id(self, url, session, **kwargs):
        return [self.word_adder.get_last_kalima_id(url, **kwargs)]
    
    def _get_previous_kalima_id(self, url, session, **kwargs):
        return [self.word_adder.get_previous_kalima_id(url, **kwargs)]
    

      
