from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import urllib

driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
driver.set_window_size(1120, 550)
driver.get("https://www.plos.org/publication-fees")

a = driver.find_elements_by_class_name("feature-block-text")
for i in a:
    print i.text