import os
import logging
from html.parser import HTMLParser

from traits.api import HasTraits, Interface, Any, Str, List, Dict

from sarf_service.root import IRootMeaning, Root, RootMeaning

from project_roots_online_service.constants import HTML_TRANSLITERATIONS_REVERSE

l = logging.getLogger(__name__)


class PROHTMLParser(HTMLParser, HasTraits):
    
    _current_root = Root
    _in_tag = Str
    root_meanings_dict = Dict
    pro_html_directory = Str
    
    def __init__(self, **traits):
        HTMLParser.__init__(self)
        HasTraits.__init__(self, **traits)
        
        # a dictionary of root meanings - root against root_meaning
        self._parse_html_files(self._get_html_files(self.pro_html_directory))
        
    def _get_html_files(self, pro_html_directory):
        html_files = []
        file_names = os.listdir(pro_html_directory)
        for file_name in file_names:
            if file_name.endswith('htm'):
                html_files.append(file_name)
                
        return html_files
    
    def _parse_html_files(self, file_names):
        for file_name in file_names:
            file_path = os.path.join(self.pro_html_directory, file_name)
            data = open(file_path).read()
            self.feed(data)
            
    def handle_starttag(self, tag, attrs):
        self.in_tag = tag
        if tag.upper() == 'HR':
            self._current_root = ''

    def handle_endtag(self, tag):
        self.in_tag = None
        
    def handle_data(self, data):
        matches, root = self._matches_root_letters(data)
        if matches:
            self._current_root = root
            assert isinstance(root, str)
        else:
            if self._current_root != '':
                matches, definition = self._matches_definition(data)
                if matches:
                    root_meaning = RootMeaning(root=self._current_root,
                                               meaning=definition)
                    self.root_meanings_dict[self._current_root] = root_meaning
                    #l.info('added root %s %s',self._current_root,definition)
                    self._current_root = ''
                
    def _matches_root_letters(self, data):
        data = data
        any_translit_found = False
        for translit in HTML_TRANSLITERATIONS_REVERSE:
            if data.find(translit) != -1:
                any_translit_found = True
        if not any_translit_found:
            #l.debug('no root found in data')
            return False, ''
        if '-' not in data:
            #l.debug('no - found in data')
            return False, ''
        roots = data.split('-')
        if len(roots) not in [3,4]:
            #l.debug('num roots not 3 or 4: %s, %s', roots, data)
            return False, ''
        roots = tuple([root.strip() for root in roots])
        for root in roots:
            if root not in HTML_TRANSLITERATIONS_REVERSE:
                #l.debug('not a valid root')
                if len(root) < 5:
                    pass
                    #l.warn('not a valid root? %s', root)
                return False, ''
        #l.debug('found root %s', roots)
        arabic_root = self._convert_translit_to_unicode(roots)
        #l.debug('arabic root is %s', arabic_root)
        return True, arabic_root
        
    def _matches_definition(self, data):
        if len(data) > 20:
            data = data.strip()
            if data.startswith('='):
                data = data[1:]
            return True, data
        return False, ''
    
    def _convert_translit_to_unicode(self, letters):
        arabic = ''
        for letter in letters:
            arabic_char = HTML_TRANSLITERATIONS_REVERSE[letter]
            arabic += arabic_char
            
        return arabic
        
        
        
                
            