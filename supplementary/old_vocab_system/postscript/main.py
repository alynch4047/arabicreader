import logging

root_logger = logging.getLogger()
root_logger.level = logging.DEBUG
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
hdlr = logging.StreamHandler()
hdlr.setFormatter(formatter)
root_logger.addHandler(hdlr)

import printlayout
from constants import PAGE_SIZE_HORIZONTAL, PAGE_SIZE_VERTICAL

#printlayout.printAllSections(False, PAGE_SIZE_HORIZONTAL, PAGE_SIZE_VERTICAL)

def func1():
    entry = [None, u'\u0627\u0633\u0645', u'\u0645\u0636\u0627\u0631\u0639', 'c']
    printlayout.printEntry(False, entry, 20, PAGE_SIZE_VERTICAL - 20, 50)
    width1 = printlayout.printAtArabicBuffer(30, PAGE_SIZE_VERTICAL - 30, u'\u0645\u0636\u0627\u0631\u0639', False);
    width2 = printlayout.printAtArabicBuffer(40, PAGE_SIZE_VERTICAL - 40, u'\u0645\u0636\u0627\u0631\u0639', False);
    printlayout.printAtBuffer(40, PAGE_SIZE_VERTICAL - 50, 'meaning', False)
    printlayout.printAtBuffer(40, PAGE_SIZE_VERTICAL * 2 - 50, 'meaning2', False)

printlayout.printUsingFunc(func1)