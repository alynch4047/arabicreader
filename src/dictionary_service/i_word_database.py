
from traits.api import Interface, List, Dict


class IWordDatabase(Interface):
    
    def words_possibly_matching(self, word):
        pass