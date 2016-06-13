from Parsers import *
from Query import *
import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'OA_test')

with con:
    cur = con.cursor()
    p = TSVParser("data/OA_journals.tsv")
    while not p.is_empty():
        l = p.readline()

        pub_insert = InsertInto("publishers", l[0:2], ["name", "journal"])
        journal_insert = InsertInto("journals", l[1:],  ["name", "eISSN", "pISSN", "author_price",
                                                         "website", "year", "free"])
        try:
            print "Inserting to publisher..."
            pub_insert.execute(cur)
            con.commit()
        except:
            con.rollback()

        try:
            print "Inserting to journal..."
            journal_insert.execute(cur)
            con.commit()
        except:
            con.rollback()

    con.close()
