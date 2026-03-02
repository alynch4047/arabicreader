# -*- coding: utf-8 -*-

import logging
import tempfile
import os

from traits.api import HasTraits, Int, Instance

from sarf_service.api import Word

from vocabulary_service.vocabulary import Vocabulary

from vocabulary_pdf.printlayout import PrintLayout
from vocabulary_pdf.constants import PAGE_SIZE_VERTICAL

LINE_HEIGHT = 20
TOP_OF_PAGE = 35

l = logging.getLogger(__name__)


class VocabPDF(HasTraits):
    
    user_id = Int
    
    vocabulary = Instance(Vocabulary)
    
    def create_pdf(self):
        os_handle, file_path = tempfile.mkstemp('.ps')
        l.debug('ps file is %s', file_path)
        os.close(os_handle)
        f = open(file_path, 'w')
        print_layout = PrintLayout(f)
        print_layout.printUsingFunc(self._make_pdf_content_all_words)
        f.close()
        os_handle, pdf_file_path = tempfile.mkstemp('.pdf')
        os.close(os_handle)
        res = os.spawnlp(os.P_WAIT, 'ps2pdf', 'ps2pdf', 
                         '-dEmbedAllFonts=true', 
                         file_path, pdf_file_path)
        l.debug('res is %s', res)
        pdf_data = open(pdf_file_path).read()
        l.debug('pdf file is %s', pdf_file_path)
        os.remove(file_path)
        os.remove(pdf_file_path)
        return pdf_data
    
    def _make_pdf_content_all_words(self, print_layout):
        words_grouped_by_kalima = self.vocabulary.get_all_words_grouped_by_kalima()
        self._make_pdf_content(print_layout, words_grouped_by_kalima)
    
    def _make_pdf_content(self, print_layout, words_grouped_by_kalima):
        page_number = 1
        print_layout.printTitle()
        x = {0: [550, 500, 450, 290],
             1: [270, 220, 170, 10]}
        y = TOP_OF_PAGE
        column = 0
        for kalima_id, words in words_grouped_by_kalima.items():
            if len(words) == 0:
                continue
            required_height = max(self._get_arabic_height(words),
                                  self._get_english_height(words, 40))
            if required_height > PAGE_SIZE_VERTICAL:
                raise Exception('element too big to fit page: kalima_id: %s', kalima_id)
            if y > (PAGE_SIZE_VERTICAL - required_height):
                y = TOP_OF_PAGE
                if column == 0:
                    column = 1
                else:
                    column = 0
                    print_layout.printPageNumber(page_number)
                    print_layout.newPage()
                    page_number += 1
                    print_layout.printTitle()
            english_lines = split_into_lines(words[0].meaning, 40)
            l.debug('meaning %s ', words[0].meaning)
            for line_ix, line in enumerate(english_lines):
                print_layout.printAt(x[column][3], y + line_ix * LINE_HEIGHT, line)
            for word_ix, word in enumerate(words):
                location_ix = word_ix % 3
                y_offset = int(word_ix/3) * LINE_HEIGHT
                print_layout.printAtArabic(x[column][location_ix], y + y_offset,
                                            word.text)
            y += required_height
            
        print_layout.printPageNumber(page_number)
        print_layout.newPage()
        
    def _get_arabic_height(self, words):
        height = int(len(words)/3) * LINE_HEIGHT
        return height
    
    def _get_english_height(self, words, width):
        lines = split_into_lines(words[0].meaning, width)
        return len(lines) * LINE_HEIGHT
        
        
def split_first_line_at(text, split_point, line_width):
    if split_point >= len(text):
        return [text]
    line = text[:split_point]
    line_remainder = text[split_point:]
    print(line_remainder)
    return [line] + split_into_lines(line_remainder, line_width)


def find_first_comma_space(text, from_ix=0):
    ix1 = text.find(' ', from_ix)
    ix2 = text.find(',', from_ix)
    if ix1 == -1 and ix2 != -1:
        return ix2
    if ix2 == -1 and ix1 != -1:
        return ix1
    return min(ix1, ix2)


def split_into_lines(text, line_width):
    print(text)
    if len(text) <= line_width:
        return [text]
    else:
        start_ix = 0
        while True:
            ix1 = find_first_comma_space(text, start_ix)
            if ix1 == -1 or ix1 > line_width:
                return split_first_line_at(text, line_width, line_width)
            ix2 = find_first_comma_space(text, ix1 + 1)
            if ix2 == -1 or ix2 > line_width:
                return split_first_line_at(text, ix1, line_width)
            start_ix = ix2 + 1
            
            
class TestVocabPDF(VocabPDF):
    """
    Create the pdf with a list of test words instead of vocab words
    """
    
    def _make_pdf_content_all_words(self, print_layout):
        words_grouped_by_kalima = _get_test_pdf_words_by_kalima_id()
        self._make_pdf_content(print_layout, words_grouped_by_kalima)
        
        
def _get_test_pdf_words_by_kalima_id():
    from sarf_service.test import test_words
    word_kitaab = Word(
        kalima_id=1,
        root=test_words.KTB,
        text=test_words.KITAAB)
    word_kutub = Word(
        kalima_id=1,
        root=test_words.KTB,
        text=test_words.KUTUB)
    words_by_kalima_id = {1: [word_kitaab, word_kutub]}
    word_tubashshiru = Word(
        kalima_id=2,
        root=test_words.BSHR,
        text=u'بشِّروا')
    word_bashshara = Word(
        kalima_id=2,
        root=test_words.BSHR,
        text=u'بشَّر')
    words_by_kalima_id[2] = [word_tubashshiru, word_bashshara]
    word_bashira = Word(
        kalima_id=3,
        root=test_words.BSHR,
        text=u'بشِر')
    word_bashara = Word(
        kalima_id=3,
        root=test_words.BSHR,
        text=u'بشَر')
    words_by_kalima_id[3] = [word_bashira, word_bashara]
    word_laa = Word(
        kalima_id=4,
        text=u'لا')
    word_laa_1 = Word(
        kalima_id=4,
        text=u'لَا')
    words_by_kalima_id[4] = [word_laa, word_laa_1]
    word_illaa = Word(
        kalima_id=4,
        text=u'إلّا')
    word_illaa_1 = Word(
        kalima_id=4,
        text=u'إِلَّا')
    words_by_kalima_id[4] = [word_laa, word_laa_1, word_illaa, word_illaa_1]
    words_by_kalima_id[3] = []
    words_by_kalima_id[1] = []
    words_by_kalima_id[4] = []
    return words_by_kalima_id
