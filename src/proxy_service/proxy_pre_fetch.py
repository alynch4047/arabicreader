
import logging
import threading
import time

from traits.api import HasTraits, Str, Instance, Int

from proxy_service.url_mangler_soup import URLMangler
from proxy_service.proxy_cache import ProxyCache

PREFETCH_INTERVAL = 3600
#PREFETCH_SITES = ['www.alarabiya.net', 'asharqalawsat.com',  'aljazeera.net']
PREFETCH_SITES = []

l = logging.getLogger(__name__)


class ProxyPreFetch(HasTraits):

    proxy_cache = Instance(ProxyCache)
    
    url_mangler = Instance(URLMangler, ())
    
    interval = Int(PREFETCH_INTERVAL)
    
    def start(self):
        th = threading.Thread(target=self._timed_pre_fetch)
        th.setDaemon(True)
        th.start()
        
    def _timed_pre_fetch(self):
        while True:
            for url in PREFETCH_SITES:
                self._pre_fetch_base_url(url)
            time.sleep(self.interval)
            
    def _pre_fetch_base_url(self, url):
        """Prefetch this url, and also all the first-level links from it
        """
        url = self.url_mangler.normalise_url(url)
        l.debug('prefetch URL %s', url)
        text = self.proxy_cache.get(url, reload=True)
        linked_urls = self.url_mangler.get_absolute_links(url, text)
        for link_url in linked_urls:
            if self.url_mangler.site_address(url) == self.url_mangler.site_address(link_url):
                self.proxy_cache.get(link_url, reload=True)
            else:
                l.debug('%s is different site to %s %s %s', url, link_url,
                        self.url_mangler.site_address(url),self.url_mangler.site_address(link_url))
            

            
    