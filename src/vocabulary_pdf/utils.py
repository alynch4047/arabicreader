import os
import logging

from data.unicode_data import *

from vocabulary_pdf.constants import encoding, ARABIC_FONT_SIZE
from vocabulary_pdf.type1 import type1font

l = logging.getLogger(__name__)

def get_resource_file_path(resource_name):
    resource_name = resource_name.replace('\\', '/')
    file_ = __file__.replace('\\', '/')
    _this_dir = os.sep.join(file_.split('/')[:-1])
    l.debug('path is %s', os.path.join(_this_dir, resource_name))
    return os.path.join(_this_dir, resource_name)

# set char widths
try:
    _font = type1font(get_resource_file_path('BAGHD___.PFB'))
    _font.load()
    _font.parse()
    _font.loadAFM(get_resource_file_path("BAGHD___.AFM"))
except:
    logging.exception('getting font')

TASHKEEL = (0x64B, 0x64C, 0x64D, 0x64E, 0x64F, 0x650, 0x651, 0x652, 0x640)
    
    
def unicode_to_baghdad(letter):
    if letter >= 0xfe70:
        baghdad_code = letter - 0xfe70 + 50
    else:
        baghdad_code = letter
    return baghdad_code

PRESENTATION_FATHATAAN = 0xfe71
PRESENTATION_DAMMATAAN = 0xfe72
PRESENTATION_KASRATAAN = 0xfe74
PRESENTATION_FATHA     = 0xfe77
PRESENTATION_DAMMA     = 0xfe79
PRESENTATION_SHADDA    = 0xfe7d

PRESENTATION_KASRA     = 0xfe7b
PRESENTATION_SUKUUN    = 0xfe7f

TASHKEEL_CODE_UPPER = [PRESENTATION_FATHA, PRESENTATION_DAMMA, PRESENTATION_SUKUUN,
                       PRESENTATION_FATHATAAN, PRESENTATION_DAMMATAAN,
                       PRESENTATION_SHADDA]

TASHKEEL_CODE_LOWER = [PRESENTATION_KASRA, PRESENTATION_KASRATAAN]

TASHKEEL_CODE       = TASHKEEL_CODE_UPPER + TASHKEEL_CODE_LOWER


def encode_text(text):
    # text has already been shaped, therefore is in 0xfe range
    encodedText = ''
    for i in text:
        unicharindex = ord(i)
        if unicharindex == 1600: #u'\u0640'
            continue
        if unicharindex >= 0xfe70:
            type1code = unicharindex - 0xfe70 + 50
        else:
            type1code = unicharindex
        if type1code >= 0 and type1code < 256:
            encodedText += chr(type1code) # basic glyph for Baghdad
        
        else:
            #print "codes are ",unicharindex,type1code
            raise Exception('Cant encode ord %s %s', unicharindex, i)
    return encodedText


def strip_tashkeel(text):
    """ gets a list of tuples providing the tashkeel details,
    and returns the original string with the tashkeel removed"""
    tashkeel = []
    stripped_text = ''
    for i in range(len(text)):
        #print "i = ",i
        if ord(text[i]) in TASHKEEL:
            # we have tashkeel
            tashkeel.append((i, text[i]))
            #print "note tashkeel",repr(tashkeel)
        else:
            stripped_text += text[i]
            #print "add letter ", repr(text[i])
    return tashkeel, stripped_text


def replace_tashkeel(text, tashkeel):
    """ takes a list of tuples detailing tashkeel, and inserts the tashkeel into a string """
    for i in range(len(tashkeel)):
        tashkeel_position = tashkeel[i][0]
        tashkeel_char = tashkeel[i][1]
        text = text[:tashkeel_position] + tashkeel_char + text[tashkeel_position:]
    return text


