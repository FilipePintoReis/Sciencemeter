from random import choice, sample

from Paper import Paper

class Agent:
    def __init__(self, id, name, free_hours, fields, simulation):
        self.id = id
        self.name = name
        self.free_hours = free_hours
        self.fields = fields
        self.papers = {} # Key = id ; Value = [ownership, field, paper]
        self.finished_papers = {} # Key = id ; Value = [ownership, field, paper]
        self.simulation = simulation
        
        self.number_authors_p_map = {0:1, 1:1, 2:1}
        self.paper_p_map = {}
        self.agent_p_map = {}

    def initialize_agent_p_map(self):
        for agent in self.simulation.dictionary.values():
            if agent.id != self.id:
                self.agent_p_map[agent.id] = 1

    def add_paper(self, id, ownership, field, paper):
        '''
        Adds paper to agent's list of papers.

        :param id: uuid id of the paper
        :param ownership: boolean to check if agent is paper's owner
        :param field: string field of the paper
        :param paper: Paper object
        '''
        self.papers[id] = [ownership, field, paper]
        self.paper_p_map[id] = 1
        
    def create_paper(self, field):
        '''
        Creates a paper in the given field.

        :param field: string field of new paper
        :return: tuple with the paper object and other authors
        '''
        paper = Paper(field, self.id)
        self.add_paper(paper.id, True, field, paper)

        other_authors = self.choose_authors(self.number_of_coauthors(), field)

        for author in other_authors:
            self.simulation.dictionary[author].add_paper(paper.id, False, field, paper)


    def choose_paper(self):
        '''
        Chooses a paper based on paper_p_map
        '''
        papers = [paper_id for paper_id, value in self.paper_p_map.items() for i in range(value)]


        return None if len(papers) == 0 else choice(papers)

    def choose_authors(self, number, field):
        '''
        Chooses number authors based on agent_p_map
        '''
        teachers = [teacher_id for teacher_id, value in self.agent_p_map.items() for i in range(value) if field in self.simulation.dictionary[teacher_id].fields]

        try:
            return self.choose_authors(number - 1, field) if len(teachers) < number else sample(teachers, number)
        
        except Exception as e:
            print('Exception occurred:', e)
            return None
    
    def number_of_coauthors(self):
        '''
        Chooses number co-author based on number_authors_p_map
        '''
        numbers = [number for number, value in self.number_authors_p_map.items() for i in range(value)]

        return choice(numbers)

    def check_if_papers_finished(self):
        finished_papers = []
        for paper_id, paper in self.papers.items():
            if paper[2].days_left <= 0:
                finished_papers.append(paper_id)

        return finished_papers


    def finish_paper(self, paper_id):
        self.finished_papers[paper_id] = self.papers[paper_id]
        del self.papers[paper_id]
        self.paper_p_map[paper_id] = 0

    def decrement_papers_days(self):
        for paper in self.papers.values():
            if paper[0]:
                paper[2].decrement_days()
    
    def act_day(self):
        '''
        '''

        # Decide se cria paper ou não ## TODO make it better.
        if len(self.papers) < 10:
            self.create_paper(choice(self.fields))

        # Se sim, se adiciona autores ou não
        #print('Authors:', self.choose_authors(2))
        

        # Checkar se os papers acabaram
        finished_papers = self.check_if_papers_finished()
        
        # if finished_papers is not None and len(finished_papers) > 0: print(finished_papers)

        for paper in finished_papers:
            self.finish_paper(paper)

        # Para cada hora livre
            # Escolher paper para trabalhar.
            # Gastar essa hora no paper.
        for hour in range(self.free_hours):
            paper_id = self.choose_paper()
            if paper_id is not None:
                self.papers[paper_id][2].increment_hours(1)
                #print(self.papers[paper_id][2])

       

        # Decrementar os dias de um paper
        self.decrement_papers_days()

        #print(self.free_hours)

    def __repr__(self):
        return str(self.id)
        
# print(a.create_paper('math'))