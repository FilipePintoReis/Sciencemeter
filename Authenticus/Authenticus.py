from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
import requests

from Paper import Paper


def get_paper_links(url):
    browser = webdriver.Firefox()
    browser.get(url)

    try:
        time.sleep(3)
        browser.find_element_by_class_name('cc-dismiss').click()
    except Exception:
        pass

    links = []

    try:
        flag = False
        while True:
            papers = browser.find_elements_by_css_selector(".div-odd")
            for index, paper in enumerate(papers):
                if index != 0:
                    soup = BeautifulSoup(paper.get_attribute(
                        "outerHTML"), 'html.parser')

                    links.append('https://www.authenticus.pt' +
                                 soup.find('a')['href'])

            papers = browser.find_elements_by_css_selector(".div-even")
            for index, paper in enumerate(papers):
                soup = BeautifulSoup(paper.get_attribute(
                    "outerHTML"), 'html.parser')

                links.append('https://www.authenticus.pt' +
                             soup.find('a')['href'])
            # Begining of pagination handling
            pagination = browser.find_element_by_class_name('pagination')
            soup = BeautifulSoup(pagination.get_attribute(
                "outerHTML"), 'html.parser')

            aid = 0
            ul = soup.contents[0].contents
            for i in range(len(ul)):
                if i > 0 and ul[i]['class'] == ["active"]:
                    if ul[i+1]['class'] == ["disabled"]:
                        flag = True
                        break
                    else:
                        aid = ul[i+1].contents[0]['id']
                        break

            time.sleep(1)
            if not flag:
                browser.find_element_by_id(aid).click()
            else:
                break

    except Exception as err:
        print(f'Error occurred: {err}')
        time.sleep(3)
        browser.close()

    browser.close()
    return links


def parse_page(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get title
        title = soup.find(
            class_='content-header').find('h4').contents[0].strip()

        # Get publication date
        meta = soup.find(class_="mainmeta").contents
        while meta.count('\n') > 0:
            meta.remove('\n')

        publication_date = meta[1].find(
            class_="authors-flex").contents[0].strip()

        # Get authors
        authors = []
        authors_html = soup.find(
            class_='authors-flex').find(class_='authors-flex').contents

        for author_html in authors_html:
            if author_html == ' ' or author_html == '\n':
                authors_html.remove(author_html)

        for author_html in authors_html:
            if author_html.contents[0].contents[0].find('<a') == -1:
                authors.append(author_html.contents[0].contents[0])
            else:
                authors.append(author_html.contents[0].contents[0]['title'])

        return Paper(title, authors, publication_date)

    except Exception as err:
        print(f'Error occurred: {err}')


def parse_profile(url):
    links = get_paper_links(url)
    papers = []
    for link in links:
        papers.append(parse_page(link))

    return papers


print(parse_profile("https://www.authenticus.pt/en/profileOfResearchers/publicationsList/16105?total_results=162&page=1&_=1"))
