import logging

from vocabulary_pdf.utils import (reverse_phrase, strip_tashkeel, replace_tashkeel,
                                  presentation_tashkeel, TASHKEEL)

l = logging.getLogger(__name__)

JOIN_NONE = 0
JOIN_RIGHT = 1
JOIN_LEFT = 2
JOIN_DUAL = 3
JOIN_TRANSPARENT = 4
JOIN_STRIP_OUT = 5

SHADDA = 0x651


def shape(text):
    """ take a unicode non-shaped arabic string and shape it for rendering.
    Sequence shaddas before their harakat. Do ligatures. Output string
    in presentation glyphs only """
    # check which characters are adjacent to which and which  are
    # right-join, dual-join, and left-join
    text = shaddas_before_harakaat(text)
    text = do_ligatures(text) 
    text = reverse_phrase(text)
    try:
        # first join any necessary characters e.g. laam + alif
    
#        text = charjoin(text)
        tashkeel, text = strip_tashkeel(text) # remove tashkeel and save it to put it back
        shapedText = ''
        # assume R-L text i.e. has already been reversed
        l.debug('stripped text is %s', text)
        for i in range(len(text)):
            # get relevant (adjacent) characters
            if i != 0:
                leftChar = ord(text[i - 1])
            else:
                leftChar = None
            if i != len(text) - 1:
                rightChar = ord(text[i + 1])
            else:
                rightChar = None        
            thisChar = ord(text[i])
#            l.debug('%x %x %x', leftChar, thisChar, rightChar)
    
            if thisChar not in CHAR_ATTRIBUTES: continue
            
            # check for isolated form
            if CHAR_ATTRIBUTES[thisChar] == JOIN_NONE or \
               ((leftChar == None) or CHAR_ATTRIBUTES[leftChar] in (JOIN_NONE, JOIN_LEFT) or \
                CHAR_ATTRIBUTES[thisChar] in (JOIN_NONE,JOIN_RIGHT)) and \
               ((rightChar == None) or CHAR_ATTRIBUTES[rightChar] in (JOIN_NONE, JOIN_RIGHT)):
                #print "use isolated form"
                charForm = CHAR_ISOLATED_FORM[ord(text[i])]
                shapedText += chr(charForm)
            # check for initial form
            elif (rightChar == None or CHAR_ATTRIBUTES[rightChar] in (JOIN_NONE, JOIN_RIGHT)) and \
               (CHAR_ATTRIBUTES[leftChar] in (JOIN_RIGHT, JOIN_DUAL)) and \
               CHAR_ATTRIBUTES[thisChar] in (JOIN_LEFT, JOIN_DUAL):
                #print "use initial form"
                charForm = CHAR_INITIAL_FORM[ord(text[i])]
                shapedText += chr(charForm)
            # check for final form (we know not isolated or initial)
            elif  CHAR_ATTRIBUTES[thisChar] == JOIN_RIGHT or \
               (((leftChar == None) or  CHAR_ATTRIBUTES[leftChar] in (JOIN_NONE, JOIN_LEFT)) and \
               (CHAR_ATTRIBUTES[rightChar] in (JOIN_LEFT, JOIN_DUAL)) and \
               CHAR_ATTRIBUTES[thisChar] in (JOIN_RIGHT, JOIN_DUAL)):
                #print "use final form"
                charForm = CHAR_FINAL_FORM[ord(text[i])]
                shapedText += chr(charForm)
            # check for medial form    
            # if this char is dual join and left character is dual or right join and
            # right character is dual or left form then we want medial form
            elif (CHAR_ATTRIBUTES[thisChar] == JOIN_DUAL) and CHAR_ATTRIBUTES[leftChar] in (JOIN_RIGHT, JOIN_DUAL) and \
                 CHAR_ATTRIBUTES[rightChar] in (JOIN_LEFT, JOIN_DUAL):
                # use medial form
                #print "use medial form"
                charForm = CHAR_MEDIAL_FORM[ord(text[i])]
                shapedText += chr(charForm)
            elif CHAR_ATTRIBUTES[thisChar] == JOIN_STRIP_OUT:
                pass
            else:
                raise Exception("Form not found! %s", text[i])
                shapedText += text[i]
        #print "shaped text without tashkeel is " + repr(shapedText)
        shapedText = replace_tashkeel(shapedText, tashkeel)
        shapedText = presentation_tashkeel(shapedText)
        #print "shaped text with tashkeel is " + repr(shapedText)
        shapedText = reverse_phrase(shapedText)
        return shapedText
    except:
        logging.exception('shaping %s', text)
        raise
    
    
def shaddas_before_harakaat(text):
    """
    Move shaddas before any harakaat
    """
    shadda_indices = []
    for ix, letter in enumerate(text):
        if ord(letter) == SHADDA:
            shadda_indices.append(ix)
    if not shadda_indices:
        return text
    letter_list = list(text)
    for ix in shadda_indices:
        if ix > 0 and ord(text[ix-1]) in TASHKEEL:
            letter_list[ix] = letter_list[ix-1]
            letter_list[ix-1] = chr(SHADDA)
    return ''.join(letter_list)

    
