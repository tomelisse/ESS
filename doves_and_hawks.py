from __future__ import print_function
from matplotlib import pyplot as plt
import random
import string

class bird:
    ''' class for individual birds '''
    _win       = 50
    _wounds    = -100
    _timewaste = -10
    _max_age   = 3
    _litter_thr1 = 50
    _litter_thr2 = 100
    _litter_thr3 = 150
    _duels_rules = {('dove', 'dove'):(_win+_timewaste, _timewaste),
                   ('dove', 'hawk'):(0, _win),
                   ('hawk', 'dove'):(_win, 0),
                   ('hawk', 'hawk'):(_win ,_wounds)}

    def __init__(self, species):
        ''' bird's characteristics '''
        self.species = species
        self.age     = 0
        self.HP      = 50

    def duel(self, opponent):
        ''' duel between 2 individuals '''
        results     = bird._duels_rules[self.species, opponent.species]
        self.HP     += results[0]
        opponent.HP += results[1]
        # print('duel: {} {}:{:d} vs {} {}:{:d}'.format(self.species, self.ID, self.HP, 
        #                                         opponent.species, opponent.ID, opponent.HP))

    def litter(self):
        ''' litter size, dependant on HP'''
        if self.HP < bird._litter_thr1:
            return 0
        if self.HP < bird._litter_thr2:
            return 1
        if self.HP < bird._litter_thr3:
            return 2
        else:
            return 3

class population:
    _evolution_time  = 10 
    _limit = 400000
    # percentage of population perished during mass extinction
    _extinction_factors = [ 0.6, 0.7, 0.8, 0.9]
    # number of duels wrt number of members
    _duels_percentage = 0.5
    ''' class for a population of birds '''
    def __init__(self):
        ''' population composition '''
        n_doves = 50
        n_all   = 100
        self.species = {'dove': 0, 'hawk' : 0, 'all' : 0}
        # data for the plots
        self.ratio = []
        self.doves = []
        self.hawks = []
        species = ['dove', 'hawk']
        self.members = []
        for i in range(n_all):
            index = i in range(n_doves, n_all)
            spec = species[index] 
            self.add_member(spec)

    def add_member(self, species):
        ''' adds a new member to the population '''
        member = bird(species)
        self.members.append(member)
        self.species[species] += 1
        self.species['all'  ] += 1

    def remove_member(self, index):
        ''' remove the given member from the population '''
        species = self.members[index].species
        del self.members[index]
        self.species[species] -= 1
        self.species['all']   -= 1

    def reproduction(self):
        ''' reproduction of individuals depending on their HP '''
        print('-> reproduction')
        # copy the original list
        members = list(self.members)
        for member in members:
            litter_size = member.litter()
            # print('{} {} of HP:{:d} has {:d} children'.format(member.species, member.ID, member.HP, litter_size))
            for _ in range(litter_size):
                species = member.species
                self.add_member(species)

    def mass_extinction(self):
        ''' if population is overcrowded '''
        if self.species['all'] > population._limit:
            self.print_members()
            extinction_factor = random.choice(population._extinction_factors)
            print('->>> MASS EXTINCTION <<<-')
            print('extinction factor: ', extinction_factor)
            fatalities = int(extinction_factor*all_members)
            for _ in range(fatalities):
                index  = random.choice(range(self.species['all']))
                self.remove_member(index)

    def extinction(self):
        ''' old and injured members die out, others get older '''
        print('-> extinction')
        # died = 0
        members = list(self.members)
        index = 0
        for member in members:
            member.age += 1
            if member.HP < 0 or member.age == bird._max_age:
                self.remove_member(index)
            else:
                index += 1
                # died += 1
        # print('died: ', died)

    def duels(self):
        ''' set up duels between pairs of members '''
        n_duels = int(population._duels_percentage*self.species['all'])
        print('-> duels')
        # print('=== {} duels ==='.format(n_duels))
        indices = range(self.species['all'])
        for i in range(n_duels):
            # if i%1000 == 0:
            #     print('duel {} out of {}'.format(i, n_duels))
            player1_index = random.choice(indices)
            player2_index = random.choice(indices)
            while player2_index == player1_index:
                player2_index = random.choice(indices)
            self.members[player1_index].duel(self.members[player2_index])

    def update_plot_data(self):
        ''' update info about the number of each species '''
        doves = self.species['dove']
        hawks = self.species['hawk']
        self.doves.append(doves)
        self.hawks.append(hawks)
        self.ratio.append(float(doves)/float(hawks))

    def prepare_plots(self):
        ''' prepares plots '''
        plotpath = 'plots/ratio.png'
        f, (ax1, ax2) = plt.subplots(2,1)
        ax1.plot(self.ratio, 'mo--', ms=5)
        # ax1.xlabel('epochs')
        # ax1.ylabel('ratios')
        ax1.text(2, 0.75, 'max_age: {}\nthresholds: {}, {}, {}'.format(bird._max_age, 
            bird._litter_thr1, bird._litter_thr2, bird._litter_thr3))
        ax2.plot(self.doves, 'o--', ms=5)
        # ax2.xlabel('epochs')
        # ax2.ylabel('doves')
        ax2.plot(self.hawks, 'yo--', ms=5)
        # ax3.xlabel('epochs')
        # ax3.ylabel('hawks')
        plt.show()
        # plt.savefig(plotpath)

    def introduce_perturbation(self):
        ''' check if a one-species population is stable '''
        ''' by adding an admixture of the other species '''
        pass

    def print_members(self):
        ''' print members '''
        # print('=== print members ===')
        species = self.species
        print('all: ', species['all'], 'doves: ', species['dove'], 'hawks: ', species['hawk'])
        # for member in list(self.members.values()):
        #     print(member.ID, member.species, member.HP, member.age)

    def evolution(self):
        ''' simulates the evolution of the population '''
        self.update_plot_data()
        for epoch in range(population._evolution_time):
            print('======== epoch: {} ========'.format(epoch))
            self.print_members()
            self.duels()
            self.extinction()
            self.reproduction()
            self.mass_extinction()
            self.update_plot_data()
        self.print_members()
        self.prepare_plots()


def main():
    ''' main '''
    my_population = population()
    my_population.evolution()
    # for member in my_population.members.values():
    #     print(member.ID, member.species)
    

if __name__ == '__main__':
    main()
