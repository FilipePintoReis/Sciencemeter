import random
from uuid import uuid4

class Paper:
    def __init__(self, field, owner):
        self.id = uuid4()
        self.owner = owner
        self.authors = [owner]
        self.field = field
        self.total_citations = 0
        self.worked_hours = 0
        self.days_left = 365

        start_hour = random.randint(15, 40)

        self.hour_mapping = {i:start_hour + 1.9**i for i in range(1,11)}
        

    def increment_citations(self, number):
        self.total_citations += number
    
    def increment_hours(self, hours):
        self.worked_hours += hours

    def add_author(self, author_id):
        self.authors.append(author_id)

    def decrement_days(self):
        self.days_left -= 1

    def __repr__(self):
        st = ''
        st += 'ID: ' + str(self.id)
        return st
