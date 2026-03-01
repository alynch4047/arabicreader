from printer import *
from constants import *
from utils import *
from sqlite import *

cnx = connect("vocab.db")
cur = cnx.cursor()

printBuffer = []

BUFF_ENGLISH = 1
BUFF_ARABIC = 2
BUFF_COMMENT = 3
BUFF_NEWPAGE = 4

def newLine(QT):
    global myPrinter, xpos, ypos
    ypos -= NEWLINE_SPACE
    if ypos < MARGIN_VERTICAL:
        pass
    # we need to do the pagination after production of all the main document
        #newPage(QT)

def newPage(QT):
    global myPrinter, xpos, ypos

    if QT:
        myPrinter.newPage()
    else:
        psOut('showpage\n')
    topOfPage(QT)

def topOfPage(QT):
    global myPrinter, xpos, ypos
    xpos = MARGIN_HORIZONTAL
    ypos = PAGE_SIZE_VERTICAL - MARGIN_VERTICAL

def printAtBuffer(x,y,text,QT, align=ALIGN_LEFT, fontAbbrev='FT'):
    global printBuffer
    # store print details in a tuple
    printBuffer.append([y,BUFF_ENGLISH,x,text,QT,align,fontAbbrev])

def printAtArabicBuffer(x,y,text,QT):
    global printBuffer
    printBuffer.append([y,BUFF_ARABIC,x,text,QT])
    return printAtPSArabic(x,y,text, sizeonly=TRUE)

def printCommentBuffer(comment,y):
    global printBuffer
    printBuffer.append([y,BUFF_COMMENT,comment])

def bufferToPrinter(QT):
    global printBuffer, sectionPageIndex
    # first sort buffer by y co-ordinate, so that we can paginate properly
    # use ripple sort as it is already close to sorted
    rippled=TRUE
    while rippled:
        rippled = FALSE
        for i in range(len(printBuffer)-1):
            if printBuffer[i][0] < printBuffer[i+1][0]:
                temp = printBuffer[i+1][:]
                printBuffer[i+1] = printBuffer[i][:]
                printBuffer[i] = temp[:]
                rippled = TRUE

    debugFile = open('debugout','w')
    for i in range(len(printBuffer)):
        data = printBuffer[i]
        debugFile.write(str(data[0]) + ' ' + repr(data) + '\n')

    # now do the page breaks
    offset = 0
    pageNo = 1
    sectionPageIndex = []
    i = 0
    while i < len(printBuffer):
        data = printBuffer[i]
        origY = data[0]
        data[0] = data[0] + offset
        if data[0] < MARGIN_VERTICAL:
            printBuffer.insert(i,[0, BUFF_NEWPAGE, pageNo])
            i += 1
            offset = PAGE_SIZE_VERTICAL - MARGIN_VERTICAL - origY
            data[0] = PAGE_SIZE_VERTICAL - MARGIN_VERTICAL
            pageNo += 1
        # do section Page Indexing
        if data[1] == BUFF_COMMENT and data[2][0:8] == 'section:':
            sectionPageIndex.append([pageNo,data[2][9:]])
        i += 1
    # final page number

    printBuffer.insert(i,[0, BUFF_NEWPAGE, pageNo])
    
    for i in range(len(printBuffer)):
        data = printBuffer[i]
        debugFile.write(str(data[0]) + ' ' + repr(data) + '\n')
    debugFile.close()
    
    #now send data to printer
    printTitle(QT)
    for i in range(len(printBuffer)):
        data = printBuffer[i]
        if data[1] == BUFF_ENGLISH:
            printAt(data[2],data[0],data[3],data[4],data[5],data[6])
        elif data[1] == BUFF_ARABIC:
            printAtArabic(data[2],data[0],data[3],data[4])
        elif data[1] == BUFF_COMMENT:
            printComment(data[2])
        elif data[1] == BUFF_NEWPAGE:
            printPageNumber(str(data[2]),QT)
            newPage(QT)
            printTitle(QT)

    #print "INDEX:", repr(sectionPageIndex)

    return pageNo

def printTitle(QT):
    printAt(PAGE_SIZE_HORIZONTAL / 2.0 - getStringWidth(BOOK_TITLE,LATIN_FONT_SIZE) / 2.0 , PAGE_SIZE_VERTICAL - 5, BOOK_TITLE, QT)

