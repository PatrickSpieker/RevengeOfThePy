import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
import csv
from datetime import date

issn_patt = re.compile("\d{4}-\d{3}[\dxX]")

f = urllib.urlopen("http://olabout.wiley.com/WileyCDA/Section/id-828038.html")
soup = BeautifulSoup(f, 'lxml')
selected = soup.find(class_="journal")


def get_child_tag_strings(tag):
    for child in tag.children:
        if not (str(child) == "\n"):
            yield child.string


driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
driver.set_window_size(1120, 550)
driver.get("http://olabout.wiley.com/WileyCDA/Section/id-828038.html")

journal_select = Select(driver.find_element_by_id("journal"))
with open("../data/cleaned/wiley.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["pub_name", "journal_name", "date", "journal_type", "issn", "apc"])
    for journal in get_child_tag_strings(selected):
        try:
            journal_select.select_by_visible_text(journal)
            oa_option_element = driver.find_element_by_id("displayJOAP")

            if (oa_option_element.text == "Fully Open Access") or (oa_option_element.text == "OpenChoice"):
                price = driver.find_element_by_id("displayJAPC")
                cleaned_price = price.text.replace(",", "").replace("$", "")
                link_with_issn = driver.find_element_by_xpath("//div[@id='displayJAPCL']/a[1]")
                issn_matches = issn_patt.findall(link_with_issn.get_attribute("href"))
                if oa_option_element.text == "Fully Open Access":
                    journal_type = "OA"
                else:
                    journal_type = "Hybrid"

                if issn_matches:
                    row = ["Wiley", journal, str(date.today()), journal_type, issn_matches[0], cleaned_price]
                    print row
                    writer.writerow(row)
                else:
                    print "Error: " + journal + "\n\t" + oa_option_element.text
        except BaseException as e:
            print e
