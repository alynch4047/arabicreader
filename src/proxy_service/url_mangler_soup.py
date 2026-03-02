
import logging
import re

from traits.api import HasTraits

from bs4 import BeautifulSoup
from proxy_service.override_encoding import get_override_encoding

l = logging.getLogger(__name__)


class URLMangler(HasTraits):
    
    def replace_relative_links(self, text, base_url):
        l.debug('replace links')
        base_url = self._get_directory(base_url)
        soup = self._get_soup(text, base_url)
        change_tags = [('img', 'src'),
                       ('link', 'href'),
                       ('iframe', 'src'),
                       ('script', 'src'),
                       ('a', 'href'),
                       ('input', 'src'),
                       ]
        for tag_type, attr_name in change_tags:
            for element in soup.findAll(tag_type):
                try:
                    old_url = element[attr_name]
                    remote_url = self._get_absolute_url(element[attr_name], base_url)
                    if tag_type in ['a']:
                        remote_url = self._route_through_proxy(remote_url)
                        element[attr_name] = remote_url
                        #del element['href']
                        element['onclick'] = "mode_.goto_url_with_memento('%s');" % remote_url
                    else:
                        element[attr_name] = remote_url
                    element['old_url'] = old_url
                except:
                    pass

        return str(soup)
    
    def _get_soup(self, text, url):
        override_encoding = get_override_encoding(url)
        if override_encoding:
            soup = BeautifulSoup(text, isHTML=True, fromEncoding=override_encoding)
        else:
            soup = BeautifulSoup(text, isHTML=True)
        if soup.head is None:
            l.debug('cant process text (no head) %s', text)
            raise Exception('Error parsing the document: cannot find the document head')
        if soup.body is None:
            l.debug('cant process text (no body) %s', text)
            raise Exception('Error parsing the document: cannot find the document body')
        return soup
    
    def get_absolute_links(self, base_url, text):
        """ Get the links on this page, with the whole url not relative"""
        soup = self._get_soup(text, base_url)
        links = []
        for element in soup.findAll('a'):
            if 'href' in element:
                relative_link = element['href']
                absolute_url = self._get_absolute_url(relative_link, base_url)
                links.append(absolute_url)
        return links
    
    def _route_through_proxy(self, url):
        url = '/services/proxy/geturl/' + url[len('http://'):]
        return url
    
    def normalise_url(self, url):
        if not url.startswith('http://'):
            url = 'http://' + url
        if url.count('/') == 2:
            url += '/'
        return url
    
    def site_address(self, url):
        if url.count('/') == 2:
            return url
        third_slash_pos = url.find('/', 8)
        return url[:third_slash_pos]
    
    def _get_absolute_url(self, url, base_url):
        """ Combine a base url with a possibly relative URL and return
        an absoulte URL"""
        if url.startswith('http'):
            return url
        if not base_url.endswith('/'):
            base_url += '/'
        if url.startswith('/'):
           return self.site_address(base_url) + '/' + url
        return base_url + url
    
    def _get_directory(self, url):
        if url[-1] != '/':
            url = '/'.join(url.split('/')[:-1]) + '/'
        return url
        