def do_ligatures(text):
    """join any necessary characters e.g. laam + alif"""
    # this works on a string replacement basis. First try to replace the longest strings e.g. len = 4, 3, down to len == 2
    # provide alternatives for the possible tashkeel
    
    # we know shaddas are before harakaat
    
    LAAM_SHADDA_FATHA_ALIF = u'\u0644\u0651\u064e\u0627'
    LAAM_SHADDA_FATHA_ALIF_REPLACE = u'\ufefb\u0651\u064e'

    LAAM_SHADDA_ALIF = u'\u0644\u0651\u0627'
    LAAM_SHADDA_ALIF_REPLACE = u'\ufefb\u0651'

    LAAM_FATHA_ALIF = u'\u0644\u064e\u0627'
    LAAM_FATHA_ALIF_REPLACE = u'\ufefb\u064e'

    LAAM_ALIF = u'\u0644\u0627'
    LAAM_ALIF_REPLACE = u'\ufefb'
    
    replace = [(LAAM_SHADDA_FATHA_ALIF, LAAM_SHADDA_FATHA_ALIF_REPLACE),
               (LAAM_SHADDA_ALIF, LAAM_SHADDA_ALIF_REPLACE),
               (LAAM_FATHA_ALIF, LAAM_FATHA_ALIF_REPLACE),
               (LAAM_ALIF, LAAM_ALIF_REPLACE)]

    for source_string, replace_string in replace:
        try: 
            text = text.replace(source_string, replace_string)
        except (UnicodeDecodeError, UnicodeEncodeError):
            l.exception('ligatures %s', source_string)
            raise
    return text
            
# attribute can be
# 0 = non joining
# 1 = right joining
# 2 = left joining - no such thing in real life
# 3 = dual joining
# 4 = transparent
# 5 = don't include in shaped text (strip out)
CHAR_ATTRIBUTES = {32:0, 0x622:1, 0x624:1,  0x627:1, 0x628:3, 0x62a:3, 0x62b:3, 0x62c:3, 0x62d:3, 
               0x62e:3, 0x62f:1, 0x630:1, 0x631:1, 0x632:1, 0x633:3, 
               0x634:3, 0x635:3, 0x636:3, 0x637:3, 0x638:3, 0x639:3, 
               0x63a:3, 0x641:3, 0x642:3, 0x643:3, 0x644:3, 0x645:3, 
               0x646:3, 0x647:3, 0x648:1, 0x649:1, 0x64a:3, 0x64B:4, 
               0x64C:4, 0x64D:4, 0x64E:4, 0x64F:4, 0x650:4, 0x652:4, 
               0x623:1, 0x624:1, 0x625:0, 0x626:3, 0x621:0,
               0x629:1, 0x651:4, 0xfefb:1, 0x640:5}

# representational unicode glyph numbers for unicode char codes

CHAR_ISOLATED_FORM = {32:32, 0x621:0xfe80, 0x622:0xfe81, 0x623:0xfe83, 0x624:0xfe85, 0x625:0xfe87,
               0x627:0xfe8d, 0x628:0xfe8f, 0x629:0xfe93, 0x62a:0xfe95, 0x62b:0xfe99, 0x62c:0xfe9d, 0x62d:0xfea1, 
               0x62e:0xfea5, 0x62f:0xfea9, 0x630:0xfeab, 0x631:0xfead, 0x632:0xfeaf, 0x633:0xfeb1, 
               0x634:0xfeb5, 0x635:0xfeb9, 0x636:0xfebd, 0x637:0xfec1, 0x638:0xfec5, 0x639:0xfec9, 
               0x63a:0xfecd, 0x641:0xfed1, 0x642:0xfed5, 0x643:0xfed9, 0x644:0xfedd, 0x645:0xfee1, 
               0x646:0xfee5, 0x647:0xfee9, 0x648:0xfeed, 0x649:0xfeef, 0x64a:0xfef1, 0xfefb:0xfefb}

CHAR_INITIAL_FORM = {0x626:0xfe8b, 0x628:0xfe91, 0x62a:0xfe97, 0x62b:0xfe9b, 0x62c:0xfe9f, 0x62d:0xfea3, 
               0x62e:0xfea7, 0x633:0xfeb3, 
               0x634:0xfeb7, 0x635:0xfebb, 0x636:0xfebf, 0x637:0xfec3, 0x638:0xfec7, 0x639:0xfecb, 
               0x63a:0xfecf, 0x641:0xfed3, 0x642:0xfed7, 0x643:0xfedb, 0x644:0xfedf, 0x645:0xfee3, 
               0x646:0xfee7, 0x647:0xfeeb, 0x64a:0xfef3}

CHAR_MEDIAL_FORM = {0x628:0xfe92, 0x62a:0xfe98, 0x62b:0xfe9c, 0x62c:0xfea0, 0x62d:0xfea4, 
               0x62e:0xfea8, 0x633:0xfeb4, 
               0x634:0xfeb8, 0x635:0xfebc, 0x636:0xfec0, 0x637:0xfec4, 0x638:0xfec8, 0x639:0xfecc, 
               0x63a:0xfed0, 0x641:0xfed4, 0x642:0xfed8, 0x643:0xfedc, 0x644:0xfee0, 0x645:0xfee4, 
               0x646:0xfee8, 0x647:0xfeec, 0x64a:0xfef4}

CHAR_FINAL_FORM = {0x622:0xfe82, 0x623:0xfe84, 0x627:0xfe8e, 0x628:0xfe90, 0x629:0xfe94, 0x62a:0xfe96, 0x62b:0xfe9a,
               0x62c:0xfe9e, 0x62d:0xfea2, 
               0x62e:0xfea6, 0x62f:0xfeaa, 0x630:0xfeac, 0x631:0xfeae, 0x632:0xfeb0, 0x633:0xfeb2, 
               0x634:0xfeb6, 0x635:0xfeba, 0x636:0xfebe, 0x637:0xfec2, 0x638:0xfec6, 0x639:0xfeca, 
               0x63a:0xfece, 0x641:0xfed2, 0x642:0xfed6, 0x643:0xfeda, 0x644:0xfede, 0x645:0xfee2, 
               0x646:0xfee6, 0x647:0xfeea, 0x648:0xfeee, 0x649:0xfef0, 0x64a:0xfef2, 0xfefb:0xfefc, 0x624:0xfe86 }

    
