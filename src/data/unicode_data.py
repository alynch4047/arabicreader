
ALIF =   u'\u0627'
BAA =    u'\u0628'
TAA_MARBUTA =  u'\u0629'
TAA =    u'\u062A'
THAA =   u'\u062B'
JIIM =   u'\u062C'
HAA_ =   u'\u062D'
KHAA =   u'\u062E'
DAAL =   u'\u062F'
DHAAL =  u'\u0630'
RAA =    u'\u0631'
ZAAL =   u'\u0632'
SIIN =   u'\u0633'
SHIIN =  u'\u0634'
SAAD =   u'\u0635'
DAAD =   u'\u0636'
TAA_ =   u'\u0637'
DHAA_ =  u'\u0638'
AYN =    u'\u0639'
GHAYN =  u'\u063A'
FAA =    u'\u0641'
QAAF =   u'\u0642'
KAAF =   u'\u0643'
LAAM =   u'\u0644'
MIIM =   u'\u0645'
NUUN =   u'\u0646'
HAA  =   u'\u0647'
WAAW =   u'\u0648'
ALIF_MAQSURA = u'\u0649'
YAA  =   u'\u064A'
HAMZA =  u'\u0621'

FATHA = u'\u064E'
DAMMA = u'\u064F'
KASRA = u'\u0650'

FATHATAAN = u'\u064B'
DAMMATAAN = u'\u064C'
KASRATAAN = u'\u064D'

SUKUUN = u'\u0652'

SHADDA = u'\u0651'

CORE_LETTERS = [ALIF, BAA, TAA_MARBUTA, TAA, THAA, JIIM, HAA_, KHAA,
                     DAAL, DHAAL, RAA, ZAAL, SIIN, SHIIN, SAAD, DAAD, TAA_, DHAA_,
                     AYN, GHAYN, FAA, QAAF, KAAF, LAAM, MIIM, NUUN,
                     HAA, WAAW, YAA, HAMZA, SHADDA]

CANONICAL_VOWELS = [FATHA, DAMMA, KASRA, FATHATAAN, DAMMATAAN, KASRATAAN, SUKUUN]

HAMZA_1 = u'\uFB50'

ALTERNATIVE_FORMS = {}
ALTERNATIVE_FORMS[HAMZA] = [u'\uFB50', u'\uFB51']
ALTERNATIVE_FORMS[ALIF]  = [u'\uFE81', u'\uFE82']
                     
CORE_FORMS = {}

HAMZA_ABOVE_ALIF = u'\u0623'
HAMZA_ABOVE_WAAW = u'\u0624'
HAMZA_BELOW_ALIF = u'\u0625'
HAMZA_ABOVE_YAA = u'\u0626'
CORE_FORMS[HAMZA] = [HAMZA_ABOVE_ALIF, HAMZA_ABOVE_WAAW, HAMZA_BELOW_ALIF, HAMZA_ABOVE_YAA]
# XXX this is wrong
CORE_FORMS[ALIF]  = [u'\u0622']
CORE_FORMS[YAA] =   [ALIF_MAQSURA]

CANONICAL_LETTERS = CORE_LETTERS + [ALIF_MAQSURA] + \
                    CORE_FORMS[HAMZA] + CORE_FORMS[ALIF] + CORE_FORMS[YAA]

ALTERNATIVE_FORMS_LOOKUP = {}
for canonical_letter in ALTERNATIVE_FORMS:
    for alternative_letter in ALTERNATIVE_FORMS[canonical_letter]:
        if alternative_letter not in ALTERNATIVE_FORMS_LOOKUP:
            ALTERNATIVE_FORMS_LOOKUP[alternative_letter] = canonical_letter
        else:
            raise Exception()
        
CORE_FORMS_LOOKUP = {}
for core_letter in CORE_FORMS:
    for canonical_letter in CORE_FORMS[core_letter]:
        if canonical_letter not in CORE_FORMS_LOOKUP:
            CORE_FORMS_LOOKUP[canonical_letter] = core_letter
        else:
            raise Exception()