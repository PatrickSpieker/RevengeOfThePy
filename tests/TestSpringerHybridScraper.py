import unittest
from src.JournalScrapers import SpringerHybridScraper


class TestJournalScraper(unittest.TestCase):
    def setUp(self):
        self.instance = SpringerHybridScraper("../data/springer/2016+Springer+Journals+List.csv")

    def test_strip_chars(self):
        for row in self.instance.get_entries():
            print row