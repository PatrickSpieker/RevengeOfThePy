from Parsers import *
import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'OA_test')

with con:
    cur = con.cursor()

    p = OAJournalsParser("data/OA_journals.tsv")
    for row in p:
        pub_insert = OAJournalsParser.generate_pub_insert(row)
        journal_insert = OAJournalsParser.generate_journal_insert(row)
        print pub_insert + "\n"
        print journal_insert + "\n\n"

        try:
            cur.execute(pub_insert)
            con.commit()
        except Exception:
            print "Issue row was: " + str(row) +"\n"
            print "Issue query was: " + pub_insert + "\n\n"
            con.rollback()

        try:
            cur.execute(journal_insert)
            con.commit()
        except Exception:
            print "Issue row was: " + str(row) + "\n"
            print "Issue query was: " + journal_insert + "\n\n"
            con.rollback()

