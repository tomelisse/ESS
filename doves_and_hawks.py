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
        win       = self.__class__._win
        wounds    = self.__class__._wounds
        timewaste = self.__class__._timewaste
        if self.species == 'hawk' and opponent.species == 'hawk':
            self.HP     += win
            opponent.HP += wounds
        if self.species == 'hawk' and opponent.species == 'dove':
            self.HP     += win
        if self.species == 'dove' and opponent.species == 'hawk':
            opponent.HP += win
        if self.species == 'dove' and opponent.species == 'dove':
            self.HP     += win + timewaste
            opponent.HP += timewaste
        print('duel: {} {}:{:d} vs {} {}:{:d}'.format(self.species, self.ID, self.HP, 
                                                opponent.species, opponent.ID, opponent.HP))

    def litter(self):
        ''' litter size, dependant on HP'''
        if self.HP <= 0:
            return 0
        if self.HP <= 50:
            return 1
        if self.HP <= 100:
            return 2
        else:
            return 3

class population:
    _evolution_time  = 2
    # number of duels wrt number of members
    _duels_percentage = 0.5
    ''' class for a population of birds '''
    def __init__(self):
        ''' population composition '''
        n_doves = 2 
        n_all   = 5
        self.species = {'dove': 0, 'hawk' : 0, 'all' : 0}
        species = ['dove', 'hawk']
        self.members = dict()
        for i in range(n_all):
            index = i in range(n_doves, n_all)
            spec = species[index] 
            self.add_member(spec)

    def add_member(self, species):
        ''' adds a new member to the population '''
        member = bird(species)
        while member.ID in self.members:
            member = bird(species)
        self.members[member.ID] = member
        self.species[species] += 1
        self.species['all'  ] += 1

    def remove_member(self, id, species):
        ''' remove the given member from the population '''
        del self.members[id]
        self.species[species] -= 1
        self.species['all']   -= 1

    def reproduction(self):
        ''' reproduction of individuals depending on their HP '''
        print('==reproduction===')
        for member in list(self.members.values()):
            litter_size = member.litter()
            print('{} {} of HP:{:d} has {:d} children'.format(member.species, member.ID, member.HP, litter_size))
            for _ in range(litter_size):
                species = member.species
                self.add_member(species)

    # TODO: add population size limit
    def extinction(self):
        print('=== extinction ===')
        ''' old and injured members die out, others get older '''
        for member in list(self.members.values()):
            member.age += 1
            if member.HP < 0 or member.age >= member.__class__._max_age:
                print('extict: {}, HP: {:d}, age: {:d}'.format(member.ID, member.HP, member.age))
                self.remove_member(member.ID, member.species)

    def duels(self):
        ''' set up duels between pairs of members '''
        n_duels = int(self.__class__._duels_percentage*self.species['all'])
        print('==={} duels ==='.format(n_duels))
        for _ in range(n_duels):
            player1_ID = random.choice(list(self.members.keys()))
            player2_ID = random.choice(list(self.members.keys()))
            while player2_ID == player1_ID:
                player2_ID = random.choice(list(self.members.keys()))
            self.members[player1_ID].duel(self.members[player2_ID])

    def update_plots(self):
        ''' update info about the number of each species '''
        pass

    def introduce_perturbation(self):
        ''' check if a one-species population is stable '''
        ''' by adding an admixture of the other species '''
        pass

    def print_members(self):
        ''' print members '''
        print('=== print members ===')
        print('doves: ', self.species['dove'])
        print('hawks: ', self.species['hawk'])
        for member in list(self.members.values()):
            print(member.ID, member.species, member.HP, member.age)

    def evolution(self):
        ''' simulates the evolution of the population '''
        for epoch in range(self.__class__._evolution_time):
            print('epoch: {}'.format(epoch))
            self.print_members()
            self.duels()
            self.extinction()
            self.reproduction()
            self.update_plots()
        self.print_members()


def main():
    ''' main '''
    my_population = population()
    my_population.evolution()
    # doves = 0
    # for member in my_population.members.values():
    #     print(member.ID, member.species)
    #     if member.species == 'dove':
    #         doves += 1
    # print(doves)
    

if __name__ == '__main__':
    main()
