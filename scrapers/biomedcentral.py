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
                return str(int(round(float(price_matches[0].replace(",", "").replace("$", "").replace("'", "")))))
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

            yield self.to_unicode_row(["BioMed Central", journal_name, str(date.today()), "OA", issn, str(price)])

