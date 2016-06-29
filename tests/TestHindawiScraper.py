import unittest
from src.JournalScrapers import HindawiScraper

class TestJournalScraper(unittest.TestCase):
    def setUp(self):
        self.instance = HindawiScraper("http://www.hindawi.com/apc/")

    def test_strip_chars(self):
        for row in self.instance.get_entries():
            print row