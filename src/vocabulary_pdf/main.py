import logging

root_logger = logging.getLogger()
root_logger.level = logging.DEBUG
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
hdlr = logging.StreamHandler()
hdlr.setFormatter(formatter)
root_logger.addHandler(hdlr)

from vocabulary_pdf.printlayout import PrintLayout
from vocabulary_pdf.constants import PAGE_SIZE_HORIZONTAL, PAGE_SIZE_VERTICAL


def func1(print_layout):
    ara1 = u'\u0627\u0633\u0645'
    ara2 = u'\u0645\u0636\u0627\u0631\u0639'
    print_layout.printTitle()
    print_layout.printAtArabic(120, 20, ara1)
    print_layout.printAtArabic(120, 30, ara2)
    
    width = print_layout.arabicWidth(ara1)
    
    print_layout.printAt(40, PAGE_SIZE_VERTICAL - 50, 'meaning3')
    print_layout.printPageNumber(1)
    print_layout.newPage()

f = open('psout3.ps', 'w')
print_layout = PrintLayout(f)
print_layout.printUsingFunc(func1)
