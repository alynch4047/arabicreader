

from traits.api import HasTraits, Interface, implements, Any, Str, List
from traits.api import TraitString, Int


#class Root(TraitString):
#    
#    def __init__ ( self, *param):
#        kwargs = {minlen:3, maxlen:6}
#        TraitString.__init__ ( self, *param, **kwargs)
        
Root = Str


class IReference(Interface):
    
    sura = Int
    ayat = Int
    word_ix = Int
    

class Reference(HasTraits):
    
    implements(IReference)
    
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
    

class RootMeaning(HasTraits):
    
    implements(IRootMeaning)
    
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
    
