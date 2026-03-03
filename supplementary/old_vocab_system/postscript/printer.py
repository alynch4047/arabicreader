import logging

from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtPrintSupport import QPrinter

# This module does PostScript printing jobs
from constants import *
from utils import (reversePhrase, stripTashkeel, replaceTashkeel, presentationTashkeel,
                   getStringWidth, stripTashkeelWithLocation)
from postscript import postscriptProlog, psOut, postscriptEpilog

def initialisePrinter(): 
    global myPrinter
    myPrinter = QPrinter()
    myPrinter.setOrientation(QPrinter.Portrait)
    myPrinter.setPageSize(QPrinter.A4)
    myPrinter.setOutputFileName("ps2.ps")
    #myPrinter.setup()

def initialiseRenderer(QT):
    global myPrinter, myPainter

    if QT:
        initialisePrinter()
        myPainter = QPainter()
        if not myPainter.begin(myPrinter):
            return
        myFont = QFont("ae_Nada")
        myPainter.setFont(myFont)

    else:
        postscriptProlog()
        initCharAttributes()
    
def finaliseRenderer(QT):
    global myPrinter, myPainter
    if QT:
        myPrinter.newPage()
        myPainter.end()
    else:
        postscriptEpilog()

def printAtQT(x,y,text, painter, align):
    # 200 should be big enough to take sentence (if not, increase)
    myRect = painter.boundingRect(x-200,y-200,x,y,0,text)
    # text is drawn left aligned so shift left length of text
    xpos = x - myRect.width()
    ypos = y
    painter.drawText(xpos,ypos,text)

def printAtPS(x,y,text, align, fontAbbrev='FT'):
    # postscript printing method, assume prolog and epilog handled elsewhere
    stringWidth = getStringWidth(text, LATIN_FONT_SIZE)
    if align == ALIGN_LEFT:
        xOffset = 0
    else:
        xOffset = stringWidth
    psOut(str(LATIN_FONT_SIZE) + ' ' + fontAbbrev + '\n' + str(x - xOffset) + ' ' + str(y) +\
          ' moveto \n(' + text + ') show')
    #print "printing english " + text
    return stringWidth

def printComment(comment):
    psOut('% ' + comment + '\n')

def printAtPSArabic(x,y,text, sizeonly=False):
    """ postscript printing method, assume prolog and epilog handled elsewhere
        also takes a unicode string and converts it to the base Type1 font char codes
        return the width of the string"""
    
    arabictext = ''
    text = reversePhrase(text)
    text = shapePhrase(text)
    for i in text:
        unicharindex = ord(i)
        if unicharindex >= 0xfe70:
            type1code = unicharindex - 0xfe70 + 50
        else:
            type1code = unicharindex
        if type1code >= 0 and type1code < 256:
            arabictext += chr(type1code) # basic glyph for Baghdad
        else:
            #print "codes are ",unicharindex,type1code
            raise LookupError
    xOffset = getStringWidth(arabictext, ARABIC_FONT_SIZE)
    if not sizeonly:
        # strip out Harakaat for printing separately
        harakaatLocation, strippedtext = stripTashkeelWithLocation(x,y,arabictext)
        psOut(str(ARABIC_FONT_SIZE) + ' FB\n' + str(x - xOffset) + ' ' + str(y) + ' moveto \n(' + strippedtext + ') show')
        for h in harakaatLocation:
            haraka = h[1]
            x = h[2]
            y = h[3]
            psOut(str(ARABIC_FONT_SIZE) + ' FB\n' + str(x) + ' ' + str(y) + ' moveto \n(' + haraka + ') show')
    return xOffset

def shapePhrase(text):
    ret = ''
    words = text.split()
    for i in range(len(words)):
        word = words[i]
        if ret != '':
            ret += ' '
        ret += shape(word)
    return ret

def charjoin(text):
    """join any necessary characters e.g. laam + alif"""
    # this works on a string replacement basis. First try to replace the longest strings e.g. len = 4, 3, down to len == 2
    # provide alternatives for the possible tashkeel
    ALIF_LAAM = u'\u0627\u0644'
    ALIF_LAAM_REPLACE = u'\ufefb'
    ALIF_FATHA_LAAM = u'\u0627\u064e\u0644'
    ALIF_FATHA_LAAM_REPLACE = u'\ufefb\u0640'
    ALIF_MADD_LAAM = u'\u0622\u0644'
    ALIF_MADD_LAAM_REPLACE = u'\ufef5'

    replaceChars3 = {ALIF_FATHA_LAAM:ALIF_FATHA_LAAM_REPLACE }
    replaceChars2 = { ALIF_LAAM:ALIF_LAAM_REPLACE, ALIF_MADD_LAAM:ALIF_MADD_LAAM_REPLACE }

    for replaceString in replaceChars3.keys():
        try:
            text = text.replace(replaceString, replaceChars3[replaceString])
        except (UnicodeDecodeError, UnicodeEncodeError):
            print("replace string", repr(replaceString))
            print("text", repr(text))
            print(repr(replaceChars3))
    for replaceString in replaceChars2.keys():
        try:
            text = text.replace(replaceString, replaceChars2[replaceString])
        except (UnicodeDecodeError, UnicodeEncodeError):
            print("replace string", repr(replaceString))
            print("text", repr(text))
            print(repr(replaceChars2))
        #print "replacing 2 char"
    return text


def shape(text):
    """ take a unicode non-shaped R-L (i.e. beginning of word on the right i.e end of string) arabic string and shape it for rendering """
    # check which characters are adjacent to which and which  are right-join, dual-join, and left-join
    global charAttributes, charInitialForm, charMedialForm, charFinalForm, charisolatedForm
    try:
        # first join any necessary characters e.g. laam + alif
    
        text = charjoin(text)
        tashkeel, text = stripTashkeel(text) # remove tashkeel and save it to put it back
        shapedText = ''
        # assume R-L text i.e. has already been reversed
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
            #print leftChar, thisChar, rightChar
    
            if thisChar not in charAttributes: continue
    
            
            # check for isolated form
            if charAttributes[thisChar] == JOIN_NONE or \
               ((leftChar == None) or charAttributes[leftChar] in (JOIN_NONE, JOIN_LEFT) or \
                charAttributes[thisChar] in (JOIN_NONE,JOIN_RIGHT)) and \
               ((rightChar == None) or charAttributes[rightChar] in (JOIN_NONE, JOIN_RIGHT)):
                #print "use isolated form"
                charForm = charIsolatedForm[ord(text[i])]
                shapedText += chr(charForm)
            # check for initial form
            elif (rightChar == None or charAttributes[rightChar] in (JOIN_NONE, JOIN_RIGHT)) and \
               (charAttributes[leftChar] in (JOIN_RIGHT, JOIN_DUAL)) and \
               charAttributes[thisChar] in (JOIN_LEFT, JOIN_DUAL):
                #print "use initial form"
                charForm = charInitialForm[ord(text[i])]
                shapedText += chr(charForm)
            # check for final form (we know not isolated or initial)
            elif  charAttributes[thisChar] == JOIN_RIGHT or \
               (((leftChar == None) or  charAttributes[leftChar] in (JOIN_NONE, JOIN_LEFT)) and \
               (charAttributes[rightChar] in (JOIN_LEFT, JOIN_DUAL)) and \
               charAttributes[thisChar] in (JOIN_RIGHT, JOIN_DUAL)):
                #print "use final form"
                charForm = charFinalForm[ord(text[i])]
                shapedText += chr(charForm)
            # check for medial form    
            # if this char is dual join and left character is dual or right join and
            # right character is dual or left form then we want medial form
            elif (charAttributes[thisChar] == JOIN_DUAL) and charAttributes[leftChar] in (JOIN_RIGHT, JOIN_DUAL) and \
                 charAttributes[rightChar] in (JOIN_LEFT, JOIN_DUAL):
                # use medial form
                #print "use medial form"
                charForm = charMedialForm[ord(text[i])]
                shapedText += chr(charForm)
            else:
                print("Form not found!")
                shapedText += text[i]
        #print "shaped text without tashkeel is " + repr(shapedText)
        shapedText = replaceTashkeel(shapedText, tashkeel)
        shapedText = presentationTashkeel(shapedText)
        #print "shaped text with tashkeel is " + repr(shapedText)
        return shapedText
    except:
        logging.exception('shaping %s', text)
        raise
            

def initCharAttributes():
    global charAttributes, charInitialForm, charMedialForm, charFinalForm, charIsolatedForm
    # attribute can be
    # 0 = non joining
    # 1 = right joining
    # 2 = left joining - no such thing in real life
    # 3 = dual joining
    # 4 = transparent
    charAttributes = {32:0, 0x622:1, 0x624:1,  0x627:1, 0x628:3, 0x62a:3, 0x62b:3, 0x62c:3, 0x62d:3, \
                   0x62e:3, 0x62f:1, 0x630:1, 0x631:1, 0x632:1, 0x633:3, \
                   0x634:3, 0x635:3, 0x636:3, 0x637:3, 0x638:3, 0x639:3, \
                   0x63a:3, 0x641:3, 0x642:3, 0x643:3, 0x644:3, 0x645:3, \
                   0x646:3, 0x647:3, 0x648:1, 0x649:1, 0x64a:3, 0x64B:4, \
                   0x64C:4, 0x64D:4, 0x64E:4, 0x64F:4, 0x650:4, 0x652:4, \
                   0x623:1, 0x624:1, 0x625:0, 0x626:3, 0x621:0,
                   0x629:1, 0x651:4, 0xfefb:1}

    # representational unicode glyph numbers for unicode char codes
    
    charIsolatedForm = {32:32, 0x621:0xfe80, 0x622:0xfe81, 0x623:0xfe83, 0x624:0xfe85, 0x625:0xfe87,\
                   0x627:0xfe8d, 0x628:0xfe8f, 0x629:0xfe93, 0x62a:0xfe95, 0x62b:0xfe99, 0x62c:0xfe9d, 0x62d:0xfea1, \
                   0x62e:0xfea5, 0x62f:0xfea9, 0x630:0xfeab, 0x631:0xfead, 0x632:0xfeaf, 0x633:0xfeb1, \
                   0x634:0xfeb5, 0x635:0xfeb9, 0x636:0xfebd, 0x637:0xfec1, 0x638:0xfec5, 0x639:0xfec9, \
                   0x63a:0xfecd, 0x641:0xfed1, 0x642:0xfed5, 0x643:0xfed9, 0x644:0xfedd, 0x645:0xfee1, \
                   0x646:0xfee5, 0x647:0xfee9, 0x648:0xfeed, 0x649:0xfeef, 0x64a:0xfef1, 0xfefb:0xfefb}
    
    charInitialForm = {0x626:0xfe8b, 0x628:0xfe91, 0x62a:0xfe97, 0x62b:0xfe9b, 0x62c:0xfe9f, 0x62d:0xfea3, \
                   0x62e:0xfea7, 0x633:0xfeb3, \
                   0x634:0xfeb7, 0x635:0xfebb, 0x636:0xfebf, 0x637:0xfec3, 0x638:0xfec7, 0x639:0xfecb, \
                   0x63a:0xfecf, 0x641:0xfed3, 0x642:0xfed7, 0x643:0xfedb, 0x644:0xfedf, 0x645:0xfee3, \
                   0x646:0xfee7, 0x647:0xfeeb, 0x64a:0xfef3}
    
    charMedialForm = {0x628:0xfe92, 0x62a:0xfe98, 0x62b:0xfe9c, 0x62c:0xfea0, 0x62d:0xfea4, \
                   0x62e:0xfea8, 0x633:0xfeb4, \
                   0x634:0xfeb8, 0x635:0xfebc, 0x636:0xfec0, 0x637:0xfec4, 0x638:0xfec8, 0x639:0xfecc, \
                   0x63a:0xfed0, 0x641:0xfed4, 0x642:0xfed8, 0x643:0xfedc, 0x644:0xfee0, 0x645:0xfee4, \
                   0x646:0xfee8, 0x647:0xfeec, 0x64a:0xfef4}
    
    charFinalForm = {0x622:0xfe82, 0x623:0xfe84, 0x627:0xfe8e, 0x628:0xfe90, 0x629:0xfe94, 0x62a:0xfe96, 0x62b:0xfe9a,\
                   0x62c:0xfe9e, 0x62d:0xfea2, \
                   0x62e:0xfea6, 0x62f:0xfeaa, 0x630:0xfeac, 0x631:0xfeae, 0x632:0xfeb0, 0x633:0xfeb2, \
                   0x634:0xfeb6, 0x635:0xfeba, 0x636:0xfebe, 0x637:0xfec2, 0x638:0xfec6, 0x639:0xfeca, \
                   0x63a:0xfece, 0x641:0xfed2, 0x642:0xfed6, 0x643:0xfeda, 0x644:0xfede, 0x645:0xfee2, \
                   0x646:0xfee6, 0x647:0xfeea, 0x648:0xfeee, 0x649:0xfef0, 0x64a:0xfef2, 0xfefb:0xfefc, 0x624:0xfe86 }

        
