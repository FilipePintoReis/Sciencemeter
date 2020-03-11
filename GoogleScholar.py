from bs4 import BeautifulSoup
import requests


def parseProfile(url):
    try:
        response = requests.get(url, timeout = (30, 30)) # timeout is in seconds, first is connecting, second is reading
        response.raise_for_status()
        if response.status_code == 200: 
            soup = BeautifulSoup(response.content, 'html.parser')
            papers = soup.find_all(class_="gsc_a_tr")
            print(papers)

    except Exception as err:
        print(f'Error occurred: {err}')


parseProfile("https://scholar.google.com/citations?user=3IqnhE4AAAAJ&hl=en")