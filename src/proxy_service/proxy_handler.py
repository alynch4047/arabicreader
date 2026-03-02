
import urllib.parse
import logging
from urllib.parse import urlparse
import time

from traits.api import HasTraits, Str, Instance

from server.api import Handler

from bs4 import UnicodeDammit
from proxy_service.hmtl_mangler import HTMLMangler
from proxy_service.url_mangler import URLMangler
from proxy_service.proxy_cache import ProxyCache

l = logging.getLogger(__name__)

ALLOWED_SITES = ['ejtaal.net','alarabiya.net', 'asharqalawsat.com','ghazali.org',
                 'islamicweb.com', 'aljazeera.net', 'news.bbc.co.uk',
                 'www.iu.edu.sa', 'www.islampedia.com', 'www.reefnet.gov.sy',
                 'al-islam.com', 'www.arabicreader.net'
                ]


class ProxyHandler(Handler):
    
    url_root = Str
    
    proxy_cache = Instance(ProxyCache)
    
    html_mangler = Instance(HTMLMangler)
    
    url_mangler = Instance(URLMangler, ())
    
    def _html_mangler_default(self):
        return HTMLMangler(url_root=self.url_root,
                           url_mangler=self.url_mangler)
    
    def _url_lookup_default(self):
        lookup = {
                  'geturl': self._get_url,
        }
        return lookup
    
    def _get_url(self, url, session=None):
        allowed = False
        for site in ALLOWED_SITES:
            if url.find(site) != -1:
                allowed = True
                break
        if not allowed:
            return 'Disallowed Site'
        l.debug('get_url for %s', url)
        #url = 'http://%s' % urllib.quote(url)
        try:
            url = 'http://%s' % url
            if url.count('/') == 2:
                url += '/'
            text = self.proxy_cache.get(url, reload=True)
            ud = UnicodeDammit(text, isHTML=True)
            text = ud.unicode
            l.debug('first 100 is %s', text[:100])
            l.debug('original encoding is %s', ud.originalEncoding)
            l.debug('text type is %s', type(text))
            document_url_dir = self.url_mangler.get_document_url_dir(url)
            l.debug('document_url_dir is %s', document_url_dir)
            text = self.html_mangler.fixup_header_links(text, document_url_dir)
            text = self.html_mangler.add_head_info(text)
            text = self.html_mangler.set_charset_to_utf8(text, ud.originalEncoding)
            return text.encode('utf8')
        except Exception as ex:
            l.exception('processing url %s', url)
            return 'Sorry, the server had an error while trying to load that site. Please try another site!'
        
        
