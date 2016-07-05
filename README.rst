
pricesleuth
===========
``pricesleuth`` is a Python library for acquiring data on OpenAccess journals, including article processing
charge (apc) information. It works with a variety of large publishers and also incorporates some smaller,
miscellaneous publishers.

--------------------
Supported Publishers
--------------------

Currently supported
-------------------
- BioMed Central
- Elsevier
- Hindawi

In progress
-----------
- Public Library of Science (PLoS)
- Sage

------------
Installation
------------

pricesleuth (will be) available on PyPI.

``pip install pricesleuth``

-----
Usage
-----
All of the journal scrapers are located in ``pricesleuth.scrapers.journalscrapers``.
A specific journal's scraper object is formatted like ``[ScraperNameHere]Scraper``.

All scraper objects have a ``get_entries`` method, which returns a generator which generates
a Python tuple for each successfully scraped journal from that publisher. The tuple is of the form:

(publisher_name, journal_name, date_of_scraping, journal_type, ISSN_of_journal, article_publishing_cost)

- publisher_name:

- journal_name:

- date_of_scraping:

- journal_type:

- ISSN_of_journal:

- article_publishing cost:

(NOTE: not ALL journals from each publisher are able to be generated. Some suffer from web-formatting issues or other problems
which prevent efficient scraping)