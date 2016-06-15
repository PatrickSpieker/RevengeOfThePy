from bs4 import BeautifulSoup
import urllib

f = urllib.urlopen("http://www.springeropen.com/journals")
soup = BeautifulSoup(f, 'lxml')

for tag in soup.find_all(class_="list-stacked__item"):
    sub_a = tag.find("a")
    link = sub_a["href"]
    if "springeropen.com" in link:
        # follow the link += "/about"
        g = urllib.urlopen(link + "/about")
        about_soup = BeautifulSoup(g, 'lxml')
        # find the content with the pound/dollar/euro
        for about_tag in about_soup.find_all(class_="CmsArticle_body"):
            pass



