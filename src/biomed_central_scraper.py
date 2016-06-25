from bs4 import BeautifulSoup
import urllib
import re
import csv
from datetime import date

f = urllib.urlopen("https://www.biomedcentral.com/journals")
soup = BeautifulSoup(f, 'lxml')

price_patt = re.compile("\$\d[,|\d*]\d*")
paid_for_patt = re.compile("do not need to pay")
issn_patt = re.compile("\d{4}-\d{3}[\dxX]")

with open("../data/cleaned/biomedcentral.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["pub_name", "journal_name", "date", "journal_type", "issn", "apc"])
    for tag in soup.find_all(class_="list-stacked__item"):
        link = tag.find("a")["href"]
        print link
        g = urllib.urlopen(link + "about")
        about_soup = BeautifulSoup(g, 'lxml')
        # find the content with the pound/dollar/euro
        price_matches = None
        paid_for_matches = None

        for about_tag in about_soup.find_all(class_="CmsArticle_body"):
            text = about_tag.get_text()
            price_matches = price_patt.findall(text)
            paid_for_matches = paid_for_patt.findall(text)
            if price_matches or paid_for_matches:
                break

        journal_name_tag = about_soup.find(class_="identity__title-link")
        if journal_name_tag:
            journal_name = journal_name_tag.string
            issn_tag = about_soup.find(class_="SideBox_defList")
            if issn_tag:
                issn_matches = issn_patt.findall(issn_tag.get_text())
                if issn_matches:
                    if price_matches:
                        price = price_matches[0].replace(",", "").replace("$", "").replace("'", "")
                    else:
                        price = 0
                    issn = issn_matches[0]
                    row = ["BioMed Central", journal_name, str(date.today()), "OA", issn, price]
                    print row
                    writer.writerow([unicode(s).encode('utf-8') for s in row])

    else:
        print "Not in valid format (or redirected): " + link


