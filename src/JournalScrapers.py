"""
class BaseScraper <- the base, abstract class
    init(self)

    get_entries() <- generator function for every entry in the scraper

class BaseWebScraper(BaseScraper): <- abstract base class for the scrapers that pull from Web
    init(self, input_address)

class JournalHTMLScraper(BaseWebScraper)

class JournalCSVScraper(BaseWebScraper)


"""

from abc import ABCMeta, abstractmethod

# imports for class implementation
import urllib2
from bs4 import BeautifulSoup
from datetime import date
import re
import itertools
import csv
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from ScraperExceptions import MissingAttributeException


class BaseScraper:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_entries(self):
        pass


class BaseJournalScraper(BaseScraper):
    __metaclass__ = ABCMeta
    COL_NAMES = ("pub_name", "journal_name", "date", "journal_type", "issn", "apc")
    PRICE_PATT = re.compile("\$\d[,|\d*]\d*")
    ISSN_PATT = re.compile("\d{4}-\d{3}[\dxX]")


class BioMedCentralScraper(BaseJournalScraper):
    paid_for_patt = re.compile("do not need to pay")
    
    def __init__(self, http_address):
        f = urllib2.urlopen(http_address, timeout=5)
        self.soup = BeautifulSoup(f, 'lxml')

    @staticmethod
    def __get_price(soup):
        for tag in soup.find_all(class_="CmsArticle_body"):
            text = tag.get_text()
            price_matches = BioMedCentralScraper.PRICE_PATT.findall(text)
            paid_for_matches = BioMedCentralScraper.paid_for_patt.findall(text)
            if price_matches:
                return price_matches[0].replace(",", "").replace("$", "").replace("'", "")
            elif paid_for_matches:
                return 0
        raise MissingAttributeException

    @staticmethod
    def __get_journal_name(soup):
        journal_name_tag = soup.find(class_="identity__title-link")
        if not journal_name_tag:
            raise MissingAttributeException
        return journal_name_tag.string

    @staticmethod
    def __get_issn(soup):
        issn_tag = soup.find(class_="SideBox_defList")
        if not issn_tag:
            raise MissingAttributeException
        issn_matches = BioMedCentralScraper.ISSN_PATT.findall(issn_tag.get_text())
        if not issn_matches:
            raise MissingAttributeException
        return issn_matches[0]

    def get_entries(self):
        for tag in self.soup.find_all(class_="list-stacked__item"):
            link = tag.find("a")["href"]
            try:
                g = urllib2.urlopen(link + "about", timeout=5)
                about_soup = BeautifulSoup(g, 'lxml')
            except Exception:
                print link + ": Connection problems, continuing to the next entry"
                continue
            try:
                price = BioMedCentralScraper.__get_price(about_soup)
            except MissingAttributeException:
                print link
                print "\n\tNo price could be found"
                continue  # skipping to the next entry

            try:
                journal_name = BioMedCentralScraper.__get_journal_name(about_soup)
            except MissingAttributeException:
                print link
                print "\n\tNo journal name could be found"
                continue  # skipping to the next entry

            try:
                issn = BioMedCentralScraper.__get_issn(about_soup)
            except MissingAttributeException:
                print link
                print "\n\tNo ISSN could be found"
                continue

            yield ("BioMed Central", journal_name, str(date.today()), "OA", issn, price)


class ElsevierScraper(BaseJournalScraper):
    REPLS = {
        "\xca": " ", "\r\xa0": "", "\x96": "n",
        "\x97": "o", "\x87": "a", "\x8b": "a",
        "\x92": "i", "\x8e": "e", "\x8f": "e",
        "\x8d": "c", "\xd5": "'", "\xea": "I",
        " fee not payable by author": ""
    }

    def __init__(self, csv_filepath):
        f = open(csv_filepath, "r")
        self.reader = csv.reader(f)
        next(self.reader)

    @staticmethod
    def __clean_entry(string):
        for repl in ElsevierScraper.REPLS:
            string = string.replace(repl, ElsevierScraper.REPLS[repl])
        return string

    def get_entries(self):
        for row in self.reader:
            row = [ElsevierScraper.__clean_entry(i) for i in row]
            yield ("Elsevier", row[1], str(date.today()),
                    'Hybrid' if row[2] == 'Hybrid' else 'OA',
                    row[0], row[4])


