
import logging

from traits.api import HasTraits, Str, Int, CInt, List, Unicode

from data.unicode_data import ALIF

from sarf_service.api import (Word, constants, check_security,
                              transliterate_to_gb, to_core_letters)

l = logging.getLogger(__name__)


class Variation(HasTraits):
    
    kalvar_id = CInt
    
    text = Unicode
    
    number = CInt
    
    tense = CInt
    
    def get_data_for_json(self):
        return [self.kalvar_id, self.text, self.number, self.tense]
    
    def __repr__(self):
        return '<Variation %s %s %s %s>' % (self.kalvar_id, transliterate_to_gb(self.text),
                                            self.number, self.tense) 


class WordSet(HasTraits):
    
    kalima_id = CInt
    
    word_type = CInt
    
    meaning = Unicode
    
    root_f = Unicode
    
    root_c = Unicode
    
    root_l = Unicode
    
    variations = List
    
    def validate(self):
        if not self.meaning:
                raise Exception('You must enter an english meaning for the word')
        for variation in self.variations:
            if not variation.text:
                raise Exception('You must enter arabic text for all the words')
    
    def get_words(self):
        words = []
        for variation in self.variations:
            words.append( Word(root=self.root_f + self.root_c + self.root_l,\
                        word_type=self.word_type,
                        kalima_id=self.kalima_id,
                        id=variation.kalvar_id,
                        meaning=self.meaning,
                        number=variation.number,
                        text=variation.text,
                        tense=variation.tense))
        return words
    
    def get_data_for_json(self):
        variations_data = [variation.get_data_for_json() for variation in self.variations]
        return [self.kalima_id, self.word_type, self.meaning, 
                self.root_f + self.root_c + self.root_l, variations_data]
        
    def populate_from_args(self, args):
        variations_by_id = {}
        for key, value in args.items():
            l.debug('key, value is %s %s', key, value)
            if key == 'kalima_id' and value.upper() == 'NEW':
                    value = 0;
            
            if key in ['kalima_id', 'word_type', 'root_f', 'root_c', 'root_l',
                       'meaning']:
                #l.debug('set %s to %s', key, value)
                setattr(self, key, value)
            else:
                variation_id = key.split('_')[-1]
                key = '_'.join(key.split('_')[:-1])
                if key == 'kalvar_id' and value.upper() == 'NEW':
                    value = 0;
                if variation_id not in variations_by_id:
                    variation = Variation()
                    variations_by_id[variation_id] = variation
                variation = variations_by_id[variation_id]
                #l.debug('set var %s %s to %s', variation_id, key, value)
                setattr(variation, key, value)
                #l.debug('vars by id is %s', variations_by_id)
        self.variations = list(variations_by_id.values())
        l.debug('form data is %s', repr(self))

        self._make_root_canonical()
        check_security(self.meaning)
        for variation in self.variations:
            check_security(variation.text)
            try:
                core_text = to_core_letters(variation.text)
            except Exception as ex:
                raise Exception(
            'Sorry, the arabic text contains an invalid (non-arabic) character')

    def populate_from_url(self, url):
        variations_by_id = {}
        form_data_pairs = url.split('&')
        for key_value_pair in form_data_pairs:
            #l.debug('unpack %s', key_value_pair)
            key, value = key_value_pair.split('=')
            if key == 'kalima_id' and value.upper() == 'NEW':
                    value = 0;
            
            if key in ['kalima_id', 'word_type', 'root_f', 'root_c', 'root_l',
                       'meaning']:
                #l.debug('set %s to %s', key, value)
                setattr(self, key, value)
            else:
                variation_id = key.split('_')[-1]
                key = '_'.join(key.split('_')[:-1])
                if key == 'kalvar_id' and value.upper() == 'NEW':
                    value = 0;
                if variation_id not in variations_by_id:
                    variation = Variation()
                    variations_by_id[variation_id] = variation
                variation = variations_by_id[variation_id]
                #l.debug('set var %s %s to %s', variation_id, key, value)
                setattr(variation, key, value)
                #l.debug('vars by id is %s', variations_by_id)
        self.variations = list(variations_by_id.values())
        l.debug('form data is %s', repr(self))

        self._make_root_canonical()
        check_security(self.meaning)
        for variation in self.variations:
            check_security(variation.text)
            try:
                core_text = to_core_letters(variation.text)
            except Exception as ex:
                raise Exception(
            'Sorry, the arabic text contains an invalid (non-arabic) character')

    def _make_root_canonical(self):
        try:
            self.root_f = to_core_letters(self.root_f)
            self.root_c = to_core_letters(self.root_c)
            self.root_l = to_core_letters(self.root_l)
        except Exception as ex:
            raise Exception('One or more of the root letters is not valid (%s)' % ex)
        
        if self.root_f == ALIF or self.root_c == ALIF or self.root_l == ALIF:
            raise Exception("Sorry, the root cannot contain alif. Did you mean hamza, yaa' or waaw?")

    def __repr__(self):
        return '<FormData %s %s %s %s>' % (
                                    self.kalima_id, 
                                    self.word_type, self.meaning,
                                    ''.join([repr(var) for var in self.variations]))
        

def make_word_set_from_url(url):
    if url[:5] == 'form?':
        url = url[5:]
    elif url[:10] == 'form/json?':
        url = url[10:]
    else:
        raise Exception('Cannot understand URL')
    word_set = WordSet()
    word_set.populate_from_url(url)
    return word_set


def make_word_set_from_args(args):
    if 'form' in args:
        del args['form']
    word_set = WordSet()
    word_set.populate_from_args(args)
    return word_set

        
def make_word_set_from_words(words):
    from vocab_db_service.api import WordSet, Variation
    first_word = words[0]
    try:
        root_f = first_word.root[0]
    except:
        root_f = ''
    try:
        root_c = first_word.root[1]
    except:
        root_c = ''
    try:
        root_l = first_word.root[2]
    except:
        root_l = ''
        
    word_set = WordSet(kalima_id=first_word.kalima_id,
                       meaning=first_word.meaning,
                       root_f=root_f,
                       root_c=root_c,
                       root_l=root_l,
                       word_type=first_word.word_type)
    for word in words:
        variation = Variation(kalvar_id=word.id,
                              text=word.text,
                              tense=word.tense,
                              number=word.number)
        word_set.variations.append(variation)
    return word_set

