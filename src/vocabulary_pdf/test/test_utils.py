import unittest
import logging

root_logger = logging.getLogger()
root_logger.level = logging.DEBUG
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
hdlr = logging.StreamHandler()
hdlr.setFormatter(formatter)
root_logger.addHandler(hdlr)

from data.unicode_data import *
from sarf_service.api import transliterate_to_gb 

from vocabulary_pdf.shape import shape
from vocabulary_pdf.utils import (strip_tashkeel_with_location, 
                                  unicode_to_baghdad, TASHKEEL)

l = logging.getLogger(__name__)

def check_is_presentation_arabic(text):
    for letter in text:
        if ord(letter) < 0xfe70 or ord(letter) > 0xfeff:
            raise Exception('not presentation arabic: %s %s', text, letter)


class TestUtils(unittest.TestCase):
    
    def test_unicode_to_baghdad(self):
        text = 0xfe76
        baghdad_code = unicode_to_baghdad(text)
        self.assertEquals(baghdad_code, 56)
    
    def test_strip_tashkeel_with_location(self):
        KITAABA = KAAF + KASRA + TAA + FATHA + ALIF + BAA + TAA_MARBUTA
        l.debug('%s', transliterate_to_gb(KITAABA))
        text = shape(KITAABA)
        check_is_presentation_arabic(text)
        harakaat, text = strip_tashkeel_with_location(100, 100, text)
        l.debug('stripped text is %s', text)
        l.debug('%s', transliterate_to_gb(text))
        l.debug('tashkeel is %s', harakaat)
        
