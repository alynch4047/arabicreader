
import urllib.parse
import logging
import threading
import shelve
import os
import datetime
import random

from traits.api import HasTraits, Str, Instance

from proxy_service.url_mangler_soup import URLMangler

_lock = threading.Lock()

l = logging.getLogger(__name__)


class ProxyCache(HasTraits):

    proxy_cache_dir = Str
    
    shelf = Instance(shelve.Shelf)
    
    url_mangler = Instance(URLMangler, ())
    
    def __init__(self, **traits):
        super(ProxyCache, self).__init__(**traits)
        
        if not os.path.isdir(self.proxy_cache_dir):
            raise Exception('The proxy cache dir (%s) is not accessible' %
                                                        self.proxy_cache_dir)
            
        shelf_path = os.path.join(self.proxy_cache_dir, 'url_shelf')
        self.shelf = shelve.open(shelf_path)
        for url in self.shelf.keys():
            pass
            #l.debug('already in proxy cache: %s', url)
            
    def _remove_from_cache(self, url):
        l.debug('remove %s from the cache', url)
        date, file_name = self.shelf[url]
        file_path = os.path.join(self.proxy_cache_dir, file_name)
        try:
            os.remove(file_path)
        except OSError:
            l.exception('removing file from cache')
        del self.shelf[url]
    
    def get(self, url, reload=False):
        """ Get the text from the given url. If it is in the cache
        and reload=False then use the cache otherwise fill cache with latest contents"""
        url = self.url_mangler.normalise_url(url)
        url = str(url)
        if reload:
            if url in self.shelf:
                self._remove_from_cache(url)
        if url not in self.shelf:
            text = self._download(url)
            l.debug('url not in proxy cache: %s', url)
            file_name = self._generate_file_name(self.proxy_cache_dir)
            file_path = os.path.join(self.proxy_cache_dir, file_name)
            f = open(file_path, 'w+')
            f.write(text)
            try:
                _lock.acquire()
                self.shelf[url] = datetime.datetime.now(), file_name
            finally:
                _lock.release()
        else:
            l.debug('get url from proxy cache: %s', url)
            date, file_name = self.shelf[url]
            file_path = os.path.join(self.proxy_cache_dir, file_name)
            text = open(file_path, 'r+').read()
        return text
    
    def _generate_file_name(self, cache_dir):
        """ Generate a unique file name for a file name in the given directory"""
        dir = os.listdir(cache_dir)
        try:
            _lock.acquire()
            while True:
                filename = str(random.randint(1000000, 9999999))
                if filename not in dir:
                    break
        finally:
            _lock.release()
        return filename
        
    def _download(self, url):
        l.debug('get URL: %s', url)
        downloader = CurlDownload()
        downloader.download(url)
        return downloader.contents
#        opener = urllib.FancyURLopener({})
#        f = opener.open(url)
#        text = f.read()
#        header = f.info()
#        #l.debug('header is %s', header)
        
#        return text

import pycurl

class CurlDownload(object):
    
        def __init__(self):
                self.contents = ''

        def _body_callback(self, buf):
                self.contents = self.contents + buf
                
        def download(self, url):
            self.contents = ''
            c = pycurl.Curl()
            l.debug('use curl to get %s', url)
            c.setopt(c.URL, url)
            c.setopt(c.FOLLOWLOCATION, 1)
            c.setopt(c.WRITEFUNCTION, self._body_callback)
            c.perform()
            c.close()
            

