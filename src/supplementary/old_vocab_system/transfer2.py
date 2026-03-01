import pgdb
import sqlite


pcnx = pgdb.connect("localhost:vocab")
pcur = pcnx.cursor()

scnx = sqlite.connect("vocab.db")
scur = scnx.cursor()

sql = """select section_id, section_name from section;"""

pcur.execute(sql)
rows = pcur.fetchall()
newId = 0
for kal in rows:
        leId = str(kal[0])
        myName= kal[1]

        isql = "insert into section (section_id, section_name) "
        isql += "values (" + leId + ",'" + myName + "');"
        scur.execute(isql)
        scnx.commit()
