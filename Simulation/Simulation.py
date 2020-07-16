from Agent import Paper, Agent
from random import sample, choice, randint
import string


# Utils
def randomString(stringLength = 8):
    vowels = 'aieou'
    ret_val = ''.join(choice(vowels) for i in range(stringLength))
    
    ret_val = ret_val[0].upper() + ret_val[1:]

    return ret_val

class Simulation:
    def __init__(self, number_of_teachers, simulation_days, directives={}):
        self.dictionary = {}  # K -> Agent ID || V -> Agent class
        self.k = 0
        self.populate(number_of_teachers)
        self.number_of_teachers = number_of_teachers
        self.initialize_agents_maps()
        self.simulation_days = simulation_days
        self.completed_papers = 0
        self.number_of_coauthors = {0: 0, 1: 0, 2: 0}
        self.papers_per_field = {}
        self.directives = directives

        self.papers_p1 = 0
        self.papers_p2 = 0
        self.papers_p3 = 0
        self.papers_p4 = 0
        self.papers_p5 = 0
        self.papers_p6 = 0
        self.papers_p7 = 0
        self.papers_p8 = 0
        self.papers_p9 = 0
        self.papers_p10 = 0

    def __repr__(self):
        self.calculate_variables()

        ret = "\n"
        ret += "-------------------------------------\n"
        ret += "-                                   -\n"
        ret += "- " + "Número de professores: " + str(self.number_of_teachers)  + "         -\n"
        ret += "- " + "Dias de Simulação: " + str(self.simulation_days)  + "             -\n"
        ret += "- " + "Número de papers completo: " + str(self.completed_papers)  + "        -\n\n"
        ret += "- " + "Paper's por nível:           -\n"
        ret += "-    " + "P1: " + str(self.papers_p1)  + "                     -\n"
        ret += "-    " + "P2: " + str(self.papers_p2)  + "                     -\n"
        ret += "-    " + "P3: " + str(self.papers_p3)  + "                     -\n"
        ret += "-    " + "P4: " + str(self.papers_p4)  + "                     -\n"
        ret += "-    " + "P5: " + str(self.papers_p5)  + "                     -\n"
        ret += "-    " + "P6: " + str(self.papers_p6)  + "                     -\n"
        ret += "-    " + "P7: " + str(self.papers_p7)  + "                     -\n"
        ret += "-    " + "P8: " + str(self.papers_p8)  + "                     -\n"
        ret += "-    " + "P9: " + str(self.papers_p9)  + "                     -\n"
        ret += "-    " + "P10: "+ str(self.papers_p10)  + "                    -\n\n"

        ret += "Papers per field: " + str(self.papers_per_field) + "\n\n"

        ret += "Co-authors " + str(self.number_of_coauthors)  + "\n"

        return ret
    
    def calculate_variables(self):
        self.completed_papers = 0
        for agent in self.dictionary.values():
            for paper in agent.finished_papers.values():
                paper_level = paper[2].paper_level
                if paper[2].owner == agent.id:
                    self.update_papers(paper_level)
                    self.completed_papers += 1

                    self.number_of_coauthors[len(paper[2].authors) - 1] += 1


                if paper[2].field in self.papers_per_field:
                    self.papers_per_field[paper[2].field] += 1
                else:
                    self.papers_per_field[paper[2].field] = 1

    def update_papers(self, paper_level):
        if paper_level == 1:
            self.papers_p1 += 1

        elif paper_level == 2:
            self.papers_p2 += 1

        elif paper_level == 3:
            self.papers_p3 += 1

        elif paper_level == 4:
            self.papers_p4 += 1

        elif paper_level == 5:
            self.papers_p5 += 1

        elif paper_level == 6:
            self.papers_p6 += 1

        elif paper_level == 7:
            self.papers_p7 += 1

        elif paper_level == 8:
            self.papers_p8 += 1

        elif paper_level == 9:
            self.papers_p9 += 1

        elif paper_level == 10:
            self.papers_p10 += 1

    def populate(self, number_of_teachers):
        self.dictionary = {}
        list_of_fields = ['Math', 'Physics', 'CS', 'Mechanics', 'Bioengineering', 'Law', 'Databases', 'Civil']
        
        def next_3_field():
            ret = []
            for _ in range(3):
                ret.append(list_of_fields[self.k % (len(list_of_fields) - 1)])
                self.k += 1
            return ret

        for i in range(number_of_teachers):
            random_string = randomString()
            self.dictionary[i] = Agent(i, random_string, randint(4,5), next_3_field(), self)
        
    def initialize_agents_maps(self):
        for agent in self.dictionary.values():
            agent.initialize_agent_p_map()

    def print_agents(self):
        for agent in self.dictionary.values():
            print(agent.name)
            print()
            
            print('Current papers')
            for paper in agent.papers.values():
                print(paper[2])

            print('Finished papers')
            for paper in agent.finished_papers.values():
                print(paper[2])

            print('Other agents')
            print(agent.agent_p_map)

    # Maximize number of papers.
    def directive_amount_of_papers(self, delta, agent):
        agent.d_p_number += delta

    # Maximize number of papers from a given level.
    def directive_papers_per_level(self, paper, level, agent):
        if paper is not None:
            if agent.papers[paper][2].paper_level < level:
                if agent.papers[paper][2].id in agent.paper_p_map:
                    agent.paper_p_map[agent.papers[paper][2].id] += 3
            else:
                if agent.papers[paper][2].id in agent.paper_p_map:
                    agent.paper_p_map[agent.papers[paper][2].id] -= 5

    # Maximize number of papers from a given field.
    def directive_papers_per_field(self, field, agent):
        if 'field' in agent.day_actions:
            for f in agent.day_actions['field']:
                if f == field:
                    agent.field_p_map[field] += 1

    # Maximize number of co-authors
    def directive_number_coauthors(self, agent):
        if 'agent' in agent.day_actions:
            agent.number_authors_p_map[len(agent.day_actions['agent'])] += len(agent.day_actions['agent'])


    def simulation(self):
        for i in range(self.simulation_days):
            for agent in self.dictionary.values():
                agent.act_day()


simul = Simulation(20, 1000, {'agent' : 0.1, 'level': 10})

simul.simulation()

print(simul)