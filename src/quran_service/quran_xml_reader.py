

from xml.dom import minidom

class QuranXMLReader(object):
    
    def __init__(self, xml_data_path):
        
        self.xml_data_path = xml_data_path
        
        self.dom = minidom.parse(xml_data_path)
        
        self.suras = {}
        
        self._populate_suras()
        
    def get_ayat_text(self, sura_no, ayat_no):
        sura_name, ayats = self.suras[sura_no]
        return ayats[ayat_no][0]
    
    def _populate_suras(self):
        for sura_element in self.dom.getElementsByTagName('sura'):
            sura_id = int(sura_element.getAttribute('id'))
            sura_name = sura_element.getAttribute('name')
            ayats = {}
            for ayat_element in sura_element.getElementsByTagName('aya'):
                aya_id = int(ayat_element.getAttribute('id'))
                search_text_element = ayat_element.getElementsByTagName('searchtext')[0]
                search_text = search_text_element.firstChild.data
                quran_text_element = ayat_element.getElementsByTagName('qurantext')[0]
                quran_text = quran_text_element.firstChild.data
                ayat_data = (quran_text, search_text)
                ayats[aya_id] = ayat_data
            self.suras[sura_id] = (sura_name, ayats)
            
            