def sortSectionPageIndex():
    global sectionPageIndex
    rippled=TRUE
    while rippled:
        rippled = FALSE
        for i in range(len(sectionPageIndex)-1):
            if sectionPageIndex[i][1] > sectionPageIndex[i+1][1]:
                temp = sectionPageIndex[i+1][:]
                sectionPageIndex[i+1] = sectionPageIndex[i][:]
                sectionPageIndex[i] = temp[:]
                rippled = TRUE
    
def printSectionPageIndex(QT,pageNo):
    global xpos, ypos, sectionPageIndex
    column = 0 # left hand column
    xpos = MARGIN_HORIZONTAL
    ypos = PAGE_SIZE_VERTICAL - MARGIN_VERTICAL
    printAt(PAGE_SIZE_HORIZONTAL / 2.0,ypos,'Index',QT)
    newLine(QT)
        
    for i in range(len(sectionPageIndex)):
        printIndexEntry(QT,xpos, ypos,sectionPageIndex[i])
        if ypos < MARGIN_VERTICAL:
            if column == 0:
                xpos = PAGE_SIZE_HORIZONTAL / 2.0
                ypos = PAGE_SIZE_VERTICAL - MARGIN_VERTICAL - NEWLINE_SPACE
                column = 1
            else:
                printAt(PAGE_SIZE_HORIZONTAL / 2.0, MARGIN_VERTICAL - 5, pageNo, QT)
                pageNo += 1
                newPage()
                xpos = MARGIN_HORIZONTAL
                ypos = PAGE_SIZE_VERTICAL - MARGIN_VERTICAL
                column = 0
            printPageNumber(pageNo,QT)
    pageNo += 1
    newPage(QT)
    return pageNo

def printPageNumber(pageNo, QT):
    printAt(PAGE_SIZE_HORIZONTAL / 2.0, 15, str(pageNo), QT)

def printIndexEntry(QT,xpos, ypos,indexEntry):
    printAt(xpos,ypos,indexEntry[1],QT)
    printAt(xpos + PAGE_SIZE_HORIZONTAL / 2.0 - MARGIN_HORIZONTAL * 2,ypos,str(indexEntry[0]),QT)
    newLine(QT)

def printAt(x,y,text,QT, align=ALIGN_LEFT, fontAbbrev='FT'):
    global myPainter
    if QT:
        printAtQT(x,y,text,myPainter, align)
    else:
        printAtPS(x,y,text, align, fontAbbrev)
   

def printAtArabic(x,y,text,QT):
    global myPainter
    if QT:
        return printAtQT(x,y,text,myPainter, ALIGN_RIGHT)
    else:
        return printAtPSArabic(x,y,text)


def printAllSections(QT, pageSizeX, pageSizeY):
    global xpos, ypos
    global printBuffer

    printBuffer = []
    
    initialiseRenderer(NO_QT)

    topOfPage(QT)
    
    sectionWidth = 245

    sql = """select distinct section_id from kalima order by section_id ; """
    
    cur = cnx.cursor() # use own cursor here
    cur.execute(sql)
    row = cur.fetchone()
    print "rowcount is ", cur.rowcount

    column = 0 # left hand column (two sections per page)
    
    while row != None:
        print "print section" , row[0]
        if column == 0:
            saveYPos = ypos
            newY = printSectionWords(NO_QT,row[0],MARGIN_HORIZONTAL, ypos, sectionWidth)
            column = 1
        else:
            ypos = saveYPos
            newY2 = printSectionWords(NO_QT,row[0], PAGE_SIZE_HORIZONTAL - sectionWidth, ypos, sectionWidth)
            column = 0
            # set ypos for next section to be lowest of newY and newY2
            if newY < newY2:
                ypos = newY
            else:
                ypos = newY2
            newLine(QT)
            #newLine(QT)
        row = cur.fetchone()
        #print "next row is", row
    # print words with no section
    printSectionWords(NO_QT, None , MARGIN_HORIZONTAL, ypos, sectionWidth * 2)

    lastPageNo = bufferToPrinter(QT)

    sortSectionPageIndex()

    printSectionPageIndex(QT,lastPageNo + 1)
        
    finaliseRenderer(NO_QT)

