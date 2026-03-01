
import os

import data

QURAN_DATA_DIR = data.__file__
QURAN_DATA_DIR = QURAN_DATA_DIR.replace('\\','/')
QURAN_DATA_DIR = '/'.join(QURAN_DATA_DIR.split('/')[:-1])
QURAN_DATA_LOC = os.path.join(QURAN_DATA_DIR, 'quran.ar.xml')

import data.project_roots_online

PRO_INIT_LOC = data.project_roots_online.__file__
PRO_INIT_LOC = PRO_INIT_LOC.replace('\\','/')
PRO_DIR = '/'.join(PRO_INIT_LOC.split('/')[:-1])
