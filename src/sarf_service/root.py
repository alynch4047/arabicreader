from traitlets import HasTraits
from traits.api import Int
from traits.api import Interface, Str, List, provides

Root = Str


class IReference(Interface):
    
    sura = Int
    ayat = Int
    word_ix = Int
    
@provides(IReference)
class Reference(HasTraits):
    
    sura = Int
    ayat = Int
    word_ix = Int
    

class IRootMeaning(Interface):
    
    # the 3 or 4 letters that indicate the root
    root = Root
    
    # the 'source' word
    masdar = Str
    
    # the meaning
    meaning = Str
    
    # the references in texts, dictionaries etc
    references = List(IReference)
    
@provides(IRootMeaning)
class RootMeaning(HasTraits):
    
    root = Root
    
    masdar = Str
    
    meaning = Str
    
    references = List(IReference)
    
    def __repr__(self):
        from sarf_service.api import transliterate_to_gb
        if len(self.meaning) > 15:
            meaning = self.meaning[:15]
        else:
            meaning = self.meaning
        return '<RootMeaning %s %s>' % (transliterate_to_gb(self.root), meaning) 
    
