

import unittest

from quran_service.quran_xml_reader import QuranXMLReader

import config
reader = QuranXMLReader(config.QURAN_DATA_LOC)


class TestQuranXMLReader(unittest.TestCase):
        
    def test_get_ayat(self):
        ayat = reader.get_ayat_text(12, 20)
