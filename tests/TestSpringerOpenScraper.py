import unittest

from scrapers.journalscrapers import SpringerOpenScraper


class TestSpringerOpenScraper(unittest.TestCase):
    def setUp(self):
        self.instance = SpringerOpenScraper("http://www.springeropen.com/journals")

    def test_strip_chars(self):
        for row in self.instance.get_entries():
            print row