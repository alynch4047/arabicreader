
ALIGN_LEFT = 0
ALIGN_RIGHT = 1

LATIN_FONT_SIZE = 9
ARABIC_FONT_SIZE = 14

PAGE_SIZE_VERTICAL = 810
PAGE_SIZE_HORIZONTAL = 560
MARGIN_HORIZONTAL = 20
MARGIN_VERTICAL = 30

BOOK_TITLE = "ArabicReader.net Vocabulary Revision"

# new encoding so that (index - 50)  matches with FE70 series of unicode
# we need to offset by 50 so as to avoid special characters like '%' and '(' and ')'
# we do the offset by inserting 50 .notdef into the encoding

encoding = []
for i in range(50):
    encoding.append('/.notdef')


encoding.extend( ['/trademark','/trademark','/onequarter','/OE','/quotedblbase',
                  '/.notdef','/degree','/degree','/mu','/mu',
          '/acute','/acute','/onesuperior','/onesuperior',
          '/threequarters','/threequarters',
          '/Thorn','/Uacute','/uacute','/Aacute','/aacute','/Otilde',
          '/otilde','/Ograve','/ograve','/Ucircumflex','/ucircumflex',
          '/exclamdown','/plusminus','/A','/a','/B',
          '/acircumflex','/Acircumflex','/b','/Adieresis','/adieresis','/T',
          '/ocircumflex','/Ocircumflex','/t','/V',
          '/odieresis','/Odieresis','/v','/J','/ecircumflex','/Ecircumflex',
          '/j','/at','/agrave','/Agrave','/grave','/X','/oslash','/Oslash',
          '/x','/D','/d','/E','/e','/R','/r','/Z',
          '/z','/S','/oacute','/Oacute','/s','/W','/divide','/multiply','/w','/C',
          '/atilde','/Atilde','/c','/dollar','/thorn','/currency',
          '/asciitilde','/Y','/ugrave','/Ugrave','/y','/P','/eth','/Eth','/p','/O',
          '/idieresis','/Idieresis','/o','/G','/ccedilla','/Ccedilla',
          '/g','/F','/ae','/AE','/f','/Q','/ntilde','/Ntilde','/q','/K',
          '/edieresis','/Edieresis','/k','/L','/igrave','/Igrave',
          '/l','/M','/iacute','/Iacute','/m','/N','/icircumflex',
          '/Icircumflex','/n','/H',
          '/egrave','/Egrave','/h','/U','/u','/Aring',
          '/aring','/I','/eacute','/Eacute','/i','/macron',
          '/questiondown','/Yacute','/yacute','/germandbls',
          '/ydieresis','/Udieresis','/udieresis','/.notdef','/.notdef','/asterisk'] )


