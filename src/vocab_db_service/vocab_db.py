
import logging

from traits.api import HasTraits, Str, Int, Instance, CInt, List, Dict

from dictionary_service.api import IDictionary, WordDatabase

from vocab_db_service.word_set import WordSet, make_word_set_from_args

l = logging.getLogger(__name__)


class WordAdder(HasTraits):
    
    dictionary = Instance(IDictionary)
    
    word_database = Instance(WordDatabase)
    
    def delete_kalima(self, url, session):
        kalima_id = int(url)
        self.word_database.delete_kalima(kalima_id, session)
        previous_id = self.get_previous_kalima_id(kalima_id)
        return previous_id
    
    def get_next_kalima_id(self, url, **kwargs):
        kalima_id = int(url)
        if 'filter' in kwargs:
            filter = kwargs['filter']
        else:
            filter = None
        next_kalima_id = self.word_database.get_next_kalima_id(kalima_id, filter)
        return next_kalima_id
    
    def get_last_kalima_id(self, url):
        last_kalima_id = self.word_database.get_last_kalima_id()
        return last_kalima_id
    
    def get_previous_kalima_id(self, url, **kwargs):
        kalima_id = int(url)
        if 'filter' in kwargs:
            filter = kwargs['filter']
        else:
            filter = None
        previous_kalima_id = self.word_database.get_previous_kalima_id(kalima_id, filter)
        return previous_kalima_id
    
    def get_variation_for_kalvar_id(self, url):
        try:
            word_id = int(url)
        except ValueError:
            l.exception('invalid word id (%s)' % url)
            raise Exception('Invalid kalima id')
        word = self.word_database.words_by_id[word_id]
        kalima_id = word.kalima_id
        return self.get_variations_for_kalima_id(kalima_id)

    def get_variations_for_kalima_id(self, kalima_id):
        try:
            kalima_id = int(kalima_id)
        except ValueError:
            l.exception('invalid kalima_id (%s)' % kalima_id)
            return []
        words = self.word_database.words_of_kalima_id(kalima_id)
        first_word = words[0]
        root = first_word.root
        word_type = first_word.word_type
        meaning = first_word.meaning
        nickname = first_word.nickname
        words_data = []
        for word in words:
            word_data = [word.id, word.text, word.tense, word.number, word.gender]
            words_data.append(word_data)
        l.debug('return %s', [kalima_id, root, word_type, meaning, nickname, words_data])
        return [kalima_id, root, word_type, meaning, nickname, words_data]
    
    def add_word_set(self, url, session, **kwargs):
        word_set = make_word_set_from_args(kwargs)
        word_set.validate()
        assert(word_set.kalima_id == 0)
        new_kalima_id = self.word_database.add_word_set(word_set, session)
        num_added = len(word_set.variations)
        return str(num_added), new_kalima_id
        
    def update_word_set(self, url, session, **kwargs):
        word_set = make_word_set_from_args(kwargs)
        assert(word_set.kalima_id != 0)
        word_set.validate()
        self.word_database.update_word_set(word_set, session)
        num_updated = len(word_set.variations)
        return str(num_updated)

       
        
