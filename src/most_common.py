from Parsers import *
from Query import *
import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'OA_test')

with con:
    cur = con.cursor()
    s = Select("publishers", ["name", "journal"], [("name", "Hindawi")])
    s.execute(cur)
    data = cur.fetchall()
    for i in data:
        print str(i) + "\n"