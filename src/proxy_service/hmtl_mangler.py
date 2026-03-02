
import logging
import re

from traits.api import HasTraits, Str, Instance

from bs4 import BeautifulSoup, NavigableString, Tag
from proxy_service.url_mangler import URLMangler

l = logging.getLogger(__name__)


class HTMLMangler(HasTraits):
    
    url_root = Str
    
    ul_mangler = Instance(URLMangler)
    
    def set_charset_to_utf8(self, html, original_encoding):
        html = html.replace(original_encoding, 'utf-8')
        return html
    
    def fixup_header_links(self, html, document_url_dir):
        """
        Fix the links in the document header.
        """
        body_start_ix = html.find(u'body')
        if body_start_ix == -1:
            body_start_ix = html.find(u'BODY')
        if body_start_ix == -1:
            raise Exception('cannot find body of document')
        l.debug('body start is at %s', body_start_ix)
        header = html[:body_start_ix]
        # e.g. <link rel='abc' href='details.asp'>, prepend document_url_dir to href
        single_or_double_quote = '[' + "\\'" + '\\"' + ']'
        patterns = []
        for attr_name in ['href=', 'src=']:
            pattern =  r'<.*?%s' % attr_name +\
                                        single_or_double_quote + '(.*?)' + \
                                        single_or_double_quote + '.*?>' 
            patterns.append(pattern)
        pattern =  r'@import\s+?' +\
                                        single_or_double_quote + '(.*?)' + \
                                        single_or_double_quote
        patterns.append(pattern)
        for pattern in patterns:
            new_html = ''
            start_ix = 0
            url_start = url_end = None
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
            for match_object in compiled_pattern.finditer(html):
                url_start = match_object.start(1)
                url_end = match_object.end(1)
                fixed_url = self.url_mangler.get_absolute_url(document_url_dir,
                                                              match_object.groups()[0])
                new_html += html[start_ix:url_start]
                new_html += str(fixed_url)
                start_ix = url_end
            if url_end:
                new_html += html[url_end:]
                html = new_html
        return html
    
    def span_text(self, text):
        l.debug('span text')
        soup = BeautifulSoup(text, convertEntities='html', isHTML=True)
        if soup.head is None:
            l.debug('cant process text (no head) %s', text)
            raise Exception('Error parsing the document: cannot find the document head')
        if soup.body is None:
            l.debug('cant process text (no body) %s', text)
            raise Exception('Error parsing the document: cannot find the document body')
        self._add_head_info(soup)
#        self._add_floating_info_pane(soup)
        self._set_up_on_load(soup)
        i = 0
        for navstr in soup.body.findAll(text=True):
            if navstr.__class__ == NavigableString:
                if navstr.parent.name in ['a', 'script']:
                    continue
                words = str(navstr).split()
                new_text = ''
                for word in words:
                    if ord(word[0]) > 0x600:  #x621 - x654
                        # strip invalid initial characters
                        inner_word_a = word
                        for char in word:
                            if (ord(char) < 0x621) or (ord(char) > 0x654):
                                inner_word_a = inner_word_a[1:]
                            else:
                                break
                        # strip invalid final characters
                        inner_word_b = ''
                        for char in inner_word_a:
                            if (ord(char) < 0x621) or (ord(char) > 0x654):
                                break
                            else:
                                inner_word_b += char
                            
                        quoted_word = "'" + inner_word_b + "'"
                        ix = str(i)
                        span_text = '<span id=central_word_'+ ix + \
                                  ' onclick="if_ar.central_word_clicked(' + quoted_word + ')"' +\
                                  ' onmouseover="if_ar.mouse_over_central_word('+ ix + ')"' +\
                                  ' onmouseout="if_ar.mouse_out_central_word('+ ix + ')">' + \
                                   word + ' </span>'
                        new_text += span_text
                        i += 1
                    else:
                        new_text += word
                navstr.replaceWith(new_text)
                
        return soup.prettify()
    
    def _add_head_info(self, soup):
        #  script = """<script type="text/javascript" src="/arareader.js"></script>"""
        #  style = """<style type="text/css">@import "/arareader.css";</style>"""
        
        script_1 = Tag(soup, 'script')
        script_1['type'] = 'text/javascript'
        script_1['src'] = '%siframe_ar.js' % self.url_root 
        soup.head.insert(0, script_1)
        style_1 = Tag(soup, 'style')
        style_text = NavigableString("""@import "%siframe_ar.css";""" % self.url_root)
        style_1.insert(0, style_text)
        soup.head.insert(0, style_1)
        
    def add_head_info(self, text):
        text =text.replace('<head>','<HEAD>')
        js_url = '%siframe_ar.js' % self.url_root
        css_url = '%siframe_ar.css' % self.url_root 
        text = text.replace('<HEAD>','<HEAD><script type="text/javascript" src="%s"></script>' % js_url)
        text = text.replace('<HEAD>','<HEAD><style type="text/css">@import "%s";</style>' % css_url)
        return text
        
    def _add_floating_info_pane(self, soup):
        div_info = Tag(soup, 'div')
        div_info['id'] = 'ar_info_pane'
        soup.body.insert(0, div_info)
        
    def _set_up_on_load(self, soup):
        also_load = """if_ar.init()"""
        try:
            original_on_load = soup.body['onload']
            new_on_load = '%s; %s' % (original_on_load, also_load)
        except KeyError:
            new_on_load = also_load
        soup.body['onload'] = new_on_load
        return new_on_load
        