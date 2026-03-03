from frmsearch import *
from sqlite import *
from utils import *

cnx = connect("localhost:vocab")
cur = cnx.cursor()

class frmSearchSub(frmSearch):
    def __init__(self, *args):
        frmSearch.__init__(self, *args)

    def pbCancel_clicked(self):
        self.done(-1)

    def pbOK_clicked(self):
        row = self.tblResults.currentRow()
        kalimaId = int(str(self.tblResults.text(row,0)))
        self.done(kalimaId)

    def tblResults_doubleClicked(self,row,col,button,mousePos):
        kalimaId = int(str(self.tblResults.text(row,0)))
        self.done(kalimaId)

    def pbSearch_clicked(self):
        sqlCondition = ''
        myArabic = encode(self.leArabic.text())
        myMeaning = encode(self.leMeaning.text())
        if myArabic != None and myArabic != '':
            sqlCondition = """ where (kalima_ism_s LIKE '""" + myArabic + """%') \
            or (kalima_ism_p LIKE '""" + myArabic + """%') \
            or (kalima_fil_ma LIKE '""" + myArabic + """%') \
            or (kalima_fil_mu LIKE '""" + myArabic + """%') \
            or (kalima_harf LIKE '""" + myArabic + """%') """
            sqlOrderBy = " kalima_sort_kalima "
        elif myMeaning != None:
            if sqlCondition == '':
                sqlCondition = ' where '
            else:
                sqlCondition += ' and '
            sqlOrderBy = " kalima_meaning "
            
            sqlCondition += " (kalima_meaning LIKE '" + myMeaning + "%') "

        sql = """select kalima_id, kalima_ism_s,
        kalima_ism_p,KALIMA_FIL_MA,
        KALIMA_FIL_MU, KALIMA_HARF, KALIMA_MEANING
        from kalima  """ 
        sql += sqlCondition + 'order by  ' + sqlOrderBy + ";"
        print(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        # clear all rows in results table
        while self.tblResults.numRows() > 0:
            self.tblResults.removeRow(0)
        # add correct number of new rows
        self.tblResults.setNumRows(len(rows))
        # put data into table
        rowNo = 0
        for row in rows:
            self.tblResults.setText(rowNo,0,str(row[0]))
            self.tblResults.setText(rowNo,1,decode(row[1]) + ' ' + decode(row[2]) +\
                                    ' ' + decode(row[3]) + ' ' + decode(row[4]) + ' ' + decode(row[5]))
            self.tblResults.setText(rowNo,2,decode(row[6]))
            rowNo += 1
        
