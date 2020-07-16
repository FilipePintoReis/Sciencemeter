import random
from uuid import uuid4

class Paper:
    def __init__(self, field, owner):
        self.id = 'Title' + str(uuid4())
        self.owner = owner
        self.authors = [owner]
        self.field = field
        self.total_citations = 0
        self.worked_hours = 0
        self.days_left = 80

        start_hour = 15

        self.hour_mapping = {i:start_hour + int(1.8**i) for i in range(1,11)}
        self.paper_level = 0

        
    def update_paper_level(self):
        for key, val in self.hour_mapping.items():
            if self.worked_hours > val:
                if key < 11:
                    self.paper_level = key
                else:
                    self.paper_level = 10

    def increment_citations(self, number):
        self.total_citations += number
    
    def increment_hours(self, hours):
        self.worked_hours += hours
        self.update_paper_level()

    def add_author(self, author_id):
        self.authors.append(author_id)

    def decrement_days(self):
        self.days_left -= 1

    def __repr__(self):
        st = '  Title: ' + self.id + '\n' 
        st += '  Worked hours' + ' ' + str(self.worked_hours) + '\n'
        st += '\n'
        return st
