import random
import matplotlib.pyplot as plt

class Human:
    def __init__(self, name, immunity=False, infected = False):
        self.name = name
        self.immunity = immunity
        self.infected = infected
    
    def infect_human(self, days_num):
        if self.immunity == False:
            self.infected = True
        self.days_num = days_num

    def disinfect_human(self):
        self.infected = False
        self.immunity = True

    def get_day_of_infection(self):
        return self.days_num
    
    def is_infected(self):
        return self.infected

    def immunise_human(self):
        self.immunity = True
    
    def __str__(self) -> str:
        return str(self.name + ': ' + str(self.infected))

class Disease:
    def __init__(self, name, R, Severity, period, total_infections = 0, total_deaths = 0, infections_graph = [], deaths_graph = []): #R is number of people they will infect, Severity is decimal chance of dying, period is how long until they are cleared
        self.name = name
        self.R = R
        self.Severity = Severity
        self.period = period
        self.total_infections = total_infections
        self.total_deaths = total_deaths
        self.infections_graph = infections_graph
        self.deaths_graph = deaths_graph
    
    def add_infection(self):
        self.total_infections += 1
    
    def add_death(self):
        self.total_deaths += 1

    def daily_update(self, new_cases, new_deaths):
        self.infections_graph.append(new_cases)
        self.deaths_graph.append(new_deaths)
    
    def get_daily_infections(self):
        return self.infections_graph
    
    def get_daily_deaths(self):
        return self.deaths_graph
    
    def get_r_naught(self):
        return self.R
    
    def get_severity(self):
        return self.Severity
    
    def get_period(self):
        return self.period
    
    def __str__(self) -> str:
        printer = '-'*20
        print(printer)
        print("Name: " + self.name)
        print('R naught: ' + str(self.R))
        print('Severity: ' + str(self.Severity))
        print('Infectious Period: ' + str(self.period))
        print('Total Infections: ' + str(self.total_infections))
        print('Total Deaths: ' + str(self.total_deaths))
        return printer

def random_name_gen():
    name = ''
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    for i in range(random.randint(3, 10)):
        if name == '':
            if (random.randint(1, 2)) == 2:
                name += random.choice(vowels)
            else:
                name += random.choice(consonants)
        else:
            if name[-1] in vowels:
                name += random.choice(consonants)
            else:
                name += random.choice(vowels)
    return name

#initialisation of disease and population
population = []
for i in range(10000):
    population.append(Human(random_name_gen()))
d1 = Disease('Sars-Cov-2 Omicron Ba2', 7, 0.03, 7)

#main routine initialisation
number_of_inital_infections = 1
for i in range(number_of_inital_infections):
    prime_infector = random.choice(population)
    prime_infector.infect_human(1)

def get_number_of_infected_people(population):
    count = 0
    for person in population:
        if person.is_infected() == True:
            count += 1
    return count

def day(population, days_num, d1):
    random.shuffle(population)
    cur_num_of_cases = get_number_of_infected_people(population)
    new_cases = 0
    new_deaths = 0
    r_naught = d1.get_r_naught()
    severity = d1.get_severity()
    period = d1.get_period()
    #run through the population and infect random 7 people for each current case (need r_naught)
    for i in range(cur_num_of_cases):
        r_naught = d1.get_r_naught()
        for person in population:
            if r_naught > 0:
                if person.is_infected() == False:
                    person.infect_human(days_num)
                    d1.add_infection()
                    new_cases += 1
                    r_naught -= 1
            else:
                break
    #run through population and check every infected person for being healed (need period)
    for person in population:
        if person.is_infected() == True:
            if (days_num - person.get_day_of_infection()) >= period:
                person.disinfect_human()
    #run through population and randomly kill off an infected person based on the severity (need severity)
    for person in population:
        if person.is_infected() == True:
            if random.random() <= severity:
                population.pop(population.index(person))
                d1.add_death()
                new_deaths += 1
    d1.daily_update(new_cases, new_deaths)
    print("Day:", days_num)
    print("New Cases:", new_cases)
    print("New Deaths:", new_deaths)
    return population

#main routine proper    
days_num = 1
while True:
    ui = int(input("Enter number of days to skip forward -: "))
    for i in range(ui):
        population = day(population, days_num, d1)
        days_num += 1
    plt.plot(d1.get_daily_infections(), label='Daily Cases')
    plt.plot(d1.get_daily_deaths(), label='Daily Cases')
    plt.show()
    print(d1)
