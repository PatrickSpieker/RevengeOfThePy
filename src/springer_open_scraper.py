from bs4 import BeautifulSoup
import urllib
import re

f = urllib.urlopen("http://www.springeropen.com/journals")
soup = BeautifulSoup(f, 'lxml')

price_patt = re.compile("\$\d[,|\d*]\d*")
paid_for_patt = re.compile("do not need to pay")
issn_patt = re.compile("\d{4}-\d{3}[\dxX]")

journal_count = 0
cost_covered_journals = 0
invalid_journals = 0
invalid_issn = 0


for tag in soup.find_all(class_="list-stacked__item"):
    journal_count += 1
    sub_a = tag.find("a")
    link = sub_a["href"]
    result = link
    if "springeropen.com" in link:
        # follow the link += "about"
        g = urllib.urlopen(link + "about")
        about_soup = BeautifulSoup(g, 'lxml')

        hasPrice = False
        # find the content with the pound/dollar/euro
        for about_tag in about_soup.find_all(class_="CmsArticle_body"):
            text = about_tag.get_text()

            for i in price_patt.findall(text):
                hasPrice = True
                result += "\n\tPrice: " + i.strip('$').replace(',', "")
            for i in paid_for_patt.findall(text):
                hasPrice = True
                cost_covered_journals += 1
                result += "\n\tPrice: " + "0 (costs covered)"

        if not hasPrice:
            invalid_journals += 1
            result += "\n\tPrice: (invalid format)"

        hasISSN = False
        for about_tag in about_soup.find_all(class_="SideBox_defList"):
            for i in issn_patt.findall(about_tag.get_text()):
                hasISSN = True
                result += "\n\tISSN: " + i

        if not hasISSN:
            invalid_journals += 1
            result += "\n\tISSN: (invalid format)"
            invalid_issn += 1
    else:
        result += "\n\tNot in valid format (or redirected)"

    print result
print "\nSummary:"
print "Total journals: " + str(journal_count)
print "Journals with costs covered: " + str(cost_covered_journals)
print "Journals with invalid webpage format: " + str(invalid_journals)
print "Invalid ISSNs: " + str(invalid_issn)


