class Paper:
    def __init__(self, name, authors, publication_date, total_citations="unknown"):
        self.name = name
        self.authors = authors
        self.publication_date = publication_date
        self.total_citations = total_citations
    
    
    def __str__(self):
        s = ''
        s += 'Paper\n' + self.name + '\n'
        for author in self.authors:
            s += author + ','
        s = s[:-1] + '\n'
        s += str(self.publication_date) + '\n' + str(self.total_citations) + '\n'
        return s

