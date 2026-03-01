# coding=utf-8

import ar_logging
import unittest
import urllib

from data.unicode_data import *
from sarf_service.test.test_words import *
from sarf_service.api import Word

from dictionary_service.api import (IDictionary, Dictionary, create_test_word_database)

from vocab_db_service.vocab_db import WordAdder

import logging
l = logging.getLogger(__name__)


class TestWordAdder(unittest.TestCase):

    def setUp(self):
        word_database = create_test_word_database()
        dictionary = Dictionary(word_database=word_database)
        self.word_adder = WordAdder(dictionary=dictionary,
                                    word_database=word_database)
        
    def test_process_url(self):
        url = """form/json?kalima_id=New&word_type=1&root_f=%D9%85&root_c=%D8%B9&root_l=%D8%AF&meaning=helper&kalvar_id_3=new&tense_3=1&number_3=1&text_3=%D9%85%D8%B3%D8%A7%D8%B9%D8%AF"""
        url = urllib.unquote(url)
        url = unicode(url, encoding='utf-8')
        class Session(object):
            def __init__(self):
                self.user_id = 1
        session = Session()
        self.word_adder.add_word_set(url, session)
        
        url2 = """"""

        