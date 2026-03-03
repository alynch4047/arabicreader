
import ar_logging
import unittest

import config
from project_roots_online_service.pro_html_parser import PROHTMLParser

HTML_DIR = config.PRO_DIR

from data.unicode_data import *


class TestPROHTMLParser(unittest.TestCase):
        
    def test_get_files_and_parse(self):
        parser = PROHTMLParser(pro_html_directory=HTML_DIR)
        files = parser._get_html_files(HTML_DIR)
        self.assert_('10_JIIM.htm' in files)
        found_roots = parser.root_meanings_dict.keys()
        RHM = RAA+HAA_+MIIM
        self.assert_(RHM in found_roots)
        

