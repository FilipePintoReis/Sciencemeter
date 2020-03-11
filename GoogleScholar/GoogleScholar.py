from bs4 import BeautifulSoup
import time
from selenium import webdriver

import ParsePaper

def parseProfile(url):
    browser = webdriver.Firefox()
    browser.get(url)

    papers_to_use = []
    try:
        while True:
            element = browser.find_element_by_id("gsc_bpf_more")
            element.click()

            time.sleep(1)
            if not element.is_enabled(): break

        papers = browser.find_elements_by_css_selector(".gsc_a_tr")        
        for paper in papers:
            time.sleep(1)
            paper.find_element_by_tag_name("a").click()

            window = browser.find_element_by_id('gs_md_cita-d-bdy')

            soup = BeautifulSoup(window.get_attribute("outerHTML"), 'html.parser')
            papers_to_use.append(ParsePaper.parse(soup))


            browser.find_element_by_id('gs_md_cita-d-x').click()
            
        browser.close()

    except Exception as err:
        time.sleep(3)
        print(f'Error occurred: {err}')
        browser.close()


parseProfile("https://scholar.google.com/citations?user=3IqnhE4AAAAJ&hl=en")
