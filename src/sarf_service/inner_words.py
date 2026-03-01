# -*- coding: utf-8 -*-
import logging

from traits.api import HasTraits
from traits.api import Instance

from data.unicode_data import *
from sarf_service.constants import *

from sarf_service.word_mangler import to_canonical_letters, get_word_haraka_pairs
from sarf_service.transliterate import transliterate_to_gb

l = logging.getLogger(__name__)

# operations
PAST_TU = 'past tu'
PAST_TI = 'past ti'
PAST_TA = 'past ta'
PAST_AT = 'past at'
PAST_NAA = 'past naa'
PAST_UU = 'past uu'

PRESENT_A_U = 'present a u'
PRESENT_TA_U = 'present ta u'
PRESENT_NA_U = 'present na u'
PRESENT_YA_UUNA = 'present ya uuna'
PRESENT_TA_UUNA = 'present ta uuna'

SUFFIX_KASRA = 'suffix kasra'

SUFFIX_II = 'suffix ii'
SUFFIX_NII = 'suffix nii'
SUFFIX_HU = 'suffix hu'
SUFFIX_HAA = 'suffix haa'
SUFFIX_HUM = 'suffix hum'
SUFFIX_KUM = 'suffix kum'
SUFFIX_KA = 'suffix ka'
SUFFIX_KI = 'suffix ki'
SUFFIX_UUNA = 'suffix uuna' # sound plural
SUFFIX_IINA = 'suffix iina' # sound plural
SUFFIX_AANI = 'suffix aani'
SUFFIX_AYNI = 'suffix ayni'

SUFFIX_TAA_MARBUTA = 'suffix taa marbuta'
SUFFIX_AAT = 'suffix aat'

SUFFIX_IYA = 'suffix iya'

SUFFIX_AN = 'suffix an'

SWITCH_TAA_MARBUTA = 'switch taa marbuta'

PREFIX_WAAW = 'prefix waaw'
PREFIX_KAAF = 'prefix kaaf'
PREFIX_AL = 'prefix al'
PREFIX_LIL = 'prefix lil'
PREFIX_LI = 'prefix li'
PREFIX_BI = 'prefix bi'
PREFIX_BIL = 'prefix bil'
PREFIX_FA = 'prefix fa'
PREFIX_SA = 'prefix sa'

AMR_SINGULAR = 'amr singular'
AMR_PLURAL = 'amr plural'

MAJZUUM_TA_SUKUUN = 'majzuum ta sukuun'
MAJZUUM_TA_UU = 'majzuum ta uu'
MAJZUUM_YA_SUKUUN = 'majzuum ya sukuun'
MAJZUUM_YA_UU = 'majzuum ya uu'

def append_text_op(text_ops, text, op, previous_ops):
    #l.debug('1 %s %s previous ops: %s', text_ops, text, previous_ops)
    new_ops = previous_ops[:]
    new_ops.append(op)
    #l.debug('2 new ops %s', new_ops)
    text_ops.append((text, new_ops))
    #l.debug('3 new text_ops %s', text_ops)


