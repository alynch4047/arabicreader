# utilities for vocab

from constants import *
from baghdad import font

def stripTashkeel(text):
    """ gets a list of tuples providing the tashkeel details,
    and returns the original string with the tashkeel removed"""
    tashkeel = []
    strippedText = ''
    for i in range(len(text)):
        #print "i = ",i
        if ord(text[i]) in TASHKEEL:
            # we have tashkeel
            tashkeel.append((i, text[i]))
            #print "note tashkeel",repr(tashkeel)
        else:
            strippedText += text[i]
            #print "add letter ", repr(text[i])
    return tashkeel, strippedText

def replaceTashkeel(text, tashkeel):
    """ takes a list of tuples detailing tashkeel, and inserts the tashkeel into a string """
    for i in range(len(tashkeel)):
        tashkeelPosition = tashkeel[i][0]
        tashkeelChar = tashkeel[i][1]
        text = text[:tashkeelPosition] + tashkeelChar + text[tashkeelPosition:]
    return text


def stripTashkeelWithLocation(x,y,text):
    """ gets a list of tuples providing the tashkeel details including location of seat letter,
    and returns the original string with the tashkeel removed.
    Note that this string is composed of baghdad code characters and has already been reversed"""

    tashkeel = []

    strippedText = ''
    for i in range(len(text)):
        #print "i = ",i
        if ord(text[i]) in TASHKEEL_BAGHDAD_CODE:
            # we have tashkeel
            tashkeelChar = ord(text[i])
            seatChar = ord(text[i+1]) # i+1 because text has been reversed
            # work out its current location, and correct depending on the seat glyph
            newx = x - getStringWidth(text[i:], ARABIC_FONT_SIZE)
            newy = y
            # adjust position depending on seat character
            if seatChar == (0xfed2 - 0xfe70 + 50): # final faa' 
                #newx = newx + 3
                newy = y - 2.5
            #if seatChar == (0xfe7a - 0xfe70 + 50): # kasra
            #    newy = newy + 2.5
            # look at char size and adjust position of haraka depending on that
            charSize = font.charSize[encoding[seatChar][1:]]
            maxHeight = float(charSize[3])
            minHeight = float(charSize[1])
            width = float(charSize[2]) - float(charSize[0]) 
            averageX = (float(charSize[0]) + float(charSize[2]))/2
            if (tashkeelChar in TASHKEEL_BAGHDAD_CODE_UPPER) and (maxHeight < 450):
                #lower fatha/damma
                newy = newy - (450 - maxHeight) * ARABIC_FONT_SIZE / 1000                
            if (tashkeelChar in TASHKEEL_BAGHDAD_CODE_UPPER) and (maxHeight > 520):
                #raise fatha/damma
                newy = newy + (maxHeight - 520) * ARABIC_FONT_SIZE / 1000                
            if (tashkeelChar in TASHKEEL_BAGHDAD_CODE_LOWER) and (minHeight > -290):
                #raise kasra
                newy = newy + (minHeight + 290) * ARABIC_FONT_SIZE / 1000                
            if (width > 440):
                #shift haraka to the right a bit
                newx = newx + (width - 390) * ARABIC_FONT_SIZE / 1000                
            tashkeel.append((i, text[i], newx, newy))
        else:
            strippedText += text[i]
    return tashkeel, strippedText

def presentationTashkeel(text):
    """ change tashkeel from unicode 0x0600 to presentation form """
    text = text.replace(unichr(0x64b),unichr(0xfe70))
    text = text.replace(unichr(0x64c),unichr(0xfe72))
    text = text.replace(unichr(0x64d),unichr(0xfe74))
    text = text.replace(unichr(0x64e),unichr(0xfe76))
    text = text.replace(unichr(0x64f),unichr(0xfe78))
    text = text.replace(unichr(0x650),unichr(0xfe7a))
    text = text.replace(unichr(0x651),unichr(0xfe7c))
    text = text.replace(unichr(0x652),unichr(0xfe7e))
    return text

def reversePhrase(text):
	ret = ''
	words = text.split()
	for i in range(len(words)):
		j = len(words) - i - 1 # reverse word order too
		word = words[j]
		if ret != '':
			ret += ' '
		ret += reverse(word)
	return ret
		

def reverse(text):
	rev = ''
	for i in range(len(text)):
		rev += text[len(text) - i - 1]
	return rev

def encode(text):
	return unicode(text).encode('UTF-8')

def decode(text):
	return unicode(text,'UTF-8')

def alphaSortValWord(word):
	sortNumber = 0
	word = stripTashkeel(word)[1]
	for i in range(len(word)):
	    sortNumber +=  41 ** (10 - i) * alphaSortVal(word[i])
	return sortNumber


def alphaSortVal(char):
	if len(unicode(char))> 0:
		val = ord(unicode(char))
		if val >= 0x622 and val <= 0x64a:
			if val <= 0x627: # hamza
				return 1
			# exclude tashkiil (0x64B - 0x650) and odd stuff e.g. ufefb and ufef5 laa and laa madd
			return val - 0x621
	return 0

def getStringWidth(text, fontSize):
    """ get widths of each character in the string and return the total width (needs text to be shaped already)"""
    global encoding
    width = 0
    for char in text:
        code = ord(char)
        if code < len(encoding):
            charName = encoding[code][1:]
            if charName not in font.charWidths.keys():
                print charName, "not in widths"
                raise LookupError
            else:
                width += font.charWidths[charName]
        else:
            raise LookupError
    return width * fontSize / 1000.0


if __name__ == '__main__':
	print "?abcdefg?"
	print '?' + reverse("abcdefg") + '?'
	print  '?' + u'\u0020\u0050' + '?'
	print '?' + reverse(u'\u0020\u0050') + '?'
	print "this is a test OK" 
	print '?' + reversePhrase("this is a test OK") + '?'
