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

from vocabulary_pdf.shape import shape, shaddas_before_harakaat

l = logging.getLogger(__name__)

def check_is_presentation_arabic(text):
    for letter in text:
        if ord(letter) < 0xfe70 or ord(letter) > 0xfeff:
            raise Exception('not presentation arabic: %s %s', text, letter)


class TestShape(unittest.TestCase):
    
    
    def test_shape(self):
        KITAABA = KAAF + KASRA + TAA + FATHA + ALIF + BAA + TAA_MARBUTA
        l.debug('%s', transliterate_to_gb(KITAABA))
        text = shape(KITAABA)
        check_is_presentation_arabic(text)
        
    def test_shaddas_before_harakaat(self):
        text = KAAF + FATHA + SHADDA
        text_out = shaddas_before_harakaat(text)
        self.assertEquals(text_out, KAAF + SHADDA + FATHA)
