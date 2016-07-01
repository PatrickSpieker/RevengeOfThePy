import unittest
from src.JournalScrapers import *


class TestGenScraper(unittest.TestCase):

    def setUp(self):
        self.SCRAPERS = [
            BioMedCentralScraper("https://www.biomedcentral.com/journals"),
            ElsevierScraper("../data/elsevier/2016-uncleaned-csv.csv"),
            ExistingScraper("../data/OA_journals.tsv"),
            HindawiScraper("http://www.hindawi.com/apc/"),
            PLOSScraper("https://www.plos.org/publication-fees"),
            SageHybridScraper(""),
            SpringerHybridScraper("../data/springer/2016+Springer+Journals+List.csv"),
            SpringerOpenScraper("http://www.springeropen.com/journals"),
            WileyScraper("http://olabout.wiley.com/WileyCDA/Section/id-828038.html")
        ]

    def test_unicode(self):
        for scraper in self.SCRAPERS:
            for row in scraper.get_entries():
                for item in row:
                    self.assertEquals(type(item), 'unicode')

