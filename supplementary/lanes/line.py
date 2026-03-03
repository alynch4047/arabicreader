
from collections import defaultdict

from gamera.core import *
from constants import *
from word import Word
from utils import get_x_coord, get_y_coord, glyph_name


class Line(object):
    
    def __init__(self, min_x, min_y, max_x, max_y, left_cc, right_cc):
        self.offset_x = min_x
        self.offset_y = min_y
        self.ncols = max_x - min_x
        self.nrows = max_y - min_y
        self.left_cc = left_cc
        self.right_cc = right_cc
        self.ccs = [left_cc, right_cc]
        self.chrs = []
        
    def ul(self):
        return FloatPoint(self.offset_x, self.offset_y)
    
    def lr(self):
        return FloatPoint(self.offset_x + self.ncols, self.offset_y + self.nrows)
    
    def __repr__(self):
        return '<Line %s %s %s %s>' % (self.offset_x, self.offset_y, self.ncols, self.nrows)
    
    def break_line_into_words(self):
        words = []
        ccs = self.ccs[:]
        ccs.sort(key=get_x_coord)
        cc = ccs[0]
        word = Word(cc)
        words.append(word)
        current_x = cc.offset_x + cc.ncols
        for cc in ccs[1:]:
            if (cc.offset_x - current_x) > WORD_GAP:
                word = Word(cc)
                words.append(word)
            else:
                word.ccs.append(cc)
                word.ncols = cc.offset_x + cc.ncols - word.offset_x
            current_x = cc.offset_x + cc.ncols
        return words
    
    def parse_line(self):
        self.words = self.break_line_into_words()
        for word in self.words:
            word.calculate_chrs()
        return self.words
    
    def find_baseline(self):
        """
        Find the baseline of the ccs in this line 
        """
        lower_ys = [c.offset_y + c.nrows for c in self.ccs]
        min_y = min(lower_ys)
        lower_ys = [y - min_y for y in lower_ys]
        
        baseline = get_underline_y(lower_ys)
        self.underline_y = min_y + baseline
        

def get_underline_y(ys):
    MULTIPLE = 3
    def nearest_multiple(x):
        if (x % MULTIPLE) > MULTIPLE / 2.0:
            return (int(x / MULTIPLE) + 1) * MULTIPLE
        else:
            return int(x / MULTIPLE) * MULTIPLE
    adjusted_ys = [nearest_multiple(y) for y in ys]
    
    m, count = mode(adjusted_ys)
    
    underline_ys = []
    for ix, y in enumerate(adjusted_ys):
        if y == m:
            underline_ys.append(ys[ix])
            
    return sum(underline_ys) / float(len(underline_ys))
    
def mode(vals):
    count = defaultdict(int)
    for val in vals:
        count[val] += 1
    max_count = max(count.values())
    for val, count in count.items():
        if count == max_count:
            return val, count
    
    
        
        
        