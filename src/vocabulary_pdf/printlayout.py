import logging

from vocabulary_pdf.constants import (ALIGN_LEFT, PAGE_SIZE_HORIZONTAL, PAGE_SIZE_VERTICAL,
                       BOOK_TITLE, LATIN_FONT_SIZE)
from vocabulary_pdf.printer import Printer, getArabicWidth
from vocabulary_pdf.utils import get_string_width


class PrintLayout(object):
    
    def __init__(self, file_handle):
        self.printer = Printer(file_handle)

    def printPageNumber(self, pageNo):
        self.printAt(PAGE_SIZE_HORIZONTAL / 2.0, PAGE_SIZE_VERTICAL - 15, str(pageNo))
    
    def printTitle(self):
        self.printAt(PAGE_SIZE_HORIZONTAL / 2.0 - get_string_width(BOOK_TITLE, LATIN_FONT_SIZE)/2.0,
                                 5, BOOK_TITLE)
    
    def printAt(self, x, y, text, align=ALIGN_LEFT, fontAbbrev='FT'):
        assert(y < PAGE_SIZE_VERTICAL)
        y = PAGE_SIZE_VERTICAL - y
        self.printer.printAtPS(x, y, text, align, fontAbbrev)
        
    def arabicWidth(self, text):
        return getArabicWidth(text)
       
    def printAtArabic(self, x, y, text):
        assert(y < PAGE_SIZE_VERTICAL)
        y = PAGE_SIZE_VERTICAL - y
        self.printer.printAtPSArabic(x, y, text)
    
    def newPage(self):
        self.printer.printNewPage()
        
    def printUsingFunc(self, func):
        self.printer.initialiseRenderer()
        func(self)
        self.printer.finaliseRenderer()
