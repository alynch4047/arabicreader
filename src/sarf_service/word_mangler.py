import logging

from data.unicode_data import *

l = logging.getLogger(__name__)

def check_security(text):
    for chars in ['<', '>', '[', ']', '@', '=', '%3C', '%3E']:
        if text.find(chars) != -1:
            raise Exception(
                'Sorry! The text/letter "%s" is not allowed in the word database' % chars)

def to_core_letters(word_text):
    """ Convert all the letters to the core form, so there is only one hamza, one yaa' etc.
    """
    core_word_text = ''
    for letter in word_text:
     if letter in CORE_LETTERS or letter in CANONICAL_VOWELS:
         core_word_text += letter
     elif letter in CORE_FORMS_LOOKUP:
         core_word_text += CORE_FORMS_LOOKUP[letter]
     else:
         l.error('%s %s is not a known letter (%s)' % (letter, repr(letter), word_text))
#         raise Exception('%s is not a known letter' % repr(letter))
    # now re-arrange shaddas to not have haraka on them
    core_word_text = _switch_shaddas(core_word_text)
    return core_word_text

def to_canonical_letters(word_text):
    """Convert non-canonical letters to the canonical counterpart i.e. the 0x0600 code page,
     and also sequence the shadda so that it comes after the haraka"""
    canonical_word_text = ''
    for letter in word_text:
     if letter in CANONICAL_LETTERS or letter in CANONICAL_VOWELS:
         canonical_word_text += letter
     elif letter in ALTERNATIVE_FORMS_LOOKUP:
         canonical_word_text += ALTERNATIVE_FORMS_LOOKUP[letter]
     else:
         l.error('%s %s is not a known letter (%s)' % (letter, repr(letter), word_text))
#         raise Exception('%s is not a known letter' % repr(letter))
    # now re-arrange shaddas to not have haraka on them
    canonical_word_text = _switch_shaddas(canonical_word_text)
    return canonical_word_text

def _switch_shaddas(text):
    """Reorder the word, if necessary, so that shaddas are effectively treated
    as a separate letter. I.e. ensure that any shadda appears after any vowel on
    a letter e.g.
    SHEEN + SHADDA + KASRA -> SHEEN + KASRA + SHADDA 
    """
    switched_text = ''
    pending_shadda = False
    for letter in text:
        if letter == SHADDA:
            pending_shadda = True
        elif letter in CANONICAL_VOWELS:
            switched_text += letter
        elif letter in CANONICAL_LETTERS:
            if pending_shadda:
                switched_text += SHADDA
                pending_shadda = False
            switched_text += letter
        else:
            switched_text += letter
    if pending_shadda:
                switched_text += SHADDA
    return switched_text
    
def strip_harakaat(word_text):
    stripped_word_text = ''
    for letter in word_text:
        if letter not in CANONICAL_VOWELS:
            stripped_word_text += letter
    return stripped_word_text

def get_word_haraka_pairs(word_text):
    if len(word_text) == 0:
        return []
    assert(word_text[0] in CANONICAL_LETTERS, '%s is not canonical' % word_text[0])
    if len(word_text) == 1:
        return [(word_text[0], None)]
    if word_text[1] in CANONICAL_VOWELS:
        pairs = [(word_text[0], word_text[1])]
        remaining_pairs = get_word_haraka_pairs(word_text[2:])
        pairs.extend(remaining_pairs)
        return pairs
    elif word_text[1] in CANONICAL_LETTERS:
        pairs = [(word_text[0], None)]
        remaining_pairs = get_word_haraka_pairs(word_text[1:])
        pairs.extend(remaining_pairs)
        return pairs
    else:
        raise Exception('invalid arabic word (second letter invalid): %s %s' % 
                        (word_text, word_text[1]))

def arabic_string_matches(wordA, wordB,
                          allow_omitted_shadda_in_a=False,
                          alif_can_be_hamza=False):
    """ Check if these words match, if a haraka is missing then ignore it.
    First break words down in (letter, haraka) pairs, then compare.
    allow_omitted_shadda_in_a means that it still matches if wordA is missing a shadda
    found in wordB.
    alif_can_be_hamza means that alifs and hamzas are considered interchangeable,
    which unfortunately is the case in the minds of most typists of arabic.
    """
    if alif_can_be_hamza:
        # convert alifs to hamza so that they will equate
        wordA = _convert_alifs_to_hamzas(wordA)
        wordB = _convert_alifs_to_hamzas(wordB)
    
    pairsA = get_word_haraka_pairs(wordA)
    pairsB = get_word_haraka_pairs(wordB)
    
    if not _shaddas_match(pairsA, pairsB, allow_omitted_shadda_in_a):
        return False
    
    # remove all shaddas before comparison
    pairsA = [pair for pair in pairsA if pair[0] != SHADDA]
    pairsB = [pair for pair in pairsB if pair[0] != SHADDA]

    if len(pairsA) != len(pairsB):
        return False
    for ix, pairA in enumerate(pairsA):
        pairB = pairsB[ix]
        if pairA[0] != pairB[0]:
            return False
        elif (pairA[1] is None) or (pairB[1] is None):
            continue
        elif pairA[1] == pairB[1]:
            continue
        else:
            return False
    return True

def _convert_alifs_to_hamzas(word_text):
    return word_text.replace(ALIF, HAMZA)

def _shaddas_match(pairsA, pairsB, allow_omitted_shadda_in_a):
    """ Do the shaddas in these two words match if we ignore the other letters?"""
    shaddas_locations_a = _get_shadda_locations(pairsA)
    shaddas_locations_b = _get_shadda_locations(pairsB)
    for location in shaddas_locations_b:
        if location not in shaddas_locations_a:
            if not allow_omitted_shadda_in_a:
                return False
    for location in shaddas_locations_a:
        if location not in shaddas_locations_b:
            return False
    return True

def _get_shadda_locations(pairs):
    ix = 0
    locations = []
    for pair in pairs:
        if pair[0] == SHADDA:
            locations.append(ix)
        else:
            ix += 1
    return locations


        
        