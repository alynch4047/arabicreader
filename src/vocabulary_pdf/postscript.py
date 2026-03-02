import logging

from vocabulary_pdf.constants import encoding
from vocabulary_pdf.utils import get_resource_file_path

class PostScript(object):
    
    def __init__(self, ps_file):
        self.ps_file = ps_file

    def psOut(self, text):
        try:
            logging.debug('ps out %s', text)
            self.ps_file.write(text + '\n')
        except:
            print("exception text is", repr(text))
            raise
    
    def postscriptProlog(self):
                  
        self.psOut('/haqqenc [')
    
        for code in encoding:
            self.psOut(code)
        
        self.psOut('] def')
    
        psPrologFile = open(get_resource_file_path('prolog.ps'),'r')
        l = psPrologFile.readline()
        while l:
            self.ps_file.write(l)
            l = psPrologFile.readline()
    
