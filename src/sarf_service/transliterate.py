
import logging

from data.unicode_data import *

l = logging.getLogger(__name__)


transliterate_gb = {
ALIF: 'A',
BAA: 'b',
TAA_MARBUTA:  '$',
TAA:    't',
THAA:   'th',
JIIM:   'j',
HAA_:   'H',
KHAA:   'K',
DAAL:   'd',
DHAAL:  'dh',
RAA:    'r',
ZAAL:   'z',
SIIN:   's',
SHIIN:  'sh',
SAAD:   'S',
DAAD:   'D',
TAA_:   'T',
DHAA_:  'DH',
AYN:    'c',
GHAYN:  'gh',
FAA:    'f',
QAAF:   'q',
KAAF:   'k',
LAAM:   'l',
MIIM:   'm',
NUUN:   'n',
HAA :   'h',
WAAW:   'w',
YAA :   'y',
HAMZA:  "'",

FATHA: 'a',
DAMMA: 'u',
KASRA: 'i',

SHADDA: '2',

           }

def transliterate_to_gb(arabic_word):
    gb_word = ''
    for letter in arabic_word:
        if letter in transliterate_gb:
            gb_word += transliterate_gb[letter]
            
    return gb_word

def out_in_gb(text_list):
    out_list = []
    if not type(text_list) == list:
        text_list = [text_list]
    for text in text_list:
        out_list.append(transliterate_to_gb(text))
    return ' '.join(out_list)
            