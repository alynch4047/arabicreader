# -*- coding: utf-8 -*-

import ar_logging; ar_logging.add_std_out()
import logging
import unittest
import os

from proxy_service.BeautifulSoup import UnicodeDammit, BeautifulSoup


class TestUnicodeDammit(unittest.TestCase):
    
   def test_aljazeera(self):
       from proxy_service import test
       package_dir = os.sep.join(test.__file__.split(os.sep)[:-1])
       al_jazeera_html_path = os.path.join(package_dir, 'aljazeera.html')
       xml = file(al_jazeera_html_path).read()
       ucd = UnicodeDammit(xml, isHTML=True)
       markup, document_encoding, sniffed_encoding = \
                     ucd._detectEncoding(xml, True)
       #print document_encoding, sniffed_encoding 
       self.assertEquals(document_encoding, 'windows-1256')
       
   def test_small_aljazeera(self):
       from proxy_service import test
       package_dir = os.sep.join(test.__file__.split(os.sep)[:-1])
       al_jazeera_html_path = os.path.join(package_dir, 'small_aljazeera.html')
       xml = file(al_jazeera_html_path).read()
       
       soup = BeautifulSoup(xml, isHTML=True)
       print unicode(soup)
       