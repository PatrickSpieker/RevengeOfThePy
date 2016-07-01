import unittest

from scrapers.journalscrapers import ExistingScraper


class TestJournalScraper(unittest.TestCase):
    def setUp(self):
        self.instance = ExistingScraper("../data/OA_journals.tsv")

    def test_strip_chars(self):
        for row in self.instance.get_entries():
            print row
