import os

PROJECT_DIR = '/home/alynch/projects/lanes'
TMP_DIR = '/tmp'
TRAINING_DIR = os.path.join(PROJECT_DIR, 'training', 'l3')
PAGES_DIR = os.path.join(PROJECT_DIR, 'pages')


from gamera.core import *
init_gamera()
image0 = load_image(os.path.join(PAGES_DIR, 'img16.png'))
rgb = image0.to_rgb()
output0 = image0.otsu_threshold(0)

ccs = output0.cc_analysis()
for c in ccs:
    if c.nrows < 12 and c.ncols < 12:
        rgb.highlight(c, RGBPixel(255,0,0))
        c.fill_white()

output0.save_PNG("/tmp/out.png")
rgb.save_PNG("/tmp/rgbout.png")
