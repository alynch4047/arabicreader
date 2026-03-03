
import unittest

from dictionary import get_likely_words_in_dictionary


class TestDictionary(unittest.TestCase):
    
    def test_find_beconaang(self):
        word = 'beconaang'
        words = get_likely_words_in_dictionary(word)
        self.assert_(len(words) > 0)
        most_likely_word, probability = words[-1]
        self.assertEqual('becoming', most_likely_word)