class ExistingScraper(BaseJournalScraper):
    def __init__(self, csv_filepath):
        f = open(csv_filepath, "rU")
        self.reader = csv.reader(f, dialect=csv.excel_tab)
        next(self.reader)

    @staticmethod
    def __get_row(row):
        if not row[2]:
            raise MissingAttributeException
        return (row[0], row[1], row[6],
                "OA" if row[4] else "Hybrid", row[2], row[4])

    def get_entries(self):
        for row in self.reader:
            try:
                yield ExistingScraper.__get_row(row)
            except MissingAttributeException:
                print row
                print "\tThe above row is broken"
                pass


class HindawiScraper(BaseJournalScraper):
    def __init__(self, http_address):
        f = urllib2.urlopen(http_address, timeout=5)
        self.soup = BeautifulSoup(f, 'lxml')

    @staticmethod
    def __get_title(tag):
        return tag.find("a").string.strip()

    @staticmethod
    def __get_price(results):
        price_matches = BaseJournalScraper.PRICE_PATT.findall(results[1])
        if not price_matches:
            raise MissingAttributeException
        return price_matches[0].replace(",", "").replace("$", "")

    @staticmethod
    def __get_issn(results):
        issn_matches = BaseJournalScraper.ISSN_PATT.findall(results[0])
        if not issn_matches:
            raise MissingAttributeException
        return issn_matches[0]

    def get_entries(self):
        for tag in itertools.chain(self.soup.find_all(class_="subscription_table_plus"),
                                   self.soup.find_all(class_="subscription_table_minus")):
            journal_title = HindawiScraper.__get_title(tag)
            results = [i.string for i in tag.find_all("td") if i.string]
            if not results or (len(results) != 2):
                print "ERROR:"
                print "\t" + str(tag.contents)
                continue
            try:
                price = HindawiScraper.__get_price(results)
                issn = HindawiScraper.__get_issn(results)
            except MissingAttributeException:
                print "ERROR:"
                print "\t" + str(tag.contents)
                continue

            yield ["Hindawi", journal_title, str(date.today()), "OA", issn, price]


class PLOSScraper(BaseJournalScraper):
    """
    Scraper isn't actually finished yet. Can't port it
    """
    def __init__(self, http_address):
        pass

    def get_entries(self):
        raise StopIteration


class SageHybridScraper(BaseJournalScraper):
    """
    Scraper isn't actually finished yet. Can't port it
    """
    def __init__(self, http_address):
        pass

    def get_entries(self):
        raise StopIteration


class SpringerHybridScraper(BaseJournalScraper):
    REPLS = {
        "\x9f": "u",
        "\x8a": "a",
        "\x8e": "e",
        "\x8d": "c",
        "\x91": "i",
        "\x87": "a",
        "\x85": "O",
        "\x9a": "o",
        "\xd0": "",
        "\xa7": "B"
    }

    def __init__(self, csv_path):
        f = open(csv_path, "r")
        self.reader = csv.reader(f)
        for i in range(9):
            next(self.reader)

    @staticmethod
    def __clean_name(string):
        for repl in SpringerHybridScraper.REPLS:
            string = string.replace(repl, SpringerHybridScraper.REPLS[repl])
        return string

    def get_entries(self):
        for row in self.reader:
            if row[11] == "Hybrid (Open Choice)":
                yield ("Springer", SpringerHybridScraper.__clean_name(row[1]), str(date.today()),
                       "Hybrid", row[5], 3000)


