
import logging
from datetime import datetime

from traits.api import HasTraits, Interface, implements
from traits.api import Instance, Any, Str, List, Dict

from dictionary_service.api import WordDatabase, SQLDatabase
from session_service.api import Session
from vocab_db_service.api import make_word_set_from_words

l = logging.getLogger(__name__)


class Vocabulary(HasTraits):
    
    session = Instance(Session)
    
    word_database = Instance(WordDatabase)
    
    sql_database = Instance(SQLDatabase)
    
    kalima_count_datetimes = List # of (kalima_id, click_count, last_click_datetime) tuples
    
    def get_all_word_ids(self):
        if self.session.is_guest():
            kalima_count_datetimes = self.kalima_count_datetimes
        else:
            kalima_count_datetimes = self.sql_database.get_vocabulary_details(
                                                                    self.session.user_id)
        return self._get_json_data_for_kalima_count_datetimes(kalima_count_datetimes)
        
    def get_all_words_grouped_by_kalima(self):
        kalima_count_datetimes = self.sql_database.get_vocabulary_details(
                                                                    self.session.user_id)
        words_grouped_by_kalima = {}
        for kalima_id, click_count, last_click_datetime in kalima_count_datetimes:
            words_grouped_by_kalima[kalima_id] = self.word_database.words_by_kalima[kalima_id]
        return words_grouped_by_kalima
    
    def add_word(self, kalima_id):
        l.debug('add word of kalima id %s to vocab', kalima_id)
        if self.session.is_guest():
            self.kalima_count_datetimes.append((int(kalima_id), 1, datetime.now()))
        else:
            self.sql_database.add_vocabulary_word(self.session.user_id, kalima_id) 
        return [kalima_id]
    
    def remove_word(self, kalima_id):
        l.debug('remove word of kalima id %s from vocab', kalima_id)
        self.sql_database.remove_vocabulary_word(self.session.user_id, kalima_id) 
        return []
    
    def _get_json_data_for_kalima_count_datetimes(self, kalima_count_datetimes):
        json_data = []
        for kalima_id, click_count, last_click_datetime in kalima_count_datetimes:
            words_for_kalima = self.word_database.words_of_kalima_id(kalima_id)
            word_set = make_word_set_from_words(words_for_kalima)
            json_data.append(word_set.get_data_for_json())
        return json_data
    
