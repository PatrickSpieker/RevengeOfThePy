import urllib
from bs4 import BeautifulSoup
import itertools
import re
from datetime import date
import csv

f = urllib.urlopen("http://www.hindawi.com/apc/")
soup = BeautifulSoup(f, 'lxml')

issn_patt = re.compile("\d{4}-\d{3}[\dxX]")
price_patt = re.compile("\$\d[,|\d*]\d*")

with open("../data/cleaned/hindawi.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["pub_name", "journal_name", "date", "journal_type", "issn", "apc"])
    for tag in itertools.chain(soup.find_all(class_="subscription_table_plus"),
                               soup.find_all(class_="subscription_table_minus")):
        journal_title = tag.find("a").string.strip()
        results = [i.string for i in tag.find_all("td") if i.string]
        issn_matches = issn_patt.findall(results[0])
        price_matches = price_patt.findall(results[1])
        if price_matches and issn_matches:
            price = price_matches[0].replace(",", "").replace("$", "")
            issn = issn_matches[0]
            row = ["Hindawi", journal_title, str(date.today()), "OA", issn, price]
            print row
            writer.writerow([unicode(s).encode("utf-8") for s in row])