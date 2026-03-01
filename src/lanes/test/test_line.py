

import unittest

from line import get_underline_y, mode


class TestLine(unittest.TestCase):
    
    def test_get_underline_y(self):
        
        ys = [15, 17, 20, 15, 16, 5, 15, 16]
        
        underline_y = get_underline_y(ys)
        self.assertEquals((15+15+15+16+16)/5.0, underline_y)
        
    def test_mode(self):
        ys = [15, 17, 20, 15, 16, 5, 15, 16]
        m, count = mode(ys)
        self.assertEquals(15, m)
        self.assertEquals(3, count)