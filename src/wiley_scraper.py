import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re

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

for journal in get_child_tag_strings(selected):
    try:
        journal_select.select_by_visible_text(journal)
        oa_option = driver.find_element_by_id("displayJOAP")
        price = driver.find_element_by_id("displayJAPC")
        link_with_issn = driver.find_element_by_xpath("//div[@id='displayJAPCL']/a[1]")
        issn_matches = issn_patt.findall(link_with_issn.get_attribute("href"))
        if issn_matches:
            print journal + ": " + link_with_issn.get_attribute("href") + "\n\tOA? : " + \
                oa_option.text + "\n\tPrice: " + price.text + "\n\tISSN: " + issn_matches[0]
        else:
            print journal + ": " + link_with_issn.get_attribute("href") + "\n\tOA? : " + \
                oa_option.text + "\n\tPrice: " + price.text + "\n\tISSN: " + "(no valid ISSN found)"
    except BaseException as e:
        print e
"""
price_list = []
issn_list = []



list_item_patt = re.compile("\'\'")
issn_patt = re.compile("\d{4}-\d{3}[\dxX]")

for script in soup.find_all('script'):
    text = script.get_text()
    if "JAPC " in text:
        arr = re.sub('.*\[', '', re.sub('\].*', '', text)).replace("\n", "")
        #print arr
        price_list = arr.split("',")
    elif "JOAPL" in text:
        issn_list = issn_patt.findall(text)
        #for i in link_list:
        #    print i
print len(price_list)
print len(issn_list)"""
"""
Thoughts:
    -use: http://www.wileyopenaccess.com/view/journals.html to associate journal name to ISSN
    then use http://www.wileyopenaccess.com/details/content/12f25e0654f/Publication-Charges.html
    to associate journal name to APC

"""


