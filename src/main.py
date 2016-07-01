import csv
import MySQLdb as mdb
from JournalScrapers import *
from contextlib import closing
import logging


def get_t1_insert(row):
    query = "INSERT INTO publishers VALUES ('"
    query += row[0] + "', '" + row[1] + "');"
    return query

def get_t2_insert(row):

    query = "INSERT INTO journal_prices VALUES ('"
    query += row[1] + "', '" + row[2] + "', "
    query += str(row[5]) + ");"
    #print "Price query: " + query
    return query

def get_t3_insert(row):
    query = "INSERT INTO journal_info VALUES ('"
    query += row[1] + "', '" + row[4] + "', '" + row[3] + "');"
    return query

setup_commands = [
    "CREATE DATABASE IF NOT EXISTS OA_journals;",
    "USE OA_journals",
    "DROP TABLE IF EXISTS publishers;",
    "DROP TABLE IF EXISTS journal_prices;",
    "DROP TABLE IF EXISTS journal_info;",
    """CREATE TABLE IF NOT EXISTS journal_info
      (journal_name VARCHAR(200),
       issn VARCHAR(12),
       journal_type VARCHAR(10),
       PRIMARY KEY (journal_name));""",
    """CREATE TABLE IF NOT EXISTS journal_prices
        (journal_name VARCHAR(200),
         issn VARCHAR(12),
         journal_type VARCHAR(10));""",
    """CREATE TABLE IF NOT EXISTS publishers
        (pub_name VARCHAR(200),
         journal_name VARCHAR(200));"""
]

logging.basicConfig(filename="../logs/org_errors.log", filemode="w", level=logging.DEBUG)

with closing(mdb.connect(host='localhost',
                         user='pspieker',
                         passwd='test623')) as con:
    # run setup commands
    for cmd in setup_commands:
        with closing(con.cursor()) as cur:
            cur.execute(cmd)

    scrapers = [
        BioMedCentralScraper("https://www.biomedcentral.com/journals"),
        ElsevierScraper("../data/elsevier/2016-uncleaned-csv.csv"),
        ExistingScraper("../data/OA_journals.tsv"),
        HindawiScraper("http://www.hindawi.com/apc/"),
        PLOSScraper("https://www.plos.org/publication-fees"),
        SageHybridScraper(""),
        SpringerHybridScraper("../data/springer/2016+Springer+Journals+List.csv"),
        SpringerOpenScraper("http://www.springeropen.com/journals"),
        WileyScraper("http://olabout.wiley.com/WileyCDA/Section/id-828038.html")
    ]
    # Table 1:
    # pub_name -> journal_name

    # Table 2:
    # journal_name -> price : date

    # Table 3:
    # journal_name -> issn

    for scraper in scrapers:
        try:
            print str(scraper)
            for row in scraper.get_entries():
                print row[1] + ": " + row[-1]
                logging.info("Error log for %s:" % row[1])
                q1 = get_t1_insert(row)
                q2 = get_t2_insert(row)
                q3 = get_t3_insert(row)
                for query in (q1, q2, q3):
                    with closing(con.cursor()) as cur:
                        try:
                            cur.execute(query)
                            con.commit()
                        except mdb.Error as e:
                            logging.warning("\t" + query + "\n\t" + str(e))
                            con.rollback()
                            continue
                        #print "Success on: " + query
                logging.debug("\n\n")
        except StopIteration:
            print str(scraper) + " is not implemented yet"

