
import urllib.parse

from server.handler import Handler
from server.cookies import set_cookie_data, get_cookie_data, delete_cookie


class URL:
    def _unquote(self, url):
        url = urllib.parse.unquote(url)
        url = url.replace('\n', '')
        url = url.replace('\t', '')
        url = url.replace('\r', '')
        return url