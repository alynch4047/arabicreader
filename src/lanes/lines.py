
import os

from gamera.core import *

from constants import *
from word import Word
from line import Line
from utils import overlaps_y, get_y_coord, get_x_coord


def find_ccs_borders(ix, image):
        
        binary = image.otsu_threshold(0)
        ccs = binary.cc_analysis()
        character_bodies = []
        for c in ccs:
            if c.nrows > 15:
    #            image.draw_hollow_rect(c.ul, c.lr, RGBPixel(0,0,0))
                character_bodies.append(c)
        
        leftmost_ccs = []   
        rightmost_ccs = []     
        for row_ix in range(0, image.nrows - 1, 10):
            leftmost_cc = None
            leftmost_cc_x = 10000
            rightmost_cc = None
            rightmost_cc_x = 0
            for c in ccs:
                if abs(c.offset_y - row_ix) < 10 and c.nrows > 15:
                    if c.offset_x > rightmost_cc_x:
                        rightmost_cc_x = c.offset_x
                        rightmost_cc = c

                    if c.offset_x < leftmost_cc_x:
                        leftmost_cc_x = c.offset_x
                        leftmost_cc = c
                        
            if rightmost_cc is not None:
                rightmost_ccs.append(rightmost_cc)
            if leftmost_cc is not None:
                leftmost_ccs.append(leftmost_cc)
            
        # remove redundant ccs
        redundant_ccs_l = set([])
        redundant_ccs_r = set([])
        edge_ccs = leftmost_ccs + rightmost_ccs
        for c in edge_ccs:
            for c2 in edge_ccs:
                if c2 is c: continue
                if overlaps_y(c2, c):
                    if c2.offset_x < c.offset_x:
                        redundant_ccs_l.add(c)
                    else:
                        redundant_ccs_l.add(c2)
                    if c2.offset_x > c.offset_x:
                        redundant_ccs_r.add(c)
                    else:
                        redundant_ccs_r.add(c2)
                    
        for c in redundant_ccs_l:
            if c in leftmost_ccs:
                leftmost_ccs.remove(c)
        for c in redundant_ccs_r:
            if c in rightmost_ccs:
                rightmost_ccs.remove(c)
                
        for c in leftmost_ccs + rightmost_ccs:
            image.draw_hollow_rect(c.ul, c.lr, RGBPixel(0,0,0))
                
        image.save_PNG(os.path.join(TMP_DIR,"out_rect%s.png" % ix))
        
        return character_bodies, leftmost_ccs, rightmost_ccs
        
        
def make_lines(image, ix, ccs, leftmost_ccs, rightmost_ccs, rgb):
    for cc in ccs:
        cc.line = None
    lines = []
    min_x = 0
    max_x = image.ncols - 1
    for ccl in leftmost_ccs:
        line = None
        for ccr in rightmost_ccs:
            if overlaps_y(ccl, ccr):
                min_y = min(ccl.offset_y, ccr.offset_y)
                max_y = max(ccl.offset_y + ccl.nrows, ccr.offset_y + ccr.nrows)
                line = Line(min_x, min_y, max_x, max_y, ccl, ccr)
                ccl.line = ccr.line = line
                break
            
        if line is not None:
            for previous_line in lines:
                if previous_line.offset_y == line.offset_y:
                    break
            else:
                lines.append(line)
            
    print('num lines', len(lines))
    print(len(ccs), 'ccs in make lines')
    for cc in ccs:
        for line in lines:
            if (cc not in line.ccs) and overlaps_y(cc, line):
                min_y = min(cc.offset_y, line.offset_y)
                max_y = max(cc.offset_y + cc.nrows, line.offset_y + line.nrows)
                line.offset_y = min_y
                line.nrows = max_y - min_y
                cc.line = line
                line.ccs.append(cc)
    
#    not_in_line = 0        
#    in_line = 0    
#    for cc in ccs:
#        if cc.line is None:
#            not_in_line += 1
#            rgb.draw_filled_rect(cc.ul, cc.lr, RGBPixel(255,0,255))
#        else:
#            in_line += 1
#    print not_in_line, 'ccs not in lines', in_line, 'in lines'
            
    for line in lines:
        rgb.draw_hollow_rect(line.ul(), line.lr(), RGBPixel(0,0,0))
        
    lines.sort(key=get_y_coord)
#    lines = lines[:1]

    return lines


def classify_ccs(lines, rgb):    
    print('load classifier')
    from gamera import knn
    Word.classifier = knn.kNNInteractive([], CLASSIFIER_FEATURES, 0)
    classifier_data_path = os.path.join(TRAINING_DIR, "classifier_glyphs.xml")
    Word.classifier.from_xml_filename(classifier_data_path)
    
    for line in lines:
        words = line.parse_line()
        for word in words:
            rgb.draw_line(FloatPoint(word.offset_x, line.offset_y),
                            FloatPoint(word.offset_x, line.offset_y + line.nrows),
                             RGBPixel(255,0,0))
            rgb.draw_line(FloatPoint(word.offset_x + word.ncols, line.offset_y),
                            FloatPoint(word.offset_x + word.ncols, line.offset_y + line.nrows),
                             RGBPixel(0,255,0))
            rgb.draw_line(FloatPoint(word.offset_x, line.offset_y),
                            FloatPoint(word.offset_x + word.ncols, line.offset_y + line.nrows),
                             RGBPixel(0,0,255))
        print()

    for line in lines:
        for word in line.words:
            print(''.join(word.chrs), end=' ')
        print()
    
