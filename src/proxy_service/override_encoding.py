
import re
import logging

l = logging.getLogger(__name__)

ENCODING_OVERRIDES = [
                      ('.*aljazeera.net.*', 'utf-8'),
                      ('.*al-islam.com.*', 'windows-1256'),
                     #  ('.*al-islam.com.*', 'utf-8'),
                      ]

COMPILED_ENCODING_OVERRIDES = []

def _compile_overrides():
    for pattern, encoding in ENCODING_OVERRIDES:
        comp = re.compile(pattern)
        COMPILED_ENCODING_OVERRIDES.append((comp, encoding))
_compile_overrides()

def get_override_encoding(url):
    encoding = None
    for url_pattern, test_encoding in COMPILED_ENCODING_OVERRIDES:
        if url_pattern.match(url):
            encoding = test_encoding
    l.debug('override encoding is %s', encoding)
    return encoding