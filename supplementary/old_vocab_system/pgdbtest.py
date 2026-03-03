from pgdb import *

cnx = connect("localhost:vocab")
print(cnx)
cur = cnx.cursor()
cur.execute("select kalima_id, kalima_ism_s, kalima_ism_p from kalima order by kalima_id desc;")
res = cur.fetchall()
print(res)

