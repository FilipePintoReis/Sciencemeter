from bs4 import BeautifulSoup
import time
from selenium import webdriver


def get_teachers(institution, initial_url):

    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", '119.81.199.82')
    profile.set_preference("network.proxy.http_port", 8123)
    browser = webdriver.Firefox(firefox_profile=profile)
    browser.get(initial_url)

    f = open(institution + "_teachers_urls.txt", "a")

    time.sleep(150)

    try:
        while True:
            e = browser.find_elements_by_class_name('gs_btnPR')

            elements = browser.find_elements_by_class_name('gsc_1usr')
            for element in elements:
                element = BeautifulSoup(
                    element.get_attribute("outerHTML"), 'html.parser')
                if element.contents[0].contents[0].contents[1].contents[2].contents[0].split()[3] == 'fe.up.pt':
                    f.write('https://scholar.google.com' +
                            element.contents[0].contents[0].contents[1].contents[0].contents[0]['href'] + '\n')

            e[0].click()

    except Exception as err:
        print(f'Error occurred: {err}')
        browser.close()

    f.close()
    browser.close()


initial_url = 'https://scholar.google.com/citations?view_op=view_org&hl=en&org=6139287000594560576'

get_teachers('FEUP', initial_url)
