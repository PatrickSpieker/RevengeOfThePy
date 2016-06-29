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
import urllib
from bs4 import BeautifulSoup
from datetime import date
import re
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
        f = urllib.urlopen(http_address)
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
        raise MissingAttributeException()

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
            g = urllib.urlopen(link + "about")
            about_soup = BeautifulSoup(g, 'lxml')
            try:
                price = BioMedCentralScraper.__get_price(about_soup)
            except MissingAttributeException as e:
                print link
                print "\n\tNo price could be found"
                continue  # skipping to the next entry

            try:
                journal_name = BioMedCentralScraper.__get_journal_name(about_soup)
            except MissingAttributeException as e:
                print link
                print "\n\tNo journal name could be found"
                continue  # skipping to the next entry

            try:
                issn = BioMedCentralScraper.__get_issn(about_soup)
            except MissingAttributeException as e:
                print link
                print "\n\tNo ISSN could be found"
                continue

            yield ("BioMed Central", journal_name, str(date.today()), "OA", issn, price)


class ElsevierScraper(BaseJournalScraper):
    def __init__(self, csv_filename):
        pass

    def get_entries(self):
        yield None


class ExistingScraper(BaseJournalScraper):
    def __init__(self, csv_filename):
        pass

    def get_entries(self):
        yield None


class HindawiScraper(BaseJournalScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass

class PLOSScraper(BaseJournalScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass

class SageHybridScraper(BaseJournalScraper):
    def __init__(self):
        pass

    def get_entries(self):
        pass


class SpringerHybridScraper(BaseJournalScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass


class SpringerOpenScraper(BaseJournalScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass


class WileyScraper(BaseJournalScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass