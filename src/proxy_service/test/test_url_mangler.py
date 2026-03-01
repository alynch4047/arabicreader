# -*- coding: utf-8 -*-

import ar_logging; ar_logging.add_std_out()
import logging
import unittest
import simplejson

from sarf_service.test.test_words import *

from proxy_service.url_mangler import URLMangler


class TestURLMangler(unittest.TestCase):
    
    def setUp(self):
        self.url_mangler = URLMangler()
        
    def test_get_document_url_dir(self):
        full_url = 'http://www.bbc.co.uk/test/test2/asbd.html'
        document_url_dir = self.url_mangler.get_document_url_dir(full_url)
        self.assertEquals(document_url_dir, 'http://www.bbc.co.uk/test/test2/')
        
        full_url = 'http://www.bbc.co.uk/test/test2/'
        document_url_dir = self.url_mangler.get_document_url_dir(full_url)
        self.assertEquals(document_url_dir, 'http://www.bbc.co.uk/test/test2/')
        
        full_url = 'http://www.bbc.co.uk/'
        document_url_dir = self.url_mangler.get_document_url_dir(full_url)
        self.assertEquals(document_url_dir, 'http://www.bbc.co.uk/')
        
    def test_get_absolute_url(self):
        document_dir_url = 'http://www.bbc.co.uk/test/'
        url = 'http://www.bbc.co.uk/test/asbd.html'
        new_url = self.url_mangler.get_absolute_url(document_dir_url, url)
        self.assertEquals(new_url, 'http://www.bbc.co.uk/test/asbd.html')
        
        url = 'asbd.html'
        new_url = self.url_mangler.get_absolute_url(document_dir_url, url)
        self.assertEquals(new_url, 'http://www.bbc.co.uk/test/asbd.html')
        
        url = 'test2/asbd.html'
        new_url = self.url_mangler.get_absolute_url(document_dir_url, url)
        self.assertEquals(new_url, 'http://www.bbc.co.uk/test/test2/asbd.html')
        
        url = '/asbd.html'
        new_url = self.url_mangler.get_absolute_url(document_dir_url, url)
        self.assertEquals(new_url, 'http://www.bbc.co.uk/asbd.html')
        
    def get_site_url(self):
        url = 'http://www.bbc.co.uk/test/asbd.html'
        site_url = self.url_mangler.get_site_url(url)
        self.assertEquals(site_url, 'http://www.bbc.co.uk/')
        
        url = 'http://www.bbc.co.uk'
        site_url = self.url_mangler.get_site_url(url)
        self.assertEquals(site_url, 'http://www.bbc.co.uk/')
        
        url = 'http://www.bbc.co.uk/'
        site_url = self.url_mangler.get_site_url(url)
        self.assertEquals(site_url, 'http://www.bbc.co.uk/')
        
   