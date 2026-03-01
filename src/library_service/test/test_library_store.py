# -*- coding: utf-8 -*-

import tempfile
import shutil
from io import StringIO
import logging

import ar_logging
#ar_logging.add_std_out()
import unittest

from library_service.library_store import LibraryStore

TEST_DATA = u'this is a test file سلام'
TEST_DATA_UTF8 = TEST_DATA.encode('utf8')


class TestLibraryStore(unittest.TestCase):
    
    def setUp(self):
        self.store_root_path = tempfile.mkdtemp('ar_test')
        self.library_store = LibraryStore(root_path=self.store_root_path)
        
    def tearDown(self):
        try:
            shutil.rmtree(self.store_root_path)
        except:
            l.exception()
            
    def test_save_file_for_user_then_retrieve(self):
        TITLE = 'Title A'
        AUTHOR_ID = 2
        f = StringIO.StringIO(TEST_DATA_UTF8)
        self.library_store.save_file(AUTHOR_ID, TITLE, f)
        available_titles = self.library_store.get_available_titles(AUTHOR_ID)
        self.assertEquals(available_titles, [TITLE])
        
        # retrieve file
        f2 = self.library_store.get_file(AUTHOR_ID, TITLE)
        data = f2.read()
        self.assertEquals(data,TEST_DATA)
        
    def test_get_file_page_data(self):
        TITLE = 'Title B'
        AUTHOR_ID = 2
        f = StringIO.StringIO(TEST_DATA_UTF8)
        self.library_store.save_file(AUTHOR_ID, TITLE, f)
        
        res = \
                            self.library_store.get_file_page_data(AUTHOR_ID, TITLE, 0)
        self.assertEquals(res['text'], TEST_DATA)
        self.assertEquals(res['num_pages'], 1)
        self.assertEquals(res['further_pages_available'], False)