class SpringerOpenScraper(BaseJournalScraper):
    def __init__(self, http_address):
        f = urllib2.urlopen(http_address, timeout=5)
        self.soup = BeautifulSoup(f, 'lxml')

    @staticmethod
    def __get_price(soup):
        for tag in soup.find_all(class_="CmsArticle_body"):
            text = tag.get_text()
            price_matches = SpringerOpenScraper.PRICE_PATT.findall(text)
            if price_matches:
                return price_matches[0].replace(",", "").replace("$", "").replace("'", "")
        raise MissingAttributeException

    @staticmethod
    def __get_journal_name(soup):
        journal_name_tag = soup.find(id="journalTitle")
        if not journal_name_tag:
            raise MissingAttributeException
        return journal_name_tag.string

    @staticmethod
    def __get_issn(soup):
        issn_tag = soup.find(class_="SideBox_defList")
        if not issn_tag:
            raise MissingAttributeException
        issn_matches = SpringerOpenScraper.ISSN_PATT.findall(issn_tag.get_text())
        if not issn_matches:
            raise MissingAttributeException
        return issn_matches[0]

    def get_entries(self):
        for tag in self.soup.find_all(class_="list-stacked__item"):
            link = tag.find("a")["href"]
            if "springeropen.com" not in link:
                print link + ": Not valid"
                continue

            try:
                g = urllib2.urlopen(link + "about", timeout=5).read()
                about_soup = BeautifulSoup(g, 'lxml')
            except Exception:
                print link + ": Connection problems, continuing to the next entry"
                continue

            try:
                price = SpringerOpenScraper.__get_price(about_soup)
            except MissingAttributeException:
                print link + ": No price could be found"
                continue  # skipping to the next entry

            try:
                journal_name = SpringerOpenScraper.__get_journal_name(about_soup)
            except MissingAttributeException:
                print link + ": No journal name could be found"
                continue  # skipping to the next entry

            try:
                issn = SpringerOpenScraper.__get_issn(about_soup)
            except MissingAttributeException:
                print link + ": No ISSN could be found"
                continue

            yield ["Springer", journal_name, str(date.today()), "OA", issn, price]


class WileyScraper(BaseJournalScraper):
    def __init__(self, http_address):
        f = urllib2.urlopen(http_address)
        self.soup = BeautifulSoup(f, 'lxml')

        self.driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
        self.driver.set_window_size(1120, 550)
        self.driver.get(http_address)

    @staticmethod
    def __get_child_tag_strings(tag):
        for child in tag.children:
            if not (str(child) == "\n"):
                yield child.string

    def __get_issn(self):
        issn_matches = (WileyScraper.ISSN_PATT
                        .findall(self.driver
                                 .find_element_by_xpath("//div[@id='displayJAPCL']/a[1]")
                                 .get_attribute("href")))
        if not issn_matches:
            raise MissingAttributeException
        return issn_matches[0]

    def get_entries(self):
        selected = self.soup.find(class_="journal")
        journal_select = Select(self.driver.find_element_by_id("journal"))

        # getting rid of first "description" row
        journal_gen = WileyScraper.__get_child_tag_strings(selected)
        next(journal_gen)

        for journal in journal_gen:
            try:
                journal_select.select_by_visible_text(journal)
            except NoSuchElementException:
                print "Couldn't find matching journal for input: " + str(journal)
                continue

            oa_option_element = self.driver.find_element_by_id("displayJOAP")

            if (oa_option_element.text == "Fully Open Access") or (oa_option_element.text == "OpenChoice"):
                price = (self.driver.find_element_by_id("displayJAPC")
                             .text.replace(",", "").replace("$", ""))
                try:
                    issn_matches = self.__get_issn()
                except MissingAttributeException:
                    print "Error: " + journal + "\n\t" + oa_option_element.text
                    continue

                journal_type = "OA" if oa_option_element.text == "Fully Open Access" else "Hybrid"

                yield ["Wiley", journal, str(date.today()), journal_type, issn_matches, price]


