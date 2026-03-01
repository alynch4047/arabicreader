import logging

from sarf_service.api import to_canonical_letters

from vocabulary_pdf.constants import LATIN_FONT_SIZE, ARABIC_FONT_SIZE, ALIGN_LEFT
from vocabulary_pdf.utils import (reverse_phrase, unicode_to_baghdad, encode_text,
                                  get_string_width, strip_tashkeel_with_location)
from vocabulary_pdf.postscript import PostScript
from vocabulary_pdf.shape import shape

l = logging.getLogger(__name__)

JOIN_NONE = 0
JOIN_RIGHT = 1
JOIN_LEFT = 2
JOIN_DUAL = 3
JOIN_TRANSPARENT = 4
JOIN_STRIP_OUT = 5


class Printer(object):
    
    def __init__(self, file_handle):
        self.file_handle = file_handle
        self.postscript = PostScript(file_handle)

    def initialiseRenderer(self):
        self.postscript.postscriptProlog()
        
    def finaliseRenderer(self):
        self.file_handle.close()
    
    def printAtPS(self, x,y,text, align, fontAbbrev='FT'):
        # postscript printing method, assume prolog and epilog handled elsewhere
        stringWidth = get_string_width(text, LATIN_FONT_SIZE)
        if align == ALIGN_LEFT:
            xOffset = 0
        else:
            xOffset = stringWidth
        self.postscript.psOut(str(LATIN_FONT_SIZE) + ' ' + fontAbbrev + '\n' +
                               str(x - xOffset) + 
                               ' ' + str(y) + ' moveto \n(' + text + ') show')
        return stringWidth
    
    def printComment(self, comment):
        self.postscript.psOut('% ' + comment + '\n')
        
    def printNewPage(self):
        self.postscript.psOut('showpage\n')
        
    def printAtPSArabic(self, x, y, text):
        # make shaddas come after any harakat
        text = to_canonical_letters(text)
        text = shape_phrase(text)
        xOffset = get_string_width(text, ARABIC_FONT_SIZE)
        # strip out Harakaat for printing separately
        harakaat_location, stripped_text = strip_tashkeel_with_location(x, y, text)
        text = reverse_phrase(stripped_text)
        baghdad_text = encode_text(text)
        self.postscript.psOut(str(ARABIC_FONT_SIZE) + ' FB\n' + str(x - xOffset) + ' '
                                    + str(y) + ' moveto \n(' + baghdad_text + ') show')
        for h in harakaat_location:
            haraka = h[1]
            x = h[2]
            y = h[3]
            haraka = unichr(unicode_to_baghdad(ord(haraka)))
            self.postscript.psOut(str(ARABIC_FONT_SIZE) + ' FB\n' + str(x) + ' ' +
                                    str(y) + ' moveto \n(' + haraka + ') show')


def getArabicWidth(text):
    text = shape_phrase(text)
    return get_string_width(text, ARABIC_FONT_SIZE)


def shape_phrase(text):
    ret = ''
    words = text.split()
    for i in range(len(words)):
        word = words[i]
        if ret != '':
            ret += ' '
        ret += shape(word)
    return ret


