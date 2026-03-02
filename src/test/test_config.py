
import ar_logging
import unittest

import config

class TestConfig(unittest.TestCase):
    
    def test_pro_data_location(self):
        loc = config.PRO_DIR
        print(loc)