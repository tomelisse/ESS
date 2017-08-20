import random
import string

class bird:
    ''' class for individual birds '''
    _win       = 50
    _wounds    = -100
    _timewaste = -10
    _max_age   = 5
    _ID_length = 6

    def __init__(self, species):
        ''' bird's characteristics '''
        self.species = species
        self.age     = 0
        self.HP      = 50
        self.ID      = self.generate_ID()

    def generate_ID(self):
        ''' generates ID for the birs '''
        return ''.join([random.choice(string.ascii_letters) 
                        for _ in range(self.__class__._ID_length)])

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
        self.n_doves = 40
        self.n_all   = 100
        self.n_hawks = self.n_all - self.n_doves
        species = ['dove', 'hawk']
        self.members = dict()
        for i in range(self.n_all):
            index = i in range(self.n_doves, self.n_all)
            spec = species[index] 
            self.add_member(spec)

    def add_member(self, species):
        ''' adds a new member to the population '''
        member = bird(species)
        while member.ID in self.members:
            member = bird(species)
        self.members[member.ID] = member

    def remove_member(self, id):
        ''' remove the given member from the population '''
        del self.members[id]

    def reproduction(self):
        ''' reproduction of individuals depending on their HP '''
        for member in self.members:
            litter_size = member.litter()
            for _ in range(litter_size):
                species = member.species
                self.add_member(species)

    def extinction(self):
        ''' old and injured members die out '''
        for id, member in self.members.items():
            if member.HP < 0 or member.age >= member.__class__.max_age:
                remove_member(id)

def main():
    ''' main '''
    my_population = population()
    doves = 0
    for member in my_population.members.values():
        print(member.ID, member.species)
        if member.species == 'dove':
            doves += 1
    print(doves)
    

if __name__ == '__main__':
    main()
