# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmsearch.ui'
#
# Created: Thu May 6 14:15:29 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


from qt import *
from qttable import QTable


class frmSearch(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("frmSearch")

        f = QFont(self.font())
        f.setFamily("Bitstream Cyberbit")
        f.setPointSize(14)
        self.setFont(f)


        self.leMeaning = QLineEdit(self,"leMeaning")
        self.leMeaning.setGeometry(QRect(254,96,169,30))
        leMeaning_font = QFont(self.leMeaning.font())
        self.leMeaning.setFont(leMeaning_font)

        self.lblArabic = QLabel(self,"lblArabic")
        self.lblArabic.setGeometry(QRect(441,44,98,29))
        lblArabic_font = QFont(self.lblArabic.font())
        self.lblArabic.setFont(lblArabic_font)

        self.lblMeaning = QLabel(self,"lblMeaning")
        self.lblMeaning.setGeometry(QRect(440,97,102,29))
        lblMeaning_font = QFont(self.lblMeaning.font())
        self.lblMeaning.setFont(lblMeaning_font)

        self.pbSearch = QPushButton(self,"pbSearch")
        self.pbSearch.setGeometry(QRect(318,152,116,39))
        pbSearch_font = QFont(self.pbSearch.font())
        self.pbSearch.setFont(pbSearch_font)

        self.pbOK = QPushButton(self,"pbOK")
        self.pbOK.setGeometry(QRect(409,423,116,39))
        pbOK_font = QFont(self.pbOK.font())
        self.pbOK.setFont(pbOK_font)

        self.pbCancel = QPushButton(self,"pbCancel")
        self.pbCancel.setGeometry(QRect(280,423,116,39))
        pbCancel_font = QFont(self.pbCancel.font())
        self.pbCancel.setFont(pbCancel_font)

        self.tblResults = QTable(self,"tblResults")
        self.tblResults.setNumCols(self.tblResults.numCols() + 1)
        self.tblResults.horizontalHeader().setLabel(self.tblResults.numCols() - 1,self.__tr("Id"))
        self.tblResults.setNumCols(self.tblResults.numCols() + 1)
        self.tblResults.horizontalHeader().setLabel(self.tblResults.numCols() - 1,self.__tr("Arabic"))
        self.tblResults.setNumCols(self.tblResults.numCols() + 1)
        self.tblResults.horizontalHeader().setLabel(self.tblResults.numCols() - 1,self.__tr("Meaning"))
        self.tblResults.setGeometry(QRect(15,206,424,199))
        self.tblResults.setNumRows(3)
        self.tblResults.setNumCols(3)

        self.leArabic = QLineEdit(self,"leArabic")
        self.leArabic.setGeometry(QRect(255,43,169,30))
        leArabic_font = QFont(self.leArabic.font())
        self.leArabic.setFont(leArabic_font)

        self.languageChange()

        self.resize(QSize(553,482).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pbSearch,SIGNAL("clicked()"),self.pbSearch_clicked)
        self.connect(self.pbOK,SIGNAL("clicked()"),self.pbOK_clicked)
        self.connect(self.pbCancel,SIGNAL("clicked()"),self.pbCancel_clicked)
        self.connect(self.tblResults,SIGNAL("doubleClicked(int,int,int,const QPoint&)"),self.tblResults_doubleClicked)


    def languageChange(self):
        self.setCaption(self.__tr("Search"))
        self.lblArabic.setText(self.__tr("Arabic Word"))
        self.lblMeaning.setText(self.__tr("Meaning"))
        self.pbSearch.setText(self.__tr("&Search"))
        self.pbOK.setText(self.__tr("&OK"))
        self.pbCancel.setText(self.__tr("&Cancel"))
        self.tblResults.horizontalHeader().setLabel(0,self.__tr("Id"))
        self.tblResults.horizontalHeader().setLabel(1,self.__tr("Arabic"))
        self.tblResults.horizontalHeader().setLabel(2,self.__tr("Meaning"))


    def pbSearch_clicked(self):
        print("frmSearch.pbSearch_clicked(): Not implemented yet")
    def pbOK_clicked(self):
        print("frmSearch.pbOK_clicked(): Not implemented yet")
    def pbCancel_clicked(self):
        print("frmSearch.pbCancel_clicked(): Not implemented yet")
    def tblResults_doubleClicked(self,a0,a1,a2,a3):
        print("frmSearch.tblResults_doubleClicked(int,int,int,const QPoint&): Not implemented yet")
    def __tr(self,s,c = None):
        return qApp.translate("frmSearch",s,c)
