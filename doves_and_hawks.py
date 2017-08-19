class bird:
    ''' class for individual birds '''
    _win       = 50
    _wounds    = -100
    _timewaste = -10
    _max_age   = 5

    def __init__(self, species):
        ''' bird's characteristics '''
        self.species = species
        self.age     = 0
        self.HP      = 50

    def duel(self, opponent):
        ''' duel between 2 individuals '''
        if self.species == 'hawk' and opponent.species == 'hawk':
            self.HP     += _win
            opponent.HP += _wounds
        if self.species == 'hawk' and opponent.species == 'dove':
            self.HP     += _win
        if self.species == 'dove' and opponent.species == 'hawk':
            opponent.HP += _win
        if self.species == 'dove' and opponent.species == 'dove':
            self.HP     += _win + _timewaste
            opponent.HP += _timewaste

    def time_flow(self):
        ''' after a year has passed '''
        self.age += 1

    def litter(self):
        ''' litter size, dependant on HP'''
        if self.HP <= 0:
            return 0
        if self.HP < 30:
            return 1
        if self.HP < 60:
            return 2
        else:
            return 3

class population:
    ''' class for a population of birds '''
    def __init__(self):
        ''' population composition '''
        self.n_doves = 50
        self.n_all   = 100
        self.n_hawks = self.n_all - self.n_doves
        species = ['dove', 'hawk']
        self.members = [bird(species[i in range(self.n_doves, self.n_all)]) 
                        for i in range(self.n_all)]

    def reproduction(self):
        ''' reproduction of individuals depending on their HP '''
        for member in self.members:
            litter = member.litter()
            for _ in range(litter):
                self.members.append(bird(member.species))

    def extinction(self):
        ''' old and injured members die out '''
        for member in self.members:
            if member.HP < 0 or member.age >= __class__???max_age:
                #die! - how to die within a list? or use another collector??

def main():
    ''' main '''
    my_population = population()
    for member in my_population.members:
        print(member.species)
    

if __name__ == '__main__':
    main()
