# -*- coding: utf-8 -*-

import ar_logging; ar_logging.add_std_out()
import logging
import unittest
import os

from bs4 import UnicodeDammit, BeautifulSoup


class TestUnicodeDammit(unittest.TestCase):
    
   def test_aljazeera(self):
       from proxy_service import test
       package_dir = os.sep.join(test.__file__.split(os.sep)[:-1])
       al_jazeera_html_path = os.path.join(package_dir, 'aljazeera.html')
       xml = open(al_jazeera_html_path, 'rb').read()
       ucd = UnicodeDammit(xml, is_html=True)
       self.assertEquals(ucd.original_encoding, 'windows-1256')
       
   def test_small_aljazeera(self):
       from proxy_service import test
       package_dir = os.sep.join(test.__file__.split(os.sep)[:-1])
       al_jazeera_html_path = os.path.join(package_dir, 'small_aljazeera.html')
       xml = open(al_jazeera_html_path, 'rb').read()
       
       soup = BeautifulSoup(xml, isHTML=True)
       print(str(soup))
       