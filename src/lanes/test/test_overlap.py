
import unittest

from find_thirds import overlaps_y

class TestOverlap(unittest.TestCase):
    
    def test_overlap(self):
        
        class CC(object):
        
            def __init__(self, offset_x, ncols, offset_y, nrows):
                self.offset_x = offset_x
                self.offset_y = offset_y
                self.ncols = ncols
                self.nrows = nrows
                
                
        a = CC(0, 10, 20, 10)
        b = CC(0, 10, 25, 6)
        
        self.assert_(overlaps_y(a, b))
        
        b = CC(0, 10, 11, 1)
        self.assertFalse(overlaps_y(a, b))
        
        b = CC(0, 10, 18, 2)
        self.assert_(overlaps_y(a, b))
        
        b = CC(0, 10, 18, 1)
        self.assertFalse(overlaps_y(a, b))
        
        b = CC(0, 10, 21, 2)
        self.assert_(overlaps_y(a, b))
        self.assert_(overlaps_y(b, a))
        
        b = CC(0, 10, 30, 2)
        self.assert_(overlaps_y(a, b))
        
        b = CC(0, 10, 31, 1)
        self.assertFalse(overlaps_y(a, b))
        
        b = CC(100, 10, 30, 2)
        self.assert_(overlaps_y(a, b))
        
        b = CC(0, 10, 20, 10)
        self.assert_(overlaps_y(a, b))
                
                