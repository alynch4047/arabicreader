
from gamera.core import *
from constants import *
from gamera.plugins import image_utilities

from utils import get_x_coord, get_y_coord, glyph_name, glyph_long_name
from dictionary import get_likely_words_in_dictionary
       
       
class Word(object):
    
    classifier = None
    
    def __init__(self, initial_cc=None):
        
        self.initial_cc = initial_cc
        self.char_set = CHAR_SET_ROMAN
        self.chrs = []
        self.ccs = []
        
        if initial_cc is not None:
            self.ccs = [initial_cc]
            self.offset_x = initial_cc.offset_x
            self.ncols = initial_cc.ncols
        else:
            self.ccs = []
            self.offset_x = 0
            self.ncols = 0
            
    def calculate_chrs(self):
        self.ccs.sort(key=get_x_coord)
        available_word_ccs = [self.ccs[:]]
        _get_available_words(self.ccs, Word.classifier, available_word_ccs)
#        self.chrs =_get_str_from_glyphs(available_word_ccs[-1])
        self.chrs = _get_best_fit_word(available_word_ccs)
    
def _get_best_fit_word(available_word_ccs):
    """
    Find possible word matches in the dictionary and return the most likely match
    
    @param available_word_ccs: a list of lists of ccs, each list of ccs being a possible word 
    """
    word_probabilities = []
    for word_ccs in available_word_ccs:
        word = _get_str_from_glyphs(word_ccs)
        likely_words = get_likely_words_in_dictionary(word)
        print('likely words for', word, 'is', likely_words)
        word_probabilities.extend(likely_words)
    if len(word_probabilities) == 0:
        word = _get_str_from_glyphs(available_word_ccs[-1])
        print(word, 'not found in dictionary')
        return word
    def get_prob(x):
        return x[1]
    word_probabilities.sort(key=get_prob)
    most_likely_match = word_probabilities[-1]
    print(most_likely_match[0], 'found in dictionary with probability', most_likely_match[1])
    return most_likely_match[0]
        
def _get_available_words(ccs, classifier, available_words, level=0):
    """
    append available_words with lists of possible classified ccs, each list of classified ccs is a possible
    word that the word image could represent 
    """
    level += 1
    new_ccs_split = []
    for ix, cc in enumerate(ccs):
        classifier.classify_list_automatic([cc])
        long_name = glyph_long_name(cc)
        print(long_name, cc.ncols, cc.get_confidence())
        is_capital = (long_name.find('capital') != -1)
        if is_capital:
            max_width = 35
        else:
            max_width = 20
        current_confidence = cc.get_confidence()
        replace = False
        if current_confidence < 0.3 and cc.ncols > max_width:
            print('try split this char into', end=' ')
            replace_ccs = cc.splitx()
            classifier.classify_list_automatic(replace_ccs)
            print([glyph_name(c) for c in replace_ccs])
            confidences = [c.get_confidence() for c in replace_ccs]
            avg_confidence = sum(confidences) / len(confidences)
            print('new confidences are', confidences, avg_confidence)
            if (avg_confidence) > current_confidence:
                # XXX don't split m into ni
                if glyph_name(cc) == 'm' and _get_str_from_glyphs(replace_ccs) == 'ni':
                    pass
                else:
                    print('(replace)')
                    replace = True
        if replace:
            new_ccs_split.extend(replace_ccs)
        else:
            new_ccs_split.append(cc)
            
    if new_ccs_split != ccs:
        available_words.append(new_ccs_split[:])
        
    # try joining original ccs
    new_ccs_joined =_join_broken_ccs(ccs, classifier)
    if new_ccs_joined != ccs:
        available_words.append(new_ccs_joined[:])
            
    # try joining with split ccs
    new_ccs_joined =_join_broken_ccs(new_ccs_split, classifier)
    if new_ccs_joined != new_ccs_split:
        available_words.append(new_ccs_joined[:])
            
    if level < 2:
        _get_available_words(new_ccs_joined, classifier, available_words, level)


def _join_broken_ccs(ccs, classifier):
    if len(ccs) == 0:
        return []
    new_ccs = []
    ix = 0
    while True:
        cc_pair = ccs[ix:ix+2]
        confidences = [c.get_confidence() for c in cc_pair]
        avg_confidence = sum(confidences) / len(confidences)
        joined_cc = image_utilities.union_images(cc_pair)
        classifier.classify_list_automatic([joined_cc])
        confidence = joined_cc.get_confidence()
        if confidence > avg_confidence:
            print('join glyphs', [glyph_name(c) for c in cc_pair], 'to make', glyph_name(joined_cc))
            new_ccs.append(joined_cc)
            ix += 2
        else:
            new_ccs.append(ccs[ix])
            ix += 1
        if ix == len(ccs) - 1:
            new_ccs.append(ccs[ix])
            break
        if ix >= len(ccs):
            break
    print('before joining:', _get_str_from_glyphs(ccs))
    print('after joining', _get_str_from_glyphs(new_ccs))

    return new_ccs


def _get_str_from_glyphs(glyphs):
    str = ''
    for c in glyphs:
        str += _get_chr_from_classification(c)
    return str
    
    
def _get_chr_from_classification(c):
    chr_name = glyph_name(c)
    long_name = glyph_long_name(c)
    chr = replace_char(chr_name)
    if long_name.find('capital') != -1:
        chr = chr.upper()
    return chr
    
    
def replace_char(chr):
    if chr == 'lbracket': return '('
    if chr == 'rbracket': return ')'
    if chr == 'lsquarebracket': return '['
    if chr == 'rsquarebracket': return ']'
    if chr == 'comma': return ','
    if chr == 'longunderscore': return '__'
    if chr == 'downarrow': return '%'
    if chr == 'stop': return '.'
    if chr == 'ampersand': return '&'
    if chr == 'hyphen': return '-'
    if chr == 'star': return '*'
    return chr


def split_chars(ccs):
    additions = []
    remove_ixs = []
    for ix, c in enumerate(ccs[:]):
#        print 'id_name',c.id_name 
        if glyph_name(c).startswith('split'):
            split_op = glyph_name(c)
            if split_op == 'splitx':
                split_chrs = c.splitx()
            elif split_op == 'splitx_right':
                split_chrs = c.splitx_right()
            else:
                raise Exception('unknown op: %s' % split_op)
            Word.classifier.classify_list_automatic(split_chrs)
            additions.extend(split_chrs)
            remove_ixs.append(ix)
    for ix in reversed(remove_ixs):
        del ccs[ix]
    ccs.extend(additions)
    if len(remove_ixs) > 0:
        split_chars(ccs)
        
    ccs.sort(key=get_x_coord)