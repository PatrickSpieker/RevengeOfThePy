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


class BaseScraper(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_entries(self):
        pass


class BioMedCentralScraper(BaseScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        yield None


class ElsevierScraper(BaseScraper):
    def __init__(self, csv_filename):
        pass

    def get_entries(self):
        yield None


class ExistingScraper(BaseScraper):
    def __init__(self, csv_filename):
        pass

    def get_entries(self):
        yield None


class HindawiScraper(BaseScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass

class PLOSScraper(BaseScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass

class SageHybridScraper(BaseScraper):
    def __init__(self):
        pass

    def get_entries(self):
        pass


class SpringerHybridScraper(BaseScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass


class SpringerOpenScraper(BaseScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass


class WileyScraper(BaseScraper):
    def __init__(self, http_address):
        pass

    def get_entries(self):
        pass