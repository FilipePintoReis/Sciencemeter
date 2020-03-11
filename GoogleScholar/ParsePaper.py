from Paper import Paper
from bs4 import BeautifulSoup

def parse(soup):
    name = soup.find(id = "gsc_vcd_title").contents[0].contents[0]
    total_citations = 0
    publication_date = 'N/a'
    elements = soup.find_all(class_="gs_scl")

    for element in elements:
        if element.contents[0].contents[0] == 'Authors':
            authors = element.contents[1].contents[0].split(',')
        if element.contents[0].contents[0] == 'Publication date':
            publication_date = element.contents[1].contents[0]
        if element.contents[0].contents[0] == 'Total citations':
            total_citations = element.contents[1].contents[0].contents[0].contents[0].split()[2]

    return Paper(name, authors, publication_date, total_citations)




