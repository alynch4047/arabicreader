
from lanes_service.lanes_handler import LanesHandler


class LanesURL(object):
    
    lanes_handler = LanesHandler()
    
    def GET(self, url):
        print LanesURL.lanes_handler.get_url(url)

