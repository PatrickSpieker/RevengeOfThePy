from Parsers import *
from Query import *
import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623','OA_test')

with con:
    cur = con.cursor()
    p = TSVParser("OA_journals.tsv")
    l = p.readline()
    pub = l[0]
    journal = l[1]
    #c = InsertInto("publishers", [pub, journal], ["name", "journal"])
    c = Delete("publishers", "name", "NULL")
    print c.__str__()
    c.execute(cur)


