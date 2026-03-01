"""
This module assists with the transformation of URLS
"""

import logging

from traits.api import HasTraits

l = logging.getLogger(__name__)


class URLMangler(HasTraits):
    
    def get_absolute_url(self, document_url_dir, href):
        """
        Append the href to the document_url_dir to give a full url.
        
        document_url_dir: the full url to the document dir
        href: can be absolute or relative path, or full url
        """
        
        assert(document_url_dir.startswith('http://'))
        
        if  href.startswith('http://'):
            return href
        
        site_url = self.get_site_url(document_url_dir)
        assert(site_url[-1] == '/'), 'invalid site url (%s)' % site_url

        if href.startswith('/'):
            return site_url + href[1:]
        
        else:
            return document_url_dir + href
        
    def get_site_url(self, url):
        """
        Get the url for the root of the site
        """
        assert(url.startswith('http://'))
        
        if url.count('/') == 2:
            if not url[-1] == '/':
                url += '/'
            return url
        third_slash_pos = url.find('/', 8)
        return url[:third_slash_pos] + '/'
    
    def get_document_url_dir(self, full_url):
        assert(full_url.startswith('http://'))
        if full_url.endswith('/'):
            return full_url
        else:
            return '/'.join(full_url.split('/')[:-1]) + '/'
        
