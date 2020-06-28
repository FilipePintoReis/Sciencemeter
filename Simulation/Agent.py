from random import choice

from Paper import Paper

class Agent:
    def __init__(self, id, name, free_hours, fields):
        self.id = id
        self.name = name
        self.total_free_hours = free_hours
        self.free_hours = free_hours
        self.fields = fields
        self.papers = {}
        self.finished_papers = {}

        self.field_p_map = {field: 1 for field in fields}

    def reset_hours(self):
        self.free_hours = self.total_free_hours

    def add_paper(self, id, ownership, field, paper):
        '''
        Adds paper to agent's list of papers.

        :param id: uuid id of the paper
        :param ownership: boolean to check if agent is paper's owner
        :param field: string field of the paper
        :param paper: Paper object
        '''
        self.papers[id] = [ownership, field, paper]
        
    def create_paper(self, field):
        paper = Paper(field, self.id)
        self.add_paper(paper.id, True, field, paper)

        return paper
    
    def choose_a_paper(self):
        '''
        Chooses a field based on the field_p_map.
        Chooses one of the papers the teacher has on that field.
        '''
        field_array = [field for field, number in self.field_p_map.items() for _ in range(number)]
        list_of_current_fields = [field[1] for field in self.papers.values()]

        field_array = list(filter(lambda x: x in list_of_current_fields, field_array))

        field = choice(field_array)

        papers_on_that_field = [paper_id for paper_id, l in self.papers.items() if l[1] == field]
        return choice(papers_on_that_field)

    def check_if_papers_finished(self):
        for paper_id, paper in self.papers.items():
            if paper[2].days_left <= 0:
                self.finish_paper(paper_id)

    def finish_paper(self, paper_id):
        self.finished_papers[paper_id] = self.papers[paper_id]
        del self.papers[paper_id]

    def decrement_papers_days(self):
        for paper in self.papers.values():
            if paper[0]:
                paper[2].decrement_days()
    
    def act_day(self): ## TODO para cada agente, criar uma probabilidade
        '''
        '''
        # Decide se cria paper ou não
        # Se sim, se adiciona autores ou não

        # Para cada hora livre
            # Escolher paper para trabalhar.
            # Gastar essa hora no paper.


        self.check_if_papers_finished()

        self.decrement_papers_days()

        self.reset_hours()

        print('Working')

    def __repr__(self):
        return self.name



# print(a.create_paper('math'))
