
import ar_logging
#ar_logging.add_std_out()
import unittest
import pickle

from sqlalchemy import create_engine

from data.unicode_data import *
from sarf_service.constants import *

from vocab_db_service.word_set import WordSet, Variation

from dictionary_service.sql_database.sql_database import SQLiteSQLDatabase

KALIMA_DATA = [
               (1, KAAF, TAA, BAA, 'to write',  WORD_TYPE_VERB, 1,
                 [(1, 1, KAAF + TAA + BAA, 0, 1),
                  (2, 1, YAA + KAAF + TAA + BAA + DAMMA, 0, 2)]),
                  
               (2, KAAF, TAA, BAA, 'book',  WORD_TYPE_NOUN, 1,
                [(5, 2, KAAF + TAA + ALIF + BAA, 1, 0),
                 (6, 2, KAAF + DAMMA + TAA + DAMMA + BAA, 3, 0)]),
               
               (3, KHAA, LAAM, QAAF, 'to create',  WORD_TYPE_VERB, 2,
                [(3, 3, KHAA + LAAM + QAAF, 0, 1),
                 (4, 3, YAA + KHAA + LAAM + QAAF, 0, 2),]),
               
               (4, '', '', '', 'in',  WORD_TYPE_PREPOSITION, 2,
                 [(7, 4, FAA + KASRA + YAA, 0, 0)]),
               
               (5, FAA, AYN, LAAM, 'to do',  WORD_TYPE_VERB, 1,
                [(8, 5, FAA + AYN + LAAM, 0, 1)]),
                
               (6, '', '', '', 'towards',  WORD_TYPE_PREPOSITION, 2,
                 [(9, 6, HAMZA_BELOW_ALIF + LAAM + ALIF_MAQSURA, 0, 0)]),
                 
                (7, '', '', '', 'that',  WORD_TYPE_PREPOSITION, 2,
                 [(10, 7, HAMZA_ABOVE_ALIF + NUUN, 0, 0)]),
                
               ]

USERS_DATA = [
              (1, 'alynch'),
              (2, 'rkayali'),
              ]

LINKS_DATA = [
              (1, 'www.alarabiya.net', 4, False),
              (1, 'www.aljazeera.net', 3, True),
              (2, 'news.bbc.co.uk/hi/arabic/news/', 3, True),
              ]

def _create_test_data(sql_database):
    
    for kalima_id, root_f, root_c, root_l, meaning, word_type, user_id, variations in KALIMA_DATA:
        word_set = WordSet(kalima_id=0,
                           root_f=root_f,
                           root_c=root_c,
                           root_l=root_l,
                           meaning=meaning,
                           word_type=word_type)
        
        for kalvar_id, kalima_id, text, number, tense in variations:
            word_set.variations.append(Variation(kalvar_id=0,
                                               text=text,
                                               number=number,
                                               tense=tense
                                               )) 
        sql_database.add_word_set(word_set, user_id)
        
    for user_id, nickname in USERS_DATA:
        sql_database.add_test_user(user_id, nickname)
        
    for user_id, url, difficulty, public in LINKS_DATA:
        sql_database.add_link(user_id, url, difficulty, public)
        
def create_test_sql_database():
    engine = create_engine('sqlite://') 
    database = SQLiteSQLDatabase(engine)
    _create_test_data(database)
    return database
        

