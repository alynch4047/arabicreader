import os

from lines import find_ccs_borders, make_lines, classify_ccs
from columns import make_columns
from constants import *

from gamera.core import *
init_gamera()

#image0 = load_image(os.path.join(PAGES_DIR, 'img16.png'))
#make_columns(image0)

for ix in [0]: #,1,2]:
    image = load_image(os.path.join(TMP_DIR,"out%s.png" % ix))
    character_bodies, leftmost_ccs, rightmost_ccs = find_ccs_borders(ix, image)        
    rgb = image.to_rgb()
    lines = make_lines(image, ix, character_bodies, leftmost_ccs, rightmost_ccs, rgb)
    
    lines = lines[5:6]
    
    rgb.save_PNG(os.path.join(TMP_DIR,"out_lined_%s.png" % ix))
    classify_ccs(lines, rgb)
    rgb.save_PNG(os.path.join(TMP_DIR,"out_words_%s.png" % ix))
    
    for line in lines:
        line.find_baseline()
        rgb.draw_line(FloatPoint(line.offset_x, line.underline_y),
                            FloatPoint(line.offset_x + line.ncols, line.underline_y),
                             RGBPixel(0,0,0))
        
    rgb.save_PNG(os.path.join(TMP_DIR,"out_underlined_%s.png" % ix))

