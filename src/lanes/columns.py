
import os
import math

from constants import *
from gamera.core import *
from utils import overlaps_y, get_y_coord, get_x_coord


def make_columns(image0):

    dilate0 = image0.dilate()
    output0 = dilate0.otsu_threshold(0)
    
    ccs = output0.cc_analysis()
    
    dividers = []
    for c in ccs:
        if c.nrows > 1000:
            dividers.append(c)
            
    dividers.sort(key=get_x_coord)
    print 'dividers', dividers
    
    rgb = image0.to_rgb()
    rotation_angle = get_dividers_rotation_angle(dividers, rgb)
    rotated0 = image0.rotate(-rotation_angle, RGBPixel(255, 255, 255), 1)
    rotated0.save_PNG(os.path.join(TMP_DIR,"out_after_correct_rotate.png"))
    
    image0 = rotated0
    dilate0 = image0.dilate()
    output0 = dilate0.otsu_threshold(0)
    ccs = output0.cc_analysis()
    
    dividers = []
    for c in ccs:
        if c.nrows > 1000:
            dividers.append(c)
            print c.nrows, c.ncols, c.offset_x, c.offset_y
            for x in range(c.ncols):
                for y in range(c.nrows):
                    image0.set(Point(x + c.offset_x, y + c.offset_y), 255)
            
    dividers.sort(key=get_x_coord)
    print 'dividers', dividers
    
    column_images = []
    
    init_col = 0
    for divider in dividers:
        top_left_point = Point(init_col, 0)
        right_col_x = divider.offset_x
        lower_right_point = Point(right_col_x + divider.ncols / 2, image0.nrows - 1)
        print top_left_point, lower_right_point
        column_image = image0.subimage(top_left_point, lower_right_point)
        column_images.append(column_image)
        init_col = right_col_x + divider.ncols / 2
        
    for ix, col_image in enumerate(column_images):
        col_image.save_PNG(os.path.join(TMP_DIR,"out%s.png" % ix))
        
        
def get_dividers_rotation_angle(dividers, rgb):
    angles = []
    for divider in dividers:
        top_row = divider.offset_y
        bottom_row = divider.offset_y + divider.nrows
        top_ten_rows_subimage = divider.subimage(Point(divider.offset_x, top_row),
                                                 Point(divider.offset_x + divider.ncols - 1, top_row + 10))
        rgb.draw_hollow_rect(top_ten_rows_subimage.ul, top_ten_rows_subimage.lr, RGBPixel(255,0,0))
        bottom_ten_rows_subimage = divider.subimage(Point(divider.offset_x, bottom_row - 10),
                                                    Point(divider.offset_x + divider.ncols - 1, bottom_row))
        rgb.draw_hollow_rect(bottom_ten_rows_subimage.ul, bottom_ten_rows_subimage.lr, RGBPixel(255,0,0))
        top_proj_cols = top_ten_rows_subimage.projection_cols()
        bottom_proj_cols = bottom_ten_rows_subimage.projection_cols()
        print top_proj_cols
        print bottom_proj_cols
        print
        avg_xs = []
        for proj in (top_proj_cols, bottom_proj_cols):
            num_pixels = sum(proj)
            weighted = 0
            for ix, num in enumerate(proj):
                weighted += (ix+1) * num
            avg_x = weighted / num_pixels
            print num_pixels, weighted, avg_x
            avg_xs.append(avg_x)
        height_diff = divider.nrows - 10
        x_diff = abs(avg_xs[0] - avg_xs[1])
        print 'diffs', height_diff, x_diff
        tan_theta = x_diff / height_diff
        theta = math.atan2(height_diff, x_diff)
        print 'theta', 90 - (theta * 180.0/ math.pi)
        theta_deg = 90 - (theta * 180.0/ math.pi)
        angles.append(theta_deg)
        
    print 'angles', angles
            
    rgb.save_PNG(os.path.join(TMP_DIR,"out_dividers.png"))
    
    angle = sum(angles) / len(angles)
    return angle
        
        
if __name__ == '__main__':
    init_gamera()
    make_columns()
    