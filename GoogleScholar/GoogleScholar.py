from bs4 import BeautifulSoup
import time
from selenium import webdriver

import GoogleScholar.ParsePaper as ParsePaper

def parseProfile(url, set1, papers_to_use):
    browser = webdriver.Firefox()
    browser.get(url)

    try:
        while True:
            element = browser.find_element_by_id("gsc_bpf_more")
            element.click()

            time.sleep(0.5)
            if not element.is_enabled(): break

        papers = browser.find_elements_by_css_selector(".gsc_a_tr")  
        
        for paper in papers:
            if paper.find_element_by_tag_name("a").get_attribute('innerHTML') not in set1:
                p = paper.find_element_by_tag_name("a").get_attribute('innerHTML')

                time.sleep(0.3)
                name = paper.find_element_by_tag_name("a").get_attribute('innerHTML').strip()
                paper.find_element_by_tag_name("a").click()

                window = browser.find_element_by_id('gs_md_cita-d-bdy')

                soup = BeautifulSoup(window.get_attribute("outerHTML"), 'html.parser')
                papers_to_use.append(ParsePaper.parse(soup, name))

                set1.add(p)

                browser.find_element_by_id('gs_md_cita-d-x').click()
            
        browser.quit()
        return (set1, papers_to_use, True)
    
    except Exception as err:
        time.sleep(3)
        print(f'Error occurred: {err}')
        browser.quit()
        return (set1, papers_to_use, False)


#parseProfile("https://scholar.google.com/citations?user=3IqnhE4AAAAJ&hl=en", {}, [])
