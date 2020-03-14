from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver

# import ParsePaper


def parseProfile(url):
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
                browser.close()

    except Exception as err:
        print(len(links))
        print(f'Error occurred: {err}')
        time.sleep(3)
        browser.close()


parseProfile(
    "https://www.authenticus.pt/en/profileOfResearchers/publicationsList/16105?total_results=162&page=1&_=1")
