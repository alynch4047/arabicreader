from type1 import *

""" map unicode glyphs to baghdad font glyphs """



# set char widths
font = type1font('fonts/BAGHD___.PFB')
font.load()
font.parse()
font.loadAFM("BAGHD___.AFM")

#baghdadCharWidths = font.charWidths


#for code in baghdadEncodeReplace.keys():
    # width of recoded char is set to the width of the char at the original code (>255)
#    if baghdadCharNames[code] in baghdadCharWidths.keys():
#        baghdadCharWidths[baghdadEncodeReplace[code]] = baghdadCharWidths[baghdadCharNames[code]]
