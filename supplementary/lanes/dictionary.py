

from constants import DICTIONARY_FILEPATH

dictionary_words = set([])

def _load_dictionary():
    global dictionary_words
    print('load dictionary')
    for word in open(DICTIONARY_FILEPATH).readlines():
        word = word.strip()
        if word.endswith("'s"):
            continue
        dictionary_words.add(word)
    print('end load dictionary: ', len(dictionary_words), 'found')
    dictionary_words.add('TA')

def get_likely_words_in_dictionary(word):
    """
    return a sorted list of tuples of (word, probability), sorted by probability
    """
    global dictionary_words
    matches = []
    if word in dictionary_words:
        matches.append((word, 1.0))
    else:
        
        
        
    def get_prob(x):
        return x[1]
    matches.sort(key=get_prob)
    return matches


_load_dictionary()