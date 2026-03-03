
import os

PROJECT_DIR = r'/home/alynch/workspace/lanes_lexicon'
PROJECT_DIR = r"D:\Documents and Settings\alynch\workspace\lanes_lexicon"
TMP_DIR = r'/tmp'
TRAINING_DIR = os.path.join(PROJECT_DIR, 'training', 't2')
PAGES_DIR = os.path.join(PROJECT_DIR, 'pages')
DICTIONARY_FILEPATH = os.path.join(PROJECT_DIR, "dictionaries", "british-english")

CLASSIFIER_FEATURES = ["aspect_ratio","moments","volume64regions","nrows_feature"]
#CLASSIFIER_FEATURES = "all"

WORD_GAP = 6

CHAR_SET_ROMAN = 1
CHAR_SET_ITALIC = 2
CHAR_SET_ARABIC = 3