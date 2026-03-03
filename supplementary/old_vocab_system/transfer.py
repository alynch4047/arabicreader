import pgdb
import sqlite


pcnx = pgdb.connect("localhost:vocab")
pcur = pcnx.cursor()

scnx = sqlite.connect("vocab.db")
scur = scnx.cursor()

sql = """select kalima_id, kalima_ism_s,
            kalima_ism_p,KALIMA_FIL_MA,
            KALIMA_FIL_MU,  KALIMA_MASDAR,
            KALIMA_HARF,    KALIMA_MEANING,
            KALIMA_EXAMPLE, KALIMA_SORT_KALIMA,
            KALIMA_JIDHR1,  KALIMA_JIDHR2,
            KALIMA_JIDHR3,  KALIMA_JIDHR4,
            KALIMA_JIDHR5,KALIMA_SORT_KALIMA, KALIMA_SORT_JIDHR, SECTION_ID from kalima;"""

pcur.execute(sql)
rows = pcur.fetchall()
newId = 0
for kal in rows:
        leId = str(kal[0])
        myIsmS= kal[1]
        myIsmP=kal[2]
        myFilMa=kal[3]
        myFilMu=kal[4]
        myMasdar=kal[5]
        myHarf=kal[6]
        myMeaning=kal[7]
        myExample=kal[8]
        myJidhr1=kal[10]
        myJidhr2=kal[11]
        myJidhr3=kal[12]
        myJidhr4=kal[13]
        myJidhr5=kal[14]
    mySortKalima=kal[15]
    mySortJidhr=kal[16]
    mySectionId=kal[17]

    if mySectionId == None:
        mySectionId = 0

        isql = "insert into kalima (kalima_id) "
        isql += "values (" + leId + ");"
        scur.execute(isql)
        scnx.commit()

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
        sql += " kalima_sort_kalima = "  + str(mySortKalima) + " , "
        sql += " kalima_sort_jidhr = "  + str(mySortJidhr) + " ,  "
        sql += " section_id = "  + str(mySectionId) + "   "
        sql += " where kalima_id =  " + leId + ";"
    print(sql)
        scur.execute(sql)
        scnx.commit()
