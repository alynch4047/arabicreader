
def overlaps_y(c,c2):
    if (c2.offset_y >= c.offset_y) and (c2.offset_y <= (c.offset_y + c.nrows)):
        return True
    if ((c2.offset_y + c2.nrows) >= c.offset_y) and ((c2.offset_y  + c2.nrows) <= (c.offset_y + c.nrows)):
        return True
    if (c.offset_y >= c2.offset_y) and (c.offset_y <= (c2.offset_y + c2.nrows)):
        return True
    if ((c.offset_y + c.nrows) >= c2.offset_y) and ((c.offset_y  + c.nrows) <= (c2.offset_y + c2.nrows)):
        return True
    return False

def get_x_coord(c):
    return c.offset_x

def get_y_coord(c):
    return c.offset_y

def glyph_name(c):
    return c.id_name[0][1].split('.')[-1]

def glyph_long_name(c):
    return c.id_name[0][1]