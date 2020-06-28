from Agent import Paper, Agent
from random import sample, choice, randint
import string


# Utils
def randomString(stringLength = 8):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(stringLength))


def populate(number_of_students):
    dictionary = {}
    list_of_fields = ['Math', 'Physics', 'CS', 'Mechanics', 'Bioengineering', 'Law', 'Databases', 'Civil']

    for i in range(number_of_students):
        random_string = randomString()
        dictionary[random_string] = Agent(i, random_string, randint(4,5), sample(list_of_fields, 3))

    return dictionary

def simulation(simulation_days = 3):
    dictionary = populate(3)

    for id, agent in dictionary.items(): 
        print(agent.id, agent.name, agent.free_hours, agent.fields)
    
    for i in range(simulation_days):
        for agent in dictionary.values():
            agent.act_day()
        print()



simulation()