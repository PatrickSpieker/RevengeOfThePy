import csv
import MySQLdb as mdb


def get_t1_insert(row):
    query = "INSERT INTO publishers VALUES ('"
    query += row[0] + "', '" + row[1] + "');"
    return query

def get_t2_insert(row):
    query = "INSERT INTO journal_prices VALUES ('"
    query += row[1] + "', '" + row[2] + "', "
    query += row[5] + ");"
    return query

def get_t3_insert(row):
    query = "INSERT INTO journal_info VALUES ('"
    query += row[1] + "', '" + row[4] + "', '" + row[3] + "');"
    return query

con = mdb.connect('localhost', 'pspieker', 'spie1004', 'OA_journals')
with con:
    cur = con.cursor()
    paths_to_data = ["../data/cleaned/biomedcentral.csv", "../data/cleaned/elsevier.csv",
                     "../data/cleaned/hindawi.csv", "../data/cleaned/original_converted.csv",
                     "../data/cleaned/springer.csv", "../data/cleaned/wiley.csv"]
    scrapers = [
        BiomedCentralScraper("url"),
        ElsevierScraper(""),
        ExistingScraper(""),
        HindawiScraper(""),
        PLOSScraper(""),
        SageHybridScraper(""),
        SpringerHybridScraper(""),
        SpringerOpenScraper(""),
        WileyScraper("")
    ]
    # Table 1:
    # pub_name -> journal_name

    # Table 2:
    # journal_name -> price : date

    # Table 3:
    # journal_name -> issn

    for scraper in scrapers:
        for row in scraper.get_entries():
            q1 = get_t1_insert(row)
            q2 = get_t2_insert(row)
            q3 = get_t3_insert(row)
            try:
                cur.execute(q1)
                con.commit()
            except Exception as e:
                print "\nError on: " + q1
                print e
                print "\n"
                con.rollback()
            try:
                cur.execute(q2)
                con.commit()
            except Exception as e:
                print "\nError on: " + q2
                print e
                print "\n"
                con.rollback()
            try:
                cur.execute(q3)
                con.commit()
            except Exception as e:
                print "\nError on: " + q3
                print e
                print "\n"
                con.rollback()