def printEntry(QT, entryData, x, y, maxX):
    """ print this entry at the location requested (x,y) and return the size of printing space taken """
    arabicWord1 = entryData[1]
    arabicWord2 = entryData[2]
    meaning = entryData[3]
    width1 = printAtArabicBuffer(x + maxX,y,arabicWord1,QT);
    width2 = printAtArabicBuffer(x + maxX - width1 - 10,ypos,arabicWord2,QT);
    printAtBuffer(x,y,meaning,QT)

def printSectionWords(QT, sectionId, x, y, sectionWidth):
    """ print the words for this section in two columns under a section header """
    global xpos, ypos

    xpos = x
    ypos = y
    column = 0 # left hand column

    columnGap = sectionWidth / 10

    if sectionId == None:
        sql = """select kalima_id, kalima_ism_s,
        kalima_ism_p,   KALIMA_FIL_MA,
        KALIMA_FIL_MU,	KALIMA_MASDAR,
        KALIMA_HARF,	KALIMA_MEANING,
        KALIMA_EXAMPLE,	KALIMA_SORT_KALIMA,
        KALIMA_JIDHR1,	KALIMA_JIDHR2,
        KALIMA_JIDHR3,	KALIMA_JIDHR4,
        KALIMA_JIDHR5, 0,'No Section' ,0
        from kalima
        where section_id is null ; """
    else:
        sql = """select kalima_id, kalima_ism_s,
        kalima_ism_p,   KALIMA_FIL_MA,
        KALIMA_FIL_MU,	KALIMA_MASDAR,
        KALIMA_HARF,	KALIMA_MEANING,
        KALIMA_EXAMPLE,	KALIMA_SORT_KALIMA,
        KALIMA_JIDHR1,	KALIMA_JIDHR2,
        KALIMA_JIDHR3,	KALIMA_JIDHR4,
        KALIMA_JIDHR5, kalima.section_id, section_name , kalima_layout_seq
        from kalima left outer join section
        using (section_id) 
        where section.section_id = """ + str(sectionId)   +  """ order by kalima_layout_seq  ; """
    
    cur.execute(sql)
    rows = cur.fetchall()

    if len(rows) > 0:
        sectionName = rows[0][16]
        printCommentBuffer("section: " + sectionName, ypos)
        printAtBuffer(xpos, ypos, sectionName, QT, ALIGN_LEFT, 'FTB')
        ypos -= NEWLINE_SPACE

        # entry locations are offset from sectionName position
        yPosSectionName = ypos
        horizRowNo = 1
        rowNo = 0
        while rowNo < len(rows):
            # get rows in pairs, for each horizontal row in the section
            rowLHC = rows[rowNo] # LHC  = left hand column
            rowLHCSeqNo = rowLHC[17]
            # odd number 1,3,5,7, is in left hand column                
            if rowNo + 1 < len(rows) and rowLHCSeqNo % 2 == 1 and rows[rowNo+1][17] == rowLHCSeqNo + 1:
                # we have left column AND right hand column (odd & even seq no pair)
                rowNo += 1
                rowRHC = rows[rowNo]

                #print the two columns
                entryDataLHC = getEntryData(rowLHC)
                entryDataRHC = getEntryData(rowRHC)
                width = printEntry(QT, entryDataLHC, xpos, ypos, sectionWidth/2.0 - columnGap/2.0)
                width = printEntry(QT, entryDataRHC, xpos + sectionWidth/2.0 + columnGap, ypos,
                                   sectionWidth/2.0 - columnGap/2.0)

            else:
                # we only have one column for this row, so give it the full section width space
                entryDataLRHC = getEntryData(rowLHC)
                width = printEntry(QT, entryDataLRHC, xpos, ypos, sectionWidth + columnGap/2.0)
                    

            newLine(QT)

            rowNo += 1
        
    return ypos



def getEntryData(row):
    id = row[0]
    word1 = decode(row[1]) + decode(row[3]) + decode(row[6]) # one of these should contain an arabic word or phrase
    if row[2] or row[4]:
        word2 = decode(row[2]) + decode(row[4]) # one of these should contain an arabic word or phrase
    else:
        word2 = ''
        
    meaning = row[7]

    return (id, word1, word2, meaning)


if __name__ == "__main__":
    myApp = QApplication(sys.argv)

    printAllSections(NO_QT,PAGE_SIZE_HORIZONTAL, PAGE_SIZE_VERTICAL)

    myApp.quit()