class TestMemoryDatabase(unittest.TestCase):
    
    def setUp(self):
        self.database = create_test_sql_database()
        
    def test_instantiate_database(self):
        self.assert_(self.database)
        
    def test_preferences_pickle(self):
        preferences = {u'central_text_font_size': u'24',
                       u'central_text_font_family': u'Simplified Arabic'}
        preferences_pickle = pickle.dumps(preferences)
        depick = pickle.loads(preferences_pickle)
        self.database.set_preferences(1, preferences_pickle)
        
        preferences_pickle_2 = self.database.get_user_details(1)['preferences_pickle']
        self.assertEquals(preferences_pickle, preferences_pickle_2)
        preferences_2 = pickle.loads(preferences_pickle_2)
        self.assertEquals(preferences, preferences_2)
        
    def test_add_vocabulary_word(self):
        self.database.add_vocabulary_word(2, 3)
        vocabulary_details = self.database.get_vocabulary_details(2)
        vocabulary_details = [(x,y) for (x,y,z) in vocabulary_details]
        self.assertEquals(vocabulary_details, [(3, 1)])
        self.database.add_vocabulary_word(2, 3)
        vocabulary_details = self.database.get_vocabulary_details(2)
        vocabulary_details = [(x,y) for (x,y,z) in vocabulary_details]
        self.assertEquals(vocabulary_details, [(3, 2)])
        self.database.add_vocabulary_word(2, 4)
        vocabulary_details = self.database.get_vocabulary_details(2)
        vocabulary_details = [(x,y) for (x,y,z) in vocabulary_details]
        self.assert_((3, 2) in vocabulary_details)
        self.assert_((4, 1) in vocabulary_details)
        self.assertEquals(len(vocabulary_details), 2)
        
    def test_public_links(self):
        public_links = self.database.get_public_links()
        self.assertEquals(len(public_links), 2)
        link_urls = [link['url'] for link in public_links]
        self.assertEquals(set(['www.aljazeera.net', 'news.bbc.co.uk/hi/arabic/news/']),
                          set(link_urls))
        
    def test_user_links(self):
        user_links = self.database.get_user_links(1)
        self.assertEquals(len(user_links), 2)
        link_urls = [link['url'] for link in user_links]
        self.assertEquals(set(['www.aljazeera.net', 'www.alarabiya.net']),
                          set(link_urls))
        
    def test_get_user(self):
        user_details = self.database.get_user_details(2)
        self.assertEquals(user_details['user_id'], 2)
        self.assertEquals(user_details['nickname'], 'rkayali')
        user_details = self.database.get_user_details(200)
        self.assertEquals(user_details, None)
        
    def test_get_words(self):
        words = self.database.get_words()
        for word in words:
            self.assert_(word.id > 0)
            self.assert_(word.kalima_id > 0)
            self.assert_(word.text != '')
        
    def test_get_next_kalima_id(self):
        next_id = self.database.get_next_kalima_id(1)
        self.assertEquals(next_id, 2)
        next_id = self.database.get_next_kalima_id(3)
        self.assertEquals(next_id, 4)
        next_id = self.database.get_next_kalima_id(7)
        self.assertEquals(next_id, None)
        next_id = self.database.get_next_kalima_id(10)
        self.assertEquals(next_id, None)
        
    def test_get_previous_kalima_id(self):
        next_id = self.database.get_previous_kalima_id(1)
        self.assertEquals(next_id, None)
        next_id = self.database.get_previous_kalima_id(3)
        self.assertEquals(next_id, 2)
        next_id = self.database.get_previous_kalima_id(4)
        self.assertEquals(next_id, 3)
        
    def test_delete_kalima(self):
        self.database.delete_kalima(1, 1)
        
    def test_get_kalvars_for_kalima_id(self):
        kalvars = self.database._get_kalvars_for_kalima_id(2)
        
    def test_update_word_set(self):
        words = self.database.get_words()
        word_kv1 = [word for word in words if word.id == 1][0]
        kalima_id = word_kv1.kalima_id
        words_k1 = [word for word in words if word.kalima_id == kalima_id]
        orig_num_words = len(words_k1)
        
        word_set = WordSet(kalima_id=kalima_id,
                           meaning=word_kv1.meaning + 'modified',
                           root_f=word_kv1.root[0],
                           root_c=word_kv1.root[1],
                           root_l=word_kv1.root[2],
                           word_type=word_kv1.word_type)
        for word in words_k1:
            variation = Variation(kalvar_id=word.id,
                                  tense=word.tense,
                                  number=word.number,
                                  text=word.text + KAAF + KAAF + KAAF)
            word_set.variations.append(variation)
            
        # add new variation
        new_variation = Variation(kalvar_id=0,
                                  tense=1,
                                  number=0,
                                  text= JIIM + LAAM)
        word_set.variations.append(new_variation)
            
        self.database.update_word_set(word_set, 1)
        
        words = self.database.get_words()
        word_kv1 = [word for word in words if word.id == 1][0]
        words_k1 = [word for word in words if word.kalima_id == kalima_id]
        self.assertEquals(len(words_k1), orig_num_words + 1)
        self.assert_(word_kv1.meaning.endswith('modified') )
        self.assert_(word_kv1.text.endswith(KAAF + KAAF + KAAF) )
        
        # remove a word from the word set and check the total number of words goes down
        
        word_set.variations.pop()
        self.database.update_word_set(word_set, 1)
        words = self.database.get_words()
        words_k1 = [word for word in words if word.kalima_id == kalima_id]
        self.assertEquals(len(words_k1), orig_num_words)
        
        