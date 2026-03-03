from main3 import *
from frmsearchsub import *
from sqlite import *
from utils import *
import printlayout
import os 
from constants import *

cnx = connect("vocab.db")
cur = cnx.cursor()

optionLabelLanguage = OPTION_LABELARABIC

        
# stop their contents being auto-deleted by the garbage collector
saveLBItems = {} 
saveLVItems = []

class MainEntrySub(MainEntry):
    def __init__(self, *args):
        MainEntry.__init__(self, *args)
        self.kalimaInitialise()
        self.kalimaSortOrder = "kalima_id"
        self.revisionMode = REVISION_SHOWBOTH
        self.rbShowBoth.setChecked(1)
        self.kalimaGetIndexList()
        self.kalimaShowCurrent()

        self.initLVSection()

        self.mySearchDialog = frmSearchSub()


        QObject.connect(self.leLayoutKalima1,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima2,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima3,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima4,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima5,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima6,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima7,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima8,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima9,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima10,PYSIGNAL("startdrag"),self.startLayoutDrag)
        QObject.connect(self.leLayoutKalima1,PYSIGNAL("enddrag"),self.endLayoutDrag)
        QObject.connect(self.leLayoutKalima2,PYSIGNAL("enddrag"),self.endLayoutDrag)
        QObject.connect(self.leLayoutKalima3,PYSIGNAL("enddrag"),self.endLayoutDrag)
        QObject.connect(self.leLayoutKalima4,PYSIGNAL("enddrag"),self.endLayoutDrag)
        QObject.connect(self.leLayoutKalima5,PYSIGNAL("enddrag"),self.endLayoutDrag)
        QObject.connect(self.leLayoutKalima6,PYSIGNAL("enddrag"),self.endLayoutDrag)
        QObject.connect(self.leLayoutKalima7,PYSIGNAL("enddrag"),self.endLayoutDrag)
        QObject.connect(self.leLayoutKalima8,PYSIGNAL("enddrag"),self.endLayoutDrag)
        QObject.connect(self.leLayoutKalima9,PYSIGNAL("enddrag"),self.endLayoutDrag)
        QObject.connect(self.leLayoutKalima10,PYSIGNAL("enddrag"),self.endLayoutDrag)
        #self.lbSectionWords.setAlignment(0)

        if optionLabelLanguage == OPTION_LABELARABIC:
            self.lblIsmS.setText(u'\u0627\u0633\u0645 (\u0645)' + ':')
            self.lblIsmP.setText(u'\u0627\u0633\u0645 (\u062c)' + ':')
            self.lblFilMa.setText(u'\u0645\u0627\u0636' + ':')
            self.lblFilMu.setText(u'\u0645\u0636\u0627\u0631\u0639' + ':')
            self.lblHarf.setText(u'\u062d\u0631\u0641' + ':')
            self.lblMasdar.setText(u'\u0645\u0635\u062f\u0631' + ':')
            self.lblId.setText(u'\u0631\u0642\u0645' + ':')
            self.lblMeaning.setText(u'\u0645\u0639\u0646\u0649' + ':')
            self.lblExample.setText(u'\u0645\u062b\u0627\u0644' + ':')
            self.lblJidhr.setText(u'\u062c\u0630\u0631' + ':')
            self.pbReveal.setText(u'\u0627\u0643\u0634\u0641')

    def editFind(self):
        self.kalimaSearch()
        
    def fileSave(self):
        self.kalimaUpdateCurrent()
    def filePrint(self):
        printlayout.printAllSections(NO_QT, PAGE_SIZE_HORIZONTAL, PAGE_SIZE_VERTICAL)

        os.system('gv psout.ps')
    def goToKalima(self,index):
        self.kalimaUpdateCurrent()
        self.kalimaIndex = index
        self.kalimaShowCurrent()
        
    def kalimaFirst(self):
        self.goToKalima(0)
        
    def kalimaLast(self):
        self.goToKalima(self.kalimaIndexListMax)
        
    def kalimaInitialise(self):
        self.kalimaIndex = 0
        
    def kalimaNext(self):
        if self.kalimaIndex < self.kalimaIndexListMax:
            self.goToKalima(self.kalimaIndex + 1)
            
    def kalimaPrevious(self):
        if self.kalimaIndex > 0:
            self.goToKalima(self.kalimaIndex - 1)
            
    def kalimaGetCurrent(self):
        sql = """select kalima_id, kalima_ism_s,
        kalima_ism_p,KALIMA_FIL_MA,
        KALIMA_FIL_MU,  KALIMA_MASDAR,
        KALIMA_HARF,    KALIMA_MEANING,
        KALIMA_EXAMPLE, KALIMA_SORT_KALIMA,
        KALIMA_JIDHR1,  KALIMA_JIDHR2,
        KALIMA_JIDHR3,  KALIMA_JIDHR4,
        KALIMA_JIDHR5
        from kalima where kalima_id = """
        sql += str(self.kalimaIndexList[self.kalimaIndex][0]) + ";"
        cur.execute(sql)
        row = cur.fetchone()
        return row
    
    def kalimaSearch(self):
        """ search for a specific record and go to it"""
        newId = self.mySearchDialog.exec_loop()
        if newId == -1:
            return
        self.goToKalimaId(newId)
        
    def goToKalimaId(self, Id):
        #print repr(self.kalimaIndexList)
        # get index for this id
        for i in range(len(self.kalimaIndexList)):
            if self.kalimaIndexList[i][0] == Id:
                #print Id," found at ",i
                break
        self.goToKalima(i)
        
    def kalimaUpdateCurrent(self):
        myIsmS = encode(self.leIsmS.text())
        myIsmP = encode(self.leIsmP.text())
        myFilMa = encode(self.leFilMa.text())
        myFilMu = encode(self.leFilMu.text())
        myMasdar = encode(self.leMasdar.text())
        myHarf = encode(self.leHarf.text())
        myMeaning = encode(self.leMeaning.text())
        myExample = encode(self.leExample.text())
        myJidhr1 = encode(self.leJidhr1.text())
        myJidhr2 = encode(self.leJidhr2.text())
        myJidhr3 = encode(self.leJidhr3.text())
        myJidhr4 = encode(self.leJidhr4.text())
        #myJidhr5 = encode(self.leJidhr5.text())

        # work out sort numbers
        # based on kalima_ism_s OR kalima_fil_ma
        # each letter has a value

        myKalimaSortNumber = 0
        if len(str(self.leIsmS.text()))> 0:
            mySortWord = str(self.leIsmS.text())
        elif len(str(self.leFilMa.text()))> 0:
            mySortWord = str(self.leFilMa.text())
        else:
            mySortWord = str(self.leHarf.text())
        if mySortWord:
            myKalimaSortNumber = alphaSortValWord(mySortWord)
            
        myJidhrSortNumber = 0
        myJidhrSortNumber +=  41 ** 3 * alphaSortVal(self.leJidhr1.text())
        myJidhrSortNumber +=  41 ** 2 * alphaSortVal(self.leJidhr2.text())
        myJidhrSortNumber +=  41 * alphaSortVal(self.leJidhr3.text())
        myJidhrSortNumber +=  alphaSortVal(self.leJidhr4.text())
        sql = "update kalima set "
        sql += " kalima_ism_s = '" + myIsmS + "',"
        sql += " kalima_ism_p = '" + myIsmP + "',"
        sql += " kalima_fil_ma = '" + myFilMa + "',"
        sql += " kalima_fil_mu = '" + myFilMu + "',"
        sql += " kalima_masdar = '" + myMasdar + "',"
        sql += " kalima_harf = '" + myHarf + "',"
        sql += " kalima_meaning = '" + myMeaning + "',"
        sql += " kalima_example = '" + myExample + "',"
        sql += " kalima_jidhr1 = '" + myJidhr1 + "',"
        sql += " kalima_jidhr2 = '" + myJidhr2 + "',"
        sql += " kalima_jidhr3 = '" + myJidhr3 + "',"
        sql += " kalima_jidhr4 = '" + myJidhr4 + "',"
        #sql += " kalima_jidhr5 = '" + myJidhr5 + "',"
        sql += " kalima_sort_kalima = "  + str(myKalimaSortNumber) + " , "
        sql += " kalima_sort_jidhr = "  + str(myJidhrSortNumber) + " "
        sql += " where kalima_id =  " + str(self.leId.text()) + ";"
        cur.execute(sql)
        cnx.commit()
        
    def kalimaShowCurrent(self):
        self.kalimaClearFields()
        self.leJidhr1.setFocus()
        self.displayRevisionMode()
        kal = self.kalimaGetCurrent()
        self.leId.setText(str(kal[0]))
        if kal[1] !=None and kal[1] !='':
            self.leIsmS.setText(decode(kal[1]))
            self.lePubKalima1.setText(decode(kal[1]))
        if kal[2] !=None and kal[2] !='':
            self.leIsmP.setText(decode(kal[2]))
            self.lePubKalima2.setText(decode(kal[2]))
        if kal[3] !=None and kal[3] !='':
            self.leFilMa.setText(decode(kal[3]))
            self.lePubKalima1.setText(decode(kal[3]))
        if kal[4] !=None and kal[4] !='':
            self.leFilMu.setText(decode(kal[4]))
            self.lePubKalima2.setText(decode(kal[4]))
        if kal[5] !=None and kal[5] !='':
            self.leMasdar.setText(decode(kal[5]))
            self.lePubKalima3.setText(decode(kal[5]))
        if kal[6] !=None and kal[6] !='':
            self.leHarf.setText(decode(kal[6]))
            self.lePubKalima1.setText(decode(kal[6]))
        if kal[7] !=None:
            self.leMeaning.setText(decode(kal[7]))
        if kal[8] !=None:
            self.leExample.setText(decode(kal[8]))
        if kal[10] !=None:
            self.leJidhr1.setText(decode(kal[10]))
        if kal[11] !=None:
            self.leJidhr2.setText(decode(kal[11]))
        if kal[12] !=None:
            self.leJidhr3.setText(decode(kal[12]))
        if kal[13] !=None:
            self.leJidhr4.setText(decode(kal[13]))
        #if kal[14] !=None:
        #self.leJidhr5.setText(decode(kal[14]))
        self.kalimaSectionUpdateCurrent()
        
    def cmbOrderBy_activated(self, text):
        self.kalimaGetIndexList()
        self.kalimaFirst()
        
    def kalimaGetIndexList(self):
        self.kalimaGetSortOrder()
        print("Sorting by " + self.kalimaSortOrder)
        sql = "select kalima_id from kalima order by " + self.kalimaSortOrder +  " ;"
        cur.execute(sql)
        self.kalimaIndexList = cur.fetchall()
        self.kalimaIndexListMax = len(self.kalimaIndexList) - 1
        
    def kalimaGetSortOrder(self):
        if str(self.cmbOrderBy.currentText()) == "Id":
            self.kalimaSortOrder = "kalima_id"
        elif str(self.cmbOrderBy.currentText()) == "Kalima":
            self.kalimaSortOrder = "kalima_sort_kalima "
        elif str(self.cmbOrderBy.currentText()) == "Meaning":
            self.kalimaSortOrder = "kalima_meaning"
        else:
            self.kalimaSortOrder = "kalima_sort_jidhr"
            
    def pbAdd_clicked(self):
        self.kalimaUpdateCurrent()
        sql = "select max(kalima_id) from kalima;"
        cur.execute(sql)
        row = cur.fetchone()
        newId = row[0] + 1
        self.kalimaIndexList.append((newId,))
        self.kalimaIndexListMax += 1
        self.kalimaIndex = self.kalimaIndexListMax
        sql = "insert into kalima (kalima_id) "
        sql += "values (" + str(newId) + ");"
        cur.execute(sql)
        cnx.commit()
        self.kalimaShowCurrent()
        
    def kalimaClearFields(self):
        self.leIsmS.setText('')
        self.leIsmP.setText('')
        self.leFilMa.setText('')
        self.leFilMu.setText('')
        self.leHarf.setText('')
        self.leMasdar.setText('')
        self.leMeaning.setText('')
        self.leExample.setText('')
        self.leJidhr1.setText('')
        self.leJidhr2.setText('')
        self.leJidhr3.setText('')
        self.leJidhr4.setText('')
        self.lePubKalima1.setText('')
        self.lePubKalima2.setText('')
        self.lePubKalima3.setText('')
        self.leLayoutKalima1.setText('')
        self.leLayoutKalima2.setText('')
        self.leLayoutKalima3.setText('')
        self.leLayoutKalima4.setText('')
        self.leLayoutKalima5.setText('')
        self.leLayoutKalima6.setText('')
        self.leLayoutKalima7.setText('')
        self.leLayoutKalima8.setText('')
        self.leLayoutKalima9.setText('')
        self.leLayoutKalima10.setText('')

    def pbDelete_clicked(self):
        sql = "delete from kalima where kalima_id = " + str(self.leId.text()) + ";" 
        cur.execute(sql)
        cnx.commit()
        self.kalimaIndexList.pop(self.kalimaIndex)
        self.kalimaIndexListMax -= 1
        if self.kalimaIndex != 0:
            self.kalimaIndex -= 1
        else:
                #no change, leave kalimaIndex at 0
            pass
        self.kalimaShowCurrent()

    def rbReviseArabic_clicked(self):
        self.revisionMode = REVISION_ARABIC
        self.displayRevisionMode()
        
    def rbReviseEnglish_clicked(self):
        self.revisionMode = REVISION_ENGLISH
        self.displayRevisionMode()
        
    def rbShowBoth_clicked(self):
        self.revisionMode = REVISION_SHOWBOTH
        self.displayRevisionMode()
        
    def displayRevisionMode(self):
        if self.revisionMode == REVISION_SHOWBOTH: 
            self.leMeaning.show()
            self.leIsmS.show()
            self.leIsmP.show()
            self.leFilMa.show()
            self.leFilMu.show()
            self.leHarf.show()
            self.leMasdar.show()
            self.leJidhr1.show()
            self.leJidhr2.show()
            self.leJidhr3.show()
            self.leJidhr4.show()
        elif self.revisionMode == REVISION_ARABIC:
            self.leMeaning.hide()
            self.leIsmS.show()
            self.leIsmP.show()
            self.leFilMa.show()
            self.leFilMu.show()
            self.leHarf.show()
            self.leMasdar.show()
            self.leJidhr1.show()
            self.leJidhr2.show()
            self.leJidhr3.show()
            self.leJidhr4.show()
        else:
            self.leMeaning.show()
            self.leIsmS.hide()
            self.leIsmP.hide()
            self.leFilMa.hide()
            self.leFilMu.hide()
            self.leHarf.hide()
            self.leMasdar.hide()
            self.leJidhr1.hide()
            self.leJidhr2.hide()
            self.leJidhr3.hide()
            self.leJidhr4.hide()
            
    def pbReveal_clicked(self):
        temp = self.revisionMode
        self.revisionMode = REVISION_SHOWBOTH
        self.displayRevisionMode()
        self.revisionMode = temp

    def mainClose(self):
        self.close()

    def pbUnicode_clicked(self):
        myUnicodeWord = str(self.leIsmS.text())
        if len(myUnicodeWord) == 0:
            myUnicodeWord = str(self.leFilMa.text())
        if myUnicodeWord:
            print(repr(myUnicodeWord))

    def editUndo(self):
        self.kalimaShowCurrent()


    def initLVSection(self):
        global saveLVItems
        self.sections = {}
        saveLVItems = []
        self.lvSections.setSorting(0,1)
        for i in range(26):
            char = chr(ord('A') + i)
            self.sections[char] = QListViewItem( self.lvSections,char);

        sql  = "SELECT SECTION_NAME FROM SECTION;"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            sectionName = row[0]
            alphaSection = self.sections[sectionName[0:1].upper()]
            saveLVItems.append(QListViewItem(alphaSection, sectionName)) # otherwise it gets deleted and bad things happen - like seg faults
        alphaSection = self.sections['U']
        saveLVItems.append(QListViewItem(alphaSection, 'unallocated')) # otherwise it gets deleted and bad things happen - like seg faults
            

    def pbAddSection_clicked(self):
        sectionName = str(self.leSectionName.text())
        if sectionName == '':
            return
        alphaSection = self.sections[sectionName[0:1].upper()]
        newSection = QListViewItem(alphaSection, sectionName)
        saveLVItems.append(newSection) # otherwise it gets deleted and bad things happen - like seg faults
        alphaSection.setOpen(1)
        sql = 'SELECT MAX(SECTION_ID) FROM SECTION;'
        cur.execute(sql)
        row = cur.fetchone()
        if row[0] == None:
            nextSectionId = 0
        else:
            nextSectionId = row[0] + 1
        sql = "INSERT INTO SECTION (SECTION_ID, SECTION_NAME) VALUES ("
        sql += str(nextSectionId) + ",'" + sectionName + "');"
        cur.execute(sql)
        cnx.commit()

    def getSelectedSectionId(self):
        sectionName = str(self.lvSections.selectedItem().text(0))
        if sectionName == '':
            return
        sql = "SELECT SECTION_ID FROM SECTION WHERE SECTION_NAME = '"
        sql += sectionName + "';"
        cur.execute(sql)
        row = cur.fetchone()
        if row == None:
            print("section id not found")
            return (None, None)
        else:
            return (row[0], sectionName)

    def getSelectedKalimaId(self):
        global saveLBItems
        kalimaName = str(self.lbSectionWords.selectedItem().text())
        if kalimaName == '':
            return None
        return saveLBItems[kalimaName]

    def pbDeleteSection_clicked(self):
        sectionId, sectionName = self.getSelectedSectionId()
        sql = "UPDATE KALIMA SET SECTION_ID = NULL WHERE SECTION_ID = " + str(sectionId) + ";"
        cur.execute(sql)
        cnx.commit()
        sql = "DELETE FROM SECTION WHERE SECTION_ID = "
        sql += str(sectionId) + ";"
        cur.execute(sql)
        cnx.commit()
        item = self.lvSections.selectedItem()
        item.setText(0,str(item.text(0)) + ' (deleted)')
        


    def lvSections_selectionChanged(self, listViewItem):
        sectionId, sectionName = self.getSelectedSectionId()
        self.updateWordList(sectionId)
        self.updateSectionLayout(sectionId, sectionName)

    def clearWordList(self):
        global saveLBItems
        self.lbSectionWords.clear()
        saveLBItems = {}

    def updateWordList(self, sectionId):
        """ show the words in the section in the kalima list box"""
        global saveLBItems
        if sectionId == None:
            print("section id not found in change selection")
            return
        self.clearWordList()
        sql = """select kalima_id, kalima_ism_s,
            kalima_ism_p,KALIMA_FIL_MA,
            KALIMA_FIL_MU,  KALIMA_MASDAR,
            KALIMA_HARF,    KALIMA_MEANING,
            KALIMA_EXAMPLE, KALIMA_SORT_KALIMA,
            KALIMA_JIDHR1,  KALIMA_JIDHR2,
            KALIMA_JIDHR3,  KALIMA_JIDHR4,
            KALIMA_JIDHR5
            from kalima where section_id = """
        sql += str(sectionId) + ";"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            desc = self.getRowDescription(row)
            item = QListBoxText(self.lbSectionWords,desc)
            saveLBItems[desc] = row[0]  # otherwise it gets deleted and bad things happen - like seg faults, also saves id for future

    def getRowDescription(self, row):
        if row[1] !=None and row[1] != '':
            desc = decode(row[1])
        elif row[3] !=None and row[3] != '':
            desc = decode(row[3])
        elif row[6] !=None and row[6] != '':
            desc = decode(row[6])
        else:
            desc = 'no desc'
        return  desc + ' (' + row[7] + ')'

    def pbAddToSection_clicked(self):
        """add the current kalima to the selected section"""
        #print "abc = " + self.lvSections.selectedItem().text(0)
        if str(self.lvSections.selectedItem().text(0)) == "unallocated":
            print("must choose a section other than unallocated first")
            return
        
        sectionId, sectionName = self.getSelectedSectionId()
        sql = "UPDATE KALIMA SET SECTION_ID = " + str(sectionId) + " WHERE KALIMA_ID = " + str(self.leId.text()) + ";"
        cur.execute(sql)
        cnx.commit()
        self.updateWordList(sectionId)

    def pbRemoveFromSection_clicked(self):
        """remove the current selected kalima to the selected section"""
        kalimaId = self.getSelectedKalimaId()
        sql = "UPDATE KALIMA SET SECTION_ID = NULL  WHERE KALIMA_ID = " + str(kalimaId) + ";"
        cur.execute(sql)
        cnx.commit()
        self.updateWordList()
        

    def kalimaSectionUpdateCurrent(self):
        """ go to the section this kalima is in. If there is no section then clear the section details """
        
        sql = """select section_id  
        from kalima where kalima_id = """
        sql += str(self.leId.text()) + ";"
        cur.execute(sql)
        row = cur.fetchone()
        self.goToSection(row[0])

    def goToSection(self, sectionId):
        if sectionId == None:
            # send it the unallocated section
            sectionName = 'unallocated'
            self.clearWordList()
        else:
            sql = """select section_name from section where section_id = """
            sql += str(sectionId) + ";"
            cur.execute(sql)
            row = cur.fetchone()
            sectionName = row[0]
        item = self.lvSections.findItem(sectionName,0)
        self.lvSections.setSelected(item,1)
        self.lvSections.setOpen(item,1)
        self.lvSections.ensureItemVisible(item)

    def updateSectionLayout(self, sectionId, sectionName):
        """ layout words in the section according to their layout sequence number """
        self.layoutKalimaId = [0,0,0,0,0,0,0,0,0,0,0]
        # first update section name
        self.leLayoutSectionName.setText(sectionName)
        if sectionId == None:
            return
        # get maximum layout seq so far for this section (words with no sequence # come after this)
        sql = "select max(kalima_layout_seq) from kalima where section_id = "
        sql += str(sectionId) + ";"
        cur.execute(sql)
        row = cur.fetchone()
        if row[0] != None:
            maxSeq = row[0]
        else:
            maxSeq = 0
        
        sql = """select kalima_id, kalima_ism_s,
            kalima_ism_p,KALIMA_FIL_MA,
            KALIMA_FIL_MU,  KALIMA_MASDAR,
            KALIMA_HARF,    KALIMA_MEANING,
            KALIMA_EXAMPLE, KALIMA_SORT_KALIMA,
            KALIMA_JIDHR1,  KALIMA_JIDHR2,
            KALIMA_JIDHR3,  KALIMA_JIDHR4,
            KALIMA_JIDHR5, KALIMA_LAYOUT_SEQ
            from kalima where section_id = """
        sql += str(sectionId) + ";"
        cur.execute(sql)
        rows = cur.fetchall()
        nextSeqNo = maxSeq + 1
        for row in rows:
            kalimaId = row[0]
            desc = self.getRowDescription(row)
            layoutSeq = row[15]
            if layoutSeq == None:
                layoutSeq = nextSeqNo
                # update in database
                sql = "update kalima set kalima_layout_seq = " + str(layoutSeq) +\
                      " where kalima_id = " + str(kalimaId) + ";"
                cur.execute(sql)
                cnx.commit()
                nextSeqNo += 1

            if layoutSeq == 1:
                self.leLayoutKalima1.setText(desc)
                self.layoutKalimaId[1] = kalimaId
            elif layoutSeq == 2:
                self.leLayoutKalima2.setText(desc)
                self.layoutKalimaId[2] = kalimaId
            elif layoutSeq == 3:
                self.leLayoutKalima3.setText(desc)
                self.layoutKalimaId[3] = kalimaId
            elif layoutSeq == 4:
                self.leLayoutKalima4.setText(desc)
                self.layoutKalimaId[4] = kalimaId
            elif layoutSeq == 5:
                self.leLayoutKalima5.setText(desc)
                self.layoutKalimaId[5] = kalimaId
            elif layoutSeq == 6:
                self.leLayoutKalima6.setText(desc)
                self.layoutKalimaId[6] = kalimaId
            elif layoutSeq == 7:
                self.leLayoutKalima7.setText(desc)
                self.layoutKalimaId[7] = kalimaId
            elif layoutSeq == 8:
                self.leLayoutKalima8.setText(desc)
                self.layoutKalimaId[8] = kalimaId
            elif layoutSeq == 9:
                self.leLayoutKalima9.setText(desc)
                self.layoutKalimaId[9] = kalimaId
            elif layoutSeq == 10:
                self.leLayoutKalima10.setText(desc)
                self.layoutKalimaId[10] = kalimaId

    # drag and drop functionality in section layout
    # these are slots connected to the drag/drop signals of the lineedits
                
    def startLayoutDrag(self,text,name):
        #print "start drag",text,name
        dragObject  = self.child(name)
        dragEvent = QTextDrag(text,dragObject)
        dragEvent.dragCopy()

    def endLayoutDrag(self,e,name):
        #print "start drag",e,name
        dropObject = self.child(name)
        data = QString('')
        QTextDrag.decode(e,data)
        dropObject.setText(data)
        # clear line edit of the source
        fromEditLine = e.source()
        fromEditLine.setText('')

        # update sequence numbers
        # we get layout position from the control name
        toSeqNo = int(name[14:])
        fromEditLineName = fromEditLine.name
        sFromSeqNo = str(fromEditLineName)[14:]
        fromSeqNo = int(sFromSeqNo)
        fromKalimaId = self.layoutKalimaId[fromSeqNo]
        
        sql = "update kalima set kalima_layout_seq = " + str(toSeqNo) +\
              " where kalima_id = " + str(fromKalimaId) + ";"
        cur.execute(sql)
        cnx.commit()

        self.layoutKalimaId[fromSeqNo] = 0
        self.layoutKalimaId[toSeqNo] = fromKalimaId
        
