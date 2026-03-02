
from quran_service.quran_handler import QuranHandler

from config import QURAN_DATA_LOC


class QuranURL(object):
    
    quran_handler = QuranHandler(QURAN_DATA_LOC)
    
    def GET(self, url):
        print(QuranURL.quran_handler.get_url(url))

