from distutils.core import setup

setup(
    name="PriceSleuth",
    version="0.1.1",
    description="Web Scrapers for OpenAccess journal prices",
    author="Patrick Spieker",
    author_email="pspieker@cs.washington.edu",
    url='https://github.com/PatrickSpieker/pricesleuth',
    packages=["pricesleuth", "pricesleuth.scrapers"],
    package_data={'pricesleuth': ['data/OA_journals.tsv',
                                  'data/elsevier/2016-uncleaned.csv',
                                  'data/2016+Springer+Journals+List.csv']},
    license="MIT",
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Information Analysis',
    )
)