class InnerWords(HasTraits):
    """ The InnerWords class provides the possible inner words of some text. Words
    are returned together with a list of operations performed to get the result"""
    
    word_database = Instance('dictionary_service.api.WordDatabase')
    
    def get_inner_word_texts(self, word_text):
        assert(word_text == to_canonical_letters(word_text))
        possible_text_ops = [(word_text, [])]
        possible_text_ops += self._get_inner_word_texts_prefixes(word_text, [])
        l.debug('ptos after prefix: %s', possible_text_ops)
        for possible_text, ops in possible_text_ops[:]:
            # consider variations where prefix and suffix are present so
            # both need to be stripped
            possible_text_ops += \
                self._get_inner_word_texts_suffixes(possible_text, ops)
        l.debug('ptos after suffix: %s', possible_text_ops)
        for possible_text, ops in possible_text_ops[:]:
            # consider verbal variations 
            possible_text_ops += \
                self._get_inner_word_texts_verbs(possible_text, ops)
        l.debug('ptos after verbs: %s', possible_text_ops)
        for word, reason in possible_text_ops:
            l.debug('word suggestion is %s %s', word, transliterate_to_gb(word))
        return possible_text_ops
    
    def _get_inner_word_texts_verbs(self, word_text, previous_ops):
        possible_text_ops = []
        possible_text_ops += self._get_inner_word_texts_verbs_past(word_text, previous_ops)
        possible_text_ops += self._get_inner_word_texts_verbs_present(word_text, previous_ops)
        possible_text_ops += self._get_inner_word_texts_verbs_present_4(word_text, previous_ops)
        possible_text_ops += self._get_inner_word_texts_verbs_majzuum_or_amr(word_text, previous_ops)
        return possible_text_ops

    def _get_inner_word_texts_verbs_past(self, word_text, previous_ops):
        possible_text_ops = []
        haraka_pairs = get_word_haraka_pairs(word_text)
        if len(haraka_pairs) == 0:
            return []
        last_haraka_pair = haraka_pairs[-1]
        if len(haraka_pairs) < 2:
            return possible_text_ops
        second_last_haraka_pair = haraka_pairs[-2]
       
        # test for TU
        if last_haraka_pair in [(TAA, DAMMA), (TAA, None)]:
            if second_last_haraka_pair[1] in (None, SUKUUN):
                stripped_word = self._strip_final_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PAST_TU, previous_ops)
        # test for TI
        if last_haraka_pair in [(TAA, KASRA), (TAA, None)]:
            if second_last_haraka_pair[1] in (None, SUKUUN):
                stripped_word = self._strip_final_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PAST_TI, previous_ops)
        # test for TA
        if last_haraka_pair in [(TAA, FATHA), (TAA, None)]:
            if second_last_haraka_pair[1] in (None, SUKUUN):
                stripped_word = self._strip_final_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PAST_TA, previous_ops)        # test for AT
        if last_haraka_pair in [(TAA, SUKUUN), (TAA, None)]:
            if second_last_haraka_pair[1] in (None, FATHA):
                stripped_word = self._strip_final_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PAST_AT, previous_ops)
        # test for NAA
        if last_haraka_pair in [(ALIF, SUKUUN), (ALIF, None)]:
            if second_last_haraka_pair in [(NUUN, FATHA), (NUUN, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, 2)
                append_text_op(possible_text_ops, stripped_word, PAST_NAA, previous_ops)
        # test for UU
        if last_haraka_pair in [(ALIF, SUKUUN), (ALIF, None)]:
            if second_last_haraka_pair in [(WAAW, SUKUUN), (WAAW, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, 2)
                append_text_op(possible_text_ops, stripped_word, PAST_UU, previous_ops)
                
        return possible_text_ops
    
    def _get_inner_word_texts_verbs_present(self, word_text, previous_ops):
        possible_text_ops = []
        haraka_pairs = get_word_haraka_pairs(word_text)
        if len(haraka_pairs) == 0:
            return []
        first_haraka_pair = haraka_pairs[0]
        if len(haraka_pairs) > 1:
            second_haraka_pair = haraka_pairs[1]
        else: 
            second_haraka_pair = None
        last_haraka_pair = haraka_pairs[-1]
        if len(haraka_pairs) < 2:
            return possible_text_ops
        second_last_haraka_pair = haraka_pairs[-2]
       
        # test for AKTUBU
        if first_haraka_pair in [(HAMZA, FATHA), (HAMZA, None)]:
            if last_haraka_pair[1] in (None, DAMMA):
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_A_U, previous_ops)
        
        # test for TAKTUBU
        if first_haraka_pair in [(TAA, FATHA), (TAA, None)]:
            if last_haraka_pair[1] in (None, DAMMA):
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_TA_U, previous_ops)
                
        # test for NAKTUBU
        if first_haraka_pair in [(NUUN, FATHA), (NUUN, None)]:
            if last_haraka_pair[1] in (None, DAMMA):
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_NA_U, previous_ops)
                
        # test for YAKTUBUUNA
        if first_haraka_pair in [(YAA, FATHA), (YAA, None)]:
            if last_haraka_pair in [(NUUN, FATHA), (NUUN, None)]:
                if second_last_haraka_pair in [(WAAW, SUKUUN), (WAAW, None)]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text)
                    stripped_word = self._strip_final_haraka_pairs(stripped_word, count=2)
                    append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_YA_UUNA, previous_ops)
                    
        # test for TAKTUBUUNA
        if first_haraka_pair in [(TAA, FATHA), (TAA, None)]:
            if last_haraka_pair in [(NUUN, FATHA), (NUUN, None)]:
                if second_last_haraka_pair in [(WAAW, SUKUUN), (WAAW, None)]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text)
                    stripped_word = self._strip_final_haraka_pairs(stripped_word, count=2)
                    append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_TA_UUNA, previous_ops)
        
        return possible_text_ops
    
    def _get_inner_word_texts_verbs_present_4(self, word_text, previous_ops):
        """
        For verbs of 4 letters (yuf`ilu etc.)
        """
        possible_text_ops = []
        haraka_pairs = get_word_haraka_pairs(word_text)
        if len(haraka_pairs) == 0:
            return []
        first_haraka_pair = haraka_pairs[0]
        if len(haraka_pairs) > 1:
            second_haraka_pair = haraka_pairs[1]
        else: 
            second_haraka_pair = None
        last_haraka_pair = haraka_pairs[-1]
        if len(haraka_pairs) < 2:
            return possible_text_ops
        second_last_haraka_pair = haraka_pairs[-2]
       
        # test for UKTIBU
        if first_haraka_pair in [(HAMZA, DAMMA), (HAMZA, None)]:
            if last_haraka_pair[1] in (None, DAMMA):
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_A_U, previous_ops)
        
        # test for TUKTIBU
        if first_haraka_pair in [(TAA, DAMMA), (TAA, None)]:
            if last_haraka_pair[1] in (None, DAMMA):
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_TA_U, previous_ops)
                
        # test for NUKTIBU
        if first_haraka_pair in [(NUUN, DAMMA), (NUUN, None)]:
            if last_haraka_pair[1] in (None, DAMMA):
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_NA_U, previous_ops)
                
        # test for YUKTIBUUNA
        if first_haraka_pair in [(YAA, DAMMA), (YAA, None)]:
            if last_haraka_pair in [(NUUN, FATHA), (NUUN, None)]:
                if second_last_haraka_pair in [(WAAW, SUKUUN), (WAAW, None)]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text)
                    stripped_word = self._strip_final_haraka_pairs(stripped_word, count=2)
                    append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_YA_UUNA, previous_ops)
                    
        # test for TUKTIBUUNA
        if first_haraka_pair in [(TAA, DAMMA), (TAA, None)]:
            if last_haraka_pair in [(NUUN, FATHA), (NUUN, None)]:
                if second_last_haraka_pair in [(WAAW, SUKUUN), (WAAW, None)]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text)
                    stripped_word = self._strip_final_haraka_pairs(stripped_word, count=2)
                    append_text_op(possible_text_ops, YAA + stripped_word, PRESENT_TA_UUNA, previous_ops)
        
        return possible_text_ops
    
    def _get_inner_word_texts_verbs_majzuum_or_amr(self, word_text, previous_ops):
        possible_text_ops = []
        haraka_pairs = get_word_haraka_pairs(word_text)
        if len(haraka_pairs) == 0:
            return []
        first_haraka_pair = haraka_pairs[0]
        if len(haraka_pairs) > 1:
            second_haraka_pair = haraka_pairs[1]
        else: 
            second_haraka_pair = None
        last_haraka_pair = haraka_pairs[-1]
        if len(haraka_pairs) < 2:
            return possible_text_ops
        second_last_haraka_pair = haraka_pairs[-2]
       
        # test for UKTUB/IFCIL (not AFCIL)
        if first_haraka_pair in [(ALIF, KASRA), (ALIF, DAMMA), (ALIF, None)]:
            if last_haraka_pair[1] in (None, SUKUUN):
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                if stripped_word[-1] == DAMMA:
                    stripped_word[-1] = SUKUUN
                append_text_op(possible_text_ops, YAA + stripped_word, AMR_SINGULAR, previous_ops)
     
        # test for UKTUBUU/IFCILUU (not AFCILUU)
        if first_haraka_pair in [(ALIF, KASRA), (ALIF, DAMMA), (ALIF, None)]:
                if second_last_haraka_pair in [(WAAW, SUKUUN), (WAAW, None)] and \
                        last_haraka_pair in [(ALIF, SUKUUN), (ALIF, None)]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text)
                    stripped_word = self._strip_final_haraka_pairs(stripped_word, count=2)
                    if stripped_word[-1] == DAMMA:
                        stripped_word[-1] = SUKUUN
                    append_text_op(possible_text_ops, YAA + stripped_word, AMR_PLURAL, previous_ops)
     
      # test for TAKTUB
        if first_haraka_pair in [(TAA, FATHA), (TAA, DAMMA), (TAA, None)]:
                if last_haraka_pair[1] in [None, SUKUUN]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text)
                    append_text_op(possible_text_ops, YAA + stripped_word, MAJZUUM_TA_SUKUUN, previous_ops)
     
        # test for TAKTUBUU
        if first_haraka_pair in [(TAA, FATHA), (TAA, DAMMA), (TAA, None)]:
                if second_last_haraka_pair in [(WAAW, SUKUUN), (WAAW, None)] and \
                        last_haraka_pair in [(ALIF, SUKUUN), (ALIF, None)]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text)
                    stripped_word = self._strip_final_haraka_pairs(stripped_word, count=2)
                    if stripped_word[-1] == DAMMA:
                        stripped_word[-1] = SUKUUN
                    append_text_op(possible_text_ops, YAA + stripped_word, MAJZUUM_TA_UU, previous_ops)
                    
      # test for YAKTUB
        if first_haraka_pair in [(YAA, FATHA), (YAA, DAMMA), (YAA, None)]:
                if last_haraka_pair[1] in [None, SUKUUN]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text)
                    append_text_op(possible_text_ops, YAA + stripped_word, MAJZUUM_YA_SUKUUN, previous_ops)
     
        # test for YAKTUBUU
        if first_haraka_pair in [(YAA, FATHA), (YAA, DAMMA), (YAA, None)]:
                if second_last_haraka_pair in [(WAAW, SUKUUN), (WAAW, None)] and \
                        last_haraka_pair in [(ALIF, SUKUUN), (ALIF, None)]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text)
                    stripped_word = self._strip_final_haraka_pairs(stripped_word, count=2)
                    if stripped_word[-1] == DAMMA:
                        stripped_word[-1] = SUKUUN
                    append_text_op(possible_text_ops, YAA + stripped_word, MAJZUUM_YA_UU, previous_ops)
        
        return possible_text_ops
        
    def _get_inner_word_texts_prefixes(self, word_text, previous_ops):
        possible_text_ops = []
        haraka_pairs = get_word_haraka_pairs(word_text)
        if len(haraka_pairs) == 0:
            return []
        first_haraka_pair = haraka_pairs[0]
        if len(haraka_pairs) > 1:
            second_haraka_pair = haraka_pairs[1]
        else: 
            second_haraka_pair = None
        if len(haraka_pairs) > 2:
            third_haraka_pair = haraka_pairs[2]
        else: 
            third_haraka_pair = None
        if len(haraka_pairs) > 3:
            fourth_haraka_pair = haraka_pairs[3]
        else: 
            fourth_haraka_pair = None
        if len(haraka_pairs) > 4:
            fifth_haraka_pair = haraka_pairs[4]
        else: 
            fifth_haraka_pair = None
            
        # test for WA
        if word_text[0] == WAAW:
            if first_haraka_pair in [(WAAW, None), (WAAW, FATHA)]:
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PREFIX_WAAW, previous_ops)
                # recursively call prefix stripper
                possible_text_ops += self._get_inner_word_texts_prefixes(stripped_word, [])
                
        # test for KA
        if word_text[0] == KAAF:
            if first_haraka_pair in [(KAAF, None), (KAAF, FATHA)]:
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PREFIX_KAAF, previous_ops)
                # recursively call prefix stripper
                possible_text_ops += self._get_inner_word_texts_prefixes(stripped_word, [])
            
        # test for AL and AL + shadda on following letter
        if first_haraka_pair in [(ALIF, None), (ALIF, FATHA)] and second_haraka_pair \
            and second_haraka_pair in [(LAAM, None), (LAAM, SUKUUN)]:
                stripped_word = self._strip_initial_haraka_pairs(word_text, 2)
                # remove shadda e.g. تّيسير -> تيسير
                if fourth_haraka_pair and fourth_haraka_pair[0] == SHADDA:
                    stripped_word = self._remove_first_shadda(stripped_word)
                append_text_op(possible_text_ops, stripped_word, PREFIX_AL, previous_ops)
                
        # test for LI
        if word_text[0] == LAAM:
            if first_haraka_pair in [(LAAM, KASRA), (LAAM, None)]:
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PREFIX_LI, previous_ops)
                # test for LIL
                if second_haraka_pair \
                           and second_haraka_pair in [(LAAM, None), (LAAM, SUKUUN)]:
                    stripped_word = self._strip_initial_haraka_pairs(word_text, 2)
                    append_text_op(possible_text_ops, stripped_word, PREFIX_LIL, previous_ops)
                    
        # test for BI
        if word_text[0] == BAA:
            if first_haraka_pair in [(BAA, KASRA), (BAA, None)]:
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PREFIX_BI, previous_ops)
                # test for BIL
                if second_haraka_pair \
                               and second_haraka_pair in [(ALIF, None), (ALIF, SUKUUN)]:
                    if third_haraka_pair \
                               and third_haraka_pair in [(LAAM, None), (LAAM, SUKUUN)]:
                        stripped_word = self._strip_initial_haraka_pairs(word_text, 3)
                        if fifth_haraka_pair and fifth_haraka_pair[0] == SHADDA:
                            stripped_word = self._remove_first_shadda(stripped_word)
                        append_text_op(possible_text_ops, stripped_word, PREFIX_BIL, previous_ops)
                        
        # test for FA
        if word_text[0] == FAA:
            if first_haraka_pair in [(FAA, FATHA), (FAA, None)]:
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PREFIX_FA, previous_ops)
                
        # test for SA
        if word_text[0] == SIIN:
            if first_haraka_pair in [(SIIN, FATHA), (SIIN, None)]:
                stripped_word = self._strip_initial_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, PREFIX_SA, previous_ops)
        
        return possible_text_ops
    
    def _get_inner_word_texts_suffixes(self, word_text, previous_ops):
        possible_text_ops = []
        haraka_pairs = get_word_haraka_pairs(word_text)
        if len(haraka_pairs) == 0:
            return []
        last_haraka_pair = haraka_pairs[-1]
        if len(haraka_pairs) > 1:
            second_last_haraka_pair = haraka_pairs[-2]
        else:
            second_last_haraka_pair = None
        if len(haraka_pairs) > 2:
            third_last_haraka_pair = haraka_pairs[-3]
        else:
            third_last_haraka_pair = None
            
        # test for trailing KASRA (سَكتَتِ الأصنَام for instance)
        if last_haraka_pair[1] == KASRA:
            stripped_word = word_text[:-1]
            append_text_op(possible_text_ops, stripped_word, SUFFIX_KASRA, previous_ops)
            possible_text_ops += \
                self._get_inner_word_texts_suffixes(stripped_word, previous_ops)
            
        # test for HU/HI
        if last_haraka_pair in [(HAA, DAMMA), (HAA, None), (HAA, KASRA)]:
            stripped_word = self._strip_final_haraka_pairs(word_text)
            append_text_op(possible_text_ops, stripped_word, SUFFIX_HU, previous_ops)
            self._append_possible_taa_marbuta(possible_text_ops, stripped_word,
                                              previous_ops + [SUFFIX_HU])
        # test for II
        if last_haraka_pair in [(YAA, SUKUUN), (YAA, None)]:
            if second_last_haraka_pair and  second_last_haraka_pair[1] in [KASRA, None]:
                stripped_word = self._strip_final_haraka_pairs(word_text)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_II, previous_ops)
                self._append_possible_taa_marbuta(possible_text_ops, stripped_word,
                                                  previous_ops + [SUFFIX_II])
        # test for NII
        if last_haraka_pair in [(YAA, SUKUUN), (YAA, None)]:
            if second_last_haraka_pair and  second_last_haraka_pair in [(NUUN, KASRA),
                                                                        (NUUN, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_NII, previous_ops)
        # test for KA
        if last_haraka_pair in [(KAAF, FATHA), (KAAF, None)]:
            stripped_word = self._strip_final_haraka_pairs(word_text)
            append_text_op(possible_text_ops, stripped_word, SUFFIX_KA, previous_ops)
            self._append_possible_taa_marbuta(possible_text_ops, stripped_word,
                                              previous_ops + [SUFFIX_KA])
        # test for KI
        if last_haraka_pair in [(KAAF, KASRA), (KAAF, None)]:
            stripped_word = self._strip_final_haraka_pairs(word_text)
            append_text_op(possible_text_ops, stripped_word, SUFFIX_KI, previous_ops)
            self._append_possible_taa_marbuta(possible_text_ops, stripped_word,
                                              previous_ops + [SUFFIX_KI])
        # test for HAA
        if last_haraka_pair in [(ALIF, SUKUUN), (ALIF, None)]:
            if second_last_haraka_pair in [(HAA, FATHA), (HAA, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_HAA, previous_ops)
                self._append_possible_taa_marbuta(possible_text_ops, stripped_word,
                                                  previous_ops + [SUFFIX_HAA])
                
        # test for HUM
        if last_haraka_pair in [(MIIM, SUKUUN), (MIIM, None)]:
            if second_last_haraka_pair in [(HAA, DAMMA), (HAA, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_HUM, previous_ops)
                self._append_possible_taa_marbuta(possible_text_ops, stripped_word,
                                                  previous_ops + [SUFFIX_HUM])
        # test for KUM
        if last_haraka_pair in [(MIIM, SUKUUN), (MIIM, None)]:
            if second_last_haraka_pair in [(KAAF, DAMMA), (KAAF, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_HUM, previous_ops)
                self._append_possible_taa_marbuta(possible_text_ops, stripped_word,
                                                  previous_ops + [SUFFIX_HUM])
                
        # test for UUNA(sound plural)
        if last_haraka_pair in [(NUUN, None), (NUUN, FATHA)]:
            if second_last_haraka_pair in [(WAAW, SUKUUN), (WAAW, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_UUNA, previous_ops)
                
        # test for IINA(sound plural)
        if last_haraka_pair in [(NUUN, None), (NUUN, FATHA)]:
            if second_last_haraka_pair in [(YAA, SUKUUN), (YAA, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_IINA, previous_ops)
                
        # test for AANI(dual)
        if last_haraka_pair in [(NUUN, None), (NUUN, KASRA)]:
            if second_last_haraka_pair in [(ALIF, SUKUUN), (ALIF, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_AANI, previous_ops)
                self._append_possible_taa_marbuta(possible_text_ops, stripped_word,
                                              previous_ops + [SUFFIX_AANI])
                
        # test for AYNI(dual)
        if last_haraka_pair in [(NUUN, None), (NUUN, KASRA)]:
            if second_last_haraka_pair in [(YAA, SUKUUN), (YAA, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_AYNI, previous_ops)
                self._append_possible_taa_marbuta(possible_text_ops, stripped_word,
                                              previous_ops + [SUFFIX_AYNI])
                
        # test for TAA_MARBUTA ending
        if last_haraka_pair[0] == TAA_MARBUTA:
            stripped_word = self._strip_final_haraka_pairs(word_text)
            append_text_op(possible_text_ops, stripped_word, SUFFIX_TAA_MARBUTA, previous_ops)
                
        # test for AAT ending
        if last_haraka_pair[0] == TAA:
            if second_last_haraka_pair in [(ALIF, FATHA), (ALIF, None)]:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_AAT, previous_ops)
                # also include taa-marbuta ending version
                stripped_word += TAA_MARBUTA
                append_text_op(possible_text_ops, stripped_word, SUFFIX_AAT, previous_ops)
                
        # test for AN ending
        if last_haraka_pair in [(ALIF, None), (ALIF, FATHATAAN)]:
            stripped_word = self._strip_final_haraka_pairs(word_text)
            append_text_op(possible_text_ops, stripped_word, SUFFIX_AN, previous_ops)
            
        # test for IYA
        if last_haraka_pair[0] == TAA_MARBUTA:
            if second_last_haraka_pair and second_last_haraka_pair[0] == YAA:
                stripped_word = self._strip_final_haraka_pairs(word_text, count=2)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_IYA, previous_ops)
            elif (second_last_haraka_pair and second_last_haraka_pair[0] == SHADDA and 
            third_last_haraka_pair in [(YAA, SUKUUN), (YAA, None)]):
                stripped_word = self._strip_final_haraka_pairs(word_text, count=3)
                append_text_op(possible_text_ops, stripped_word, SUFFIX_IYA, previous_ops)

        return possible_text_ops
   
    def _append_possible_taa_marbuta(self, possible_text_ops, stripped_word,
                                          previous_ops):
        # check for TAA -> TAA MARBUTA
        # if stripped word ends in TAA then add TAA_MARBUTA alternative
        pairs = get_word_haraka_pairs(stripped_word)
        if len(pairs) == 0:
            return
        last_pair = pairs[-1]
        if last_pair == (TAA, SUKUUN):
            taa_marbuta_ending_version = stripped_word[:-2] + TAA_MARBUTA
            append_text_op(possible_text_ops, taa_marbuta_ending_version,
                           SWITCH_TAA_MARBUTA, previous_ops)
        elif last_pair == (TAA, None):
            taa_marbuta_ending_version = stripped_word[:-1] + TAA_MARBUTA
            append_text_op(possible_text_ops, taa_marbuta_ending_version,
                           SWITCH_TAA_MARBUTA, previous_ops)
    
    def _strip_final_haraka_pairs(self, word_text, count=1):
        count -= 1
        last_haraka_pair = get_word_haraka_pairs(word_text)[-1]
        if last_haraka_pair[1] is None:
            word_text = word_text[:-1]
        else:
            word_text = word_text[:-2]
        if count == 0:
            return word_text
        else:
            return self._strip_final_haraka_pairs(word_text, count)
        
    def _strip_initial_haraka_pairs(self, word_text, count=1):
        count -= 1
        first_haraka_pair = get_word_haraka_pairs(word_text)[0]
        if first_haraka_pair[1] is None:
            word_text = word_text[1:]
        else:
            word_text = word_text[2:]
        if count == 0:
            return word_text
        else:
            return self._strip_initial_haraka_pairs(word_text, count)
        
    def _remove_first_shadda(self, word_text):
        shadda_removed = False
        text = ''
        for letter in word_text:
            if letter == SHADDA and not shadda_removed:
                shadda_removed = True
                continue
            else:
                text += letter
        return text
    

    
    
            
        