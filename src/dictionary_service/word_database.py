
import logging
import threading

from traits.api import HasTraits, List, Dict, Instance, provides

from data.unicode_data import ALIF, HAMZA
from sarf_service.api import IWord, to_core_letters

from dictionary_service.i_word_database import IWordDatabase                             
from dictionary_service.sql_database.sql_database import SQLDatabase                 
 
l = logging.getLogger(__name__)


@provides(IWordDatabase)
class WordDatabase(HasTraits):
    
    sql_database = Instance(SQLDatabase)
    
    words_by_root = Dict # (key_trait=Root, value_trait=List(Word))
    
    words = List(IWord)
    
    words_by_id = Dict # words by kalvar_id
    
    words_by_kalima = Dict # words by kalima_id
    
    _words_by_letter = Dict

    _lock = threading.Lock()
    
    def __init__(self, **traits):
        super(WordDatabase, self).__init__(**traits)
        l.info('create word database')
        
        self.words = self.sql_database.get_words()
        self.words_by_id = self._get_words_by_id()
        self.words_by_root = self._get_words_by_root()
        self.words_by_kalima = self._get_words_by_kalima()
        self._initialise_words_by_letter()
        
    def add_word_set(self, word_set, session):
        new_kalima_id = self.sql_database.add_word_set(word_set, session.user_id)
        words = word_set.get_words()
        for word in words:
            self.add_word(word, session.user_id, session.nickname)
        return new_kalima_id
            
    def delete_kalima(self, kalima_id, session):
        self.sql_database.delete_kalima(kalima_id, session.user_id)
        words = self.words_by_kalima[kalima_id]
        for word in words:
            self.remove_word(word)
        del self.words_by_kalima[kalima_id]
        
    def remove_word(self, word):
        self.words.remove(word)
        del self.words_by_id[word.id]
        self.words_by_root[word.root].remove(word)
        self.words_by_kalima[word.kalima_id].remove(word)
        self._remove_word_from_words_by_letter(word)
    
    def update_word_set(self, word_set, session):
        self.sql_database.update_word_set(word_set, session.user_id)
        words = word_set.get_words()
        for word in words:
            if word.id in self.words_by_id:
                self.replace_word(word.id, word, session)
            else:
                self.add_word(word, session.user_id, session.nickname)
        
    def replace_word(self, kalvar_id, word, session):
        """
        For the given kalvar_id, replace the word with the given (changed) word
        """
        original_word = self.words_by_id[kalvar_id]
        original_creator_id = original_word.creator_id
        original_nickname = original_word.nickname
        self.remove_word(original_word)
        self.add_word(word, original_creator_id, original_nickname)
            
    def add_word(self, word, user_id, nickname):
        WordDatabase._lock.acquire()
        word.creator_id = user_id
        word.nickname = nickname
        try:
            self.words.append(word)
            if word.root not in self.words_by_root:
                self.words_by_root[word.root] = []
            self.words_by_root[word.root].append(word)
            self.words_by_id[word.id] = word
            self._add_word_to_words_by_letter(word)
            if word.kalima_id not in self.words_by_kalima:
                self.words_by_kalima[word.kalima_id] = []
            self.words_by_kalima[word.kalima_id].append(word)
        finally:
            WordDatabase._lock.release()
    
    def words_of_kalima_id(self, kalima_id):
        return self.words_by_kalima[kalima_id]
    
    def get_next_kalima_id(self, kalima_id, filter=None):
        next_id = self.sql_database.get_next_kalima_id(kalima_id, filter)
        if next_id is None:
            return None
        l.debug('next kalima id after %s is %s', kalima_id, next_id)
        return next_id
    
    def get_last_kalima_id(self):
        last_id = self.sql_database.get_last_kalima_id()
        if last_id is None:
            return None
        l.debug('last_id kalima id is %s', last_id)
        return last_id
    
    def get_previous_kalima_id(self, kalima_id, filter=None):
        previous_id = self.sql_database.get_previous_kalima_id(kalima_id, filter)
        if previous_id is None:
            return None
        return previous_id
    
    def words_possibly_matching(self, word_text):
        """ Get words that might match the given word. DO as efficiently as possible"""
        if word_text:
            word_text = to_core_letters(word_text)
            first_letter = word_text[0]
            if first_letter == ALIF:
                # put ALIF and HAMZA in the same bucket
                first_letter = HAMZA
            if first_letter in self._words_by_letter:
                return self._words_by_letter[first_letter]
        return []
        
    def _add_word_to_words_by_letter(self, word):
        if word.text:
            first_letter = word.core_form[0]
            if first_letter == ALIF:
                # put ALIF and HAMZA in the same bucket
                first_letter = HAMZA
            if first_letter not in self._words_by_letter:
                self._words_by_letter[first_letter] = []
            self._words_by_letter[first_letter].append(word)
        else:
            raise Exception('no first letter')
            
    def _remove_word_from_words_by_letter(self, word):
        if word.text:
            first_letter = word.core_form[0]
            if first_letter == ALIF:
                # put ALIF and HAMZA in the same bucket
                first_letter = HAMZA
            if first_letter in self._words_by_letter:
                self._words_by_letter[first_letter].remove(word)
    
    def _initialise_words_by_letter(self):
        self._words_by_letter = {}
        for word in self.words:
            self._add_word_to_words_by_letter(word)
    
    def _get_words_by_id(self):
        words_by_id = {}
        for word in self.words:
            words_by_id[word.id] = word
        return words_by_id
            
    def _get_words_by_root(self):
        words_by_root = {}
        for word in self.words:
            root = word.root
            if root not in words_by_root:
                words_by_root[root] = []
            words_by_root[root].append(word)
        return words_by_root
    
    def _get_words_by_kalima(self):
        words_by_kalima = {}
        for word in self.words:
            if word.kalima_id not in words_by_kalima:
                words_by_kalima[word.kalima_id] = []
            words_by_kalima[word.kalima_id].append(word)
        return words_by_kalima
    

 

    

    