def strip_tashkeel_with_location(x, y, text):
    """ gets a list of tuples providing the tashkeel details including location of seat letter,
    and returns the original string with the tashkeel removed.
    Note that this string is composed of shaped unicode presentation text"""

    l.debug('word is %s', text)
    _letters = tuple(map(ord, (list(text))))
    l.debug('ords are ' + '%x '*len(text) % _letters)

    tashkeel = []
    
    stripped_text = ''
    for i in range(len(text)):
        #print "i = ",i
        l.debug('ord is %x', ord(text[i]))
        if ord(text[i]) in TASHKEEL_CODE:
            over_shadda = False
            l.debug('taskeel is %x', ord(text[i]))
            tashkeel_char = text[i]
            tashkeel_ord = ord(text[i])
            seat_ord = ord(text[i-1])
            if seat_ord in TASHKEEL_CODE:
                if seat_ord == PRESENTATION_SHADDA:
                    over_shadda = True
                seat_ord = ord(text[i-2])
            seat_char = text[i-1]
            
            if i == len(text) - 1:
                following_char = None
            else:
                following_char = text[i+1]
            if seat_ord and tashkeel_ord and following_char:
                l.debug('ords are %x %x %x over shadda: %s', seat_ord, tashkeel_ord, ord(following_char), over_shadda)
                l.debug('chars are %s %s %s', seat_char, tashkeel_char, following_char)
            
            # work out its current location, and correct depending on the seat glyph
            newx = x - get_string_width(text[:i+1], ARABIC_FONT_SIZE)
            newy = y
            
            # adjust position depending on seat character
            min_height, max_height, width = get_char_details(seat_ord)
            l.debug('seat size is %s %s %s', min_height, max_height, width)
            h_min_height, h_max_height, h_width = get_char_details(tashkeel_ord)
            l.debug('tashkeel size is %s %s %s', h_min_height, h_max_height, h_width)
            if over_shadda:
                shadda_y = tashkeel[-1][3]
                l.debug('shadda y is %s', shadda_y)
                if tashkeel_ord in [PRESENTATION_FATHATAAN, PRESENTATION_FATHA,
                                    PRESENTATION_DAMMATAAN, PRESENTATION_DAMMA,
                                    PRESENTATION_SUKUUN]:
                    newy = shadda_y + 200 * ARABIC_FONT_SIZE / 1000
                elif  tashkeel_ord in [PRESENTATION_KASRATAAN, PRESENTATION_KASRA]:
                    tashkeel_char = chr(PRESENTATION_FATHA)
                    newy = shadda_y - 130 * ARABIC_FONT_SIZE / 1000
            else:
                if tashkeel_ord in TASHKEEL_CODE_UPPER:
                    if h_min_height < (max_height + 80):
                        offset = (max_height + 80) - h_min_height
                        l.debug('haraka too low by %s', offset)
                        newy += offset * ARABIC_FONT_SIZE / 1000
                    if h_min_height > (max_height + 80):
                        offset = h_min_height - (max_height + 80)
                        l.debug('haraka too high by %s', offset)
                        newy -= offset * ARABIC_FONT_SIZE / 1000
                elif tashkeel_ord in TASHKEEL_CODE_LOWER:
                    if h_max_height < (min_height - 80):
                        l.debug('haraka too low')
                        newy += ((min_height - 80) - h_max_height) * ARABIC_FONT_SIZE / 1000
            if width > 400:
                newx = newx + (width - 400) * ARABIC_FONT_SIZE / 1000
            
            tashkeel.append([i, tashkeel_char, newx, newy])
        else:
            stripped_text += text[i]
    return tashkeel, stripped_text


def get_char_details(unicode_letter):
    baghdad_code = unicode_to_baghdad(unicode_letter)
    charSize = _font.charSize[encoding[baghdad_code][1:]]
    max_height = float(charSize[3])
    min_height = float(charSize[1])
    width = float(charSize[2]) - float(charSize[0])
    return min_height, max_height, width


def presentation_tashkeel(text):
    """ change tashkeel from unicode 0x0600 to presentation form """
    text = text.replace(chr(0x64b),chr(0xfe71))
    text = text.replace(chr(0x64c),chr(0xfe72))
    text = text.replace(chr(0x64d),chr(0xfe74))
    text = text.replace(chr(0x64e),chr(0xfe77))
    text = text.replace(chr(0x64f),chr(0xfe79))
    text = text.replace(chr(0x650),chr(0xfe7b))
    text = text.replace(chr(0x651),chr(0xfe7d))
    text = text.replace(chr(0x652),chr(0xfe7f))
    return text


def reverse_phrase(text):
    ret = ''
    words = text.split()
    for i in range(len(words)):
        j = len(words) - i - 1 # reverse word order too
        word = words[j]
        if ret != '':
            ret += ' '
        ret += reverse(word)
    return ret


def reverse(text):
    rev = ''
    for i in range(len(text)):
        rev += text[len(text) - i - 1]
    return rev


def encode(text):
    return str(text).encode('UTF-8')


def decode(text):
    return text.decode('UTF-8') if isinstance(text, bytes) else text


def get_string_width(text, fontSize):
    """ get widths of each character in the string and return the total width (needs text to be shaped already)"""
    text = encode_text(text)
    width = 0
    for char in text:
        code = ord(char)
        if code < len(encoding):
            charName = encoding[code][1:]
            if charName not in _font.charWidths.keys():
                print(charName, "not in widths")
                raise LookupError
            else:
                width += _font.charWidths[charName]
        else:
            raise LookupError
    return width * fontSize / 1000.0

