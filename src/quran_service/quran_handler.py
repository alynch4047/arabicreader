
from quran_service.quran_xml_reader import QuranXMLReader


class QuranHandler(object):
    
    def __init__(self, xml_data_path):
        
        self.xml_data_path = xml_data_path
        self.quran_xml_reader = QuranXMLReader(xml_data_path)
        
    def get_url(self, url):
            if url.startswith('ayat/'):
                return self._get_ayat(url[5:])
            else:
                return 'invalid url'
            
    def _get_ayat(self, sura_ayat_no):
        try:
            sura_no, ayat_no = sura_ayat_no.split('/')
            ayat_text = self.quran_xml_reader.get_ayat_text(int(sura_no), int(ayat_no))
            return ayat_text
        except:
            return 'Invalid URL or syra/ayat no when getting ayat'
    
    def _get_root_info(self, root):
        root = unicode(root,'utf-8')
