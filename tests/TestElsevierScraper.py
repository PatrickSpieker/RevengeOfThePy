import unittest

from scrapers.journalscrapers import ElsevierScraper


class TestElsevierScraper(unittest.TestCase):
    def setUp(self):
        self.instance = ElsevierScraper("../data/elsevier/2016-uncleaned.csv")

    def test_strip_chars(self):
        for row in self.instance.get_entries():
            print row
