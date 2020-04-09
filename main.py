from Authenticus.Authenticus import parse_profile
from GoogleScholar.GoogleScholar import parseProfile

RosaldoRossetiAu = 'https://www.authenticus.pt/en/profileOfResearchers/publicationsList/16105?total_results=162&page=1&_=1'
RosaldoRossetiGs = 'https://scholar.google.com/citations?user=3IqnhE4AAAAJ&hl=en'
AnaPaulaRochaAu = 'https://www.authenticus.pt/en/profileOfResearchers/publicationsList/1341'
AnaPaulaRochaGs = 'https://scholar.google.com/citations?user=eFrl5Z0AAAAJ&hl=en'
HenriqueLopesCardosoAu = 'https://www.authenticus.pt/en/profileOfResearchers/publicationsList/6052'
HenriqueLopesCardosoGs = 'https://scholar.google.com/citations?user=6EINAs8AAAAJ&hl=en'

 
authenticus_links = [RosaldoRossetiAu, AnaPaulaRochaAu, HenriqueLopesCardosoAu]
scholar_links = [RosaldoRossetiGs, AnaPaulaRochaGs, HenriqueLopesCardosoGs]


authenticus_papers = []
scholar_papers = []
f1 = open('papersA.csv', "a")
f2 = open('papersGS.csv', "a")


def f(set_to_use, papers_to_use):
    try:
        for link in scholar_links:
            f = False
            while f != True:
                papers = parseProfile(link, set_to_use, papers_to_use)
                f = papers[2]
                print(papers[2])
            for paper in papers[1]:
                scholar_papers.append(paper)

        for el in scholar_papers:
            f2.write(str(el) + '\n')
    except Exception as err:
        print(err)
        f(set_to_use, papers_to_use)


try:
    # for link in authenticus_links:
    #     for paper in parse_profile(link):
    #         authenticus_papers.append(paper)

    # for el in authenticus_papers:
    #     f1.write(str(el) + '\n')


    s = set()
    papers_to_use = []
    f(s, papers_to_use)

except Exception as err:
    print(err)


