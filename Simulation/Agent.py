from random import choice, sample, random

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

        ### Reinforcement learning variables.
        self.d_p_number = 2 # Number used to decide whether to create a new paper or not.
        self.number_authors_p_map = {0:1, 1:1, 2:1}
        self.paper_p_map = {}
        self.agent_p_map = {}
        self.field_p_map = {key: 1 for key in self.fields}
        ### 

        self.day_actions = {} 
        # This should have values for:
        #    paper: <Paper> 
        #    agents: <Agent>
        #    field: <Field>

    def initialize_agent_p_map(self):
        '''
        Initializes each agent's agent probablity map.
        '''
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

        paper.add_author(self.id)

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

            if 'agent' in self.day_actions:
                self.day_actions['agent'].append(author)
            else:
                self.day_actions['agent'] = [author]

    def choose_paper(self):
        '''
        Chooses a paper based on paper_p_map
        '''
        papers = [paper_id for paper_id, value in self.paper_p_map.items() for i in range(value)]
        
        ret = choice(papers) if len(papers) > 0 else None

        if 'paper' not in self.day_actions:
            self.day_actions['paper'] = [ret]
        else:
            self.day_actions['paper'].append(ret)

        return ret

    def choose_authors(self, number, field):
        '''
        Chooses number authors based on agent_p_map
        '''
        teachers = [teacher_id for teacher_id, value in self.agent_p_map.items() for i in range(value) if field in self.simulation.dictionary[teacher_id].fields]

        return sample(teachers, number)
    
    def number_of_coauthors(self):
        '''
        Chooses number co-author based on number_authors_p_map
        '''
        numbers = [number for number, value in self.number_authors_p_map.items() for i in range(value)]

        return choice(numbers)
    
    def choose_field(self):
        '''
        Chooses a field based on field_p_map
        '''
        fields = [field for field, value in self.field_p_map.items() for i in range(value)]
        
        ret = choice(fields)

        if 'field' not in self.day_actions:
            self.day_actions['field'] = [ret]
        else:
            self.day_actions['field'].append(ret)

        return ret 

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

    def decide_to_create_paper(self):
        n = random()

        if len(self.papers) == 0 or n < (self.d_p_number/len(self.papers)):
            self.create_paper(self.choose_field())

    def run_directives(self):
        for key, val in self.simulation.directives.items():

            if key == 'level':
                if 'paper' in self.day_actions:
                    for paper in self.day_actions['paper']:
                        self.simulation.directive_papers_per_level(paper, self.simulation.directives['level'], self)
            
            if key == 'field':
                if 'field' in self.day_actions:
                    for field in self.simulation.directives['field']:
                        self.simulation.directive_papers_per_field(field, self)
            
            if key == 'delta':
                if 'field' in self.day_actions:
                    for _ in self.day_actions['field']:
                        self.simulation.directive_amount_of_papers(self.simulation.directives['delta'], self)

            if key == 'agent':
                if 'agent' in self.day_actions:
                    for _ in self.day_actions['agent']:
                        self.simulation.directive_number_coauthors(self)


    def act_day(self):
        '''
        Player's actions for a day.
        '''

        # Decide to create paper or not, and if so, create it.
        self.decide_to_create_paper()

        # Check which papers are finished.
        finished_papers = self.check_if_papers_finished()

        # Move finished papers to respective dictionary.
        for agent in self.simulation.dictionary.values():
            for paper in finished_papers:
                try:
                    agent.finish_paper(paper)
                except:
                    pass

        # For each free hour, choose a paper to work and work on it.
        for hour in range(self.free_hours):
            paper_id = self.choose_paper()
            if paper_id is not None:
                self.papers[paper_id][2].increment_hours(1)

        # Decrement paper's days.
        self.decrement_papers_days()

        # Here we should do the reinforcement learning.
        self.run_directives()
        #print(self.day_actions)

        # This is ought to clear this day's actions after reinforcement is done.
        self.day_actions.clear()

    def __repr__(self):
        return str(self.id)
