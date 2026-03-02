
import unittest

from data.unicode_data import *

KALB = KAAF + LAAM + BAA
FAKATABA = FAA + KAAF + TAA + BAA

from sarf_service.root import RootMeaning


class TestRoot(unittest.TestCase):
        
    def test_roots(self):
        root_meaning = RootMeaning(root=KALB)
        root_meaning.meaning= 'this is a word meaning'