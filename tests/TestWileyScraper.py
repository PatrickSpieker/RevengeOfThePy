import unittest
from src.JournalScrapers import WileyScraper


class TestWileyScraper(unittest.TestCase):
    def setUp(self):
        self.instance = WileyScraper("http://olabout.wiley.com/WileyCDA/Section/id-828038.html")

    def test_strip_chars(self):
        for row in self.instance.get_entries():
            print row