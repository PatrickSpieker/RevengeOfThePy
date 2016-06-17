import urllib
from bs4 import BeautifulSoup
import itertools
import re
from datetime import date
import csv

# Generating exceptions
pricing_exceptions = {}

f = urllib.urlopen("https://us.sagepub.com/en-us/nam/sage-choice-journal-and-pricing-exceptions")
soup = BeautifulSoup(f, 'lxml')

issn_patt = re.compile("\d{4}-\d{3}[\dxX]")
price_patt = re.compile("\$\d[,|\d*]\d*")

for tag in soup.find_all("tr"):

    contents = tag.find_all("td")[:2]
    print contents
    journal_title = unicode(contents[0].string).encode("utf8")
    price = unicode(contents[1].string.replace("$", "").replace(",", "")).encode("utf8")
    print journal_title + price
    #unicode(journal_title) + unicode(": ") + unicode(price)



    """journal_title = tag.find("a").string.strip()
    results = [i.string for i in tag.find_all("td") if i.string]
    issn_matches = issn_patt.findall(results[0])
    price_matches = price_patt.findall(results[1])
    if price_matches and issn_matches:
        price = price_matches[0].replace(",", "").replace("$", "")
        issn = issn_matches[0]
        row = ["Hindawi", journal_title, str(date.today()), "OA", issn, price]
        print row
        writer.writerow([unicode(s).encode("utf-8") for s in row])"""