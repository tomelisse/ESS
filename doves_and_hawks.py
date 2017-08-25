from __future__ import print_function
from matplotlib import pyplot as plt
import random
import string

class Bird(object):
    ''' class for individual birds '''
    _max_age   = 3
    # thresholds for increasing numer of offspring
    _thr1 = 50
    _thr2 = 100
    _thr3 = 150

    def __init__(self):
        ''' bird's characteristics '''
        self.age     = 0
        self.HP      = 50

    def litter(self):
        ''' litter size, dependant on HP'''
        if self.HP < Bird._thr1:
            return 0
        if self.HP < Bird._thr2:
            return 1
        if self.HP < Bird._thr3:
            return 2
        else:
            return 3

class Dove(Bird):
    ''' dove class '''
    pass

class Hawk(Bird):
    ''' hawk class '''
    pass

class Population(object):
    ''' class for a population of birds '''
    _evolution_time  = 20
    _limit           = 400000
    # percentage of population removed during mass extinction
    _extinction_factors = [ 0.6, 0.7, 0.8, 0.9]
    # number of duels wrt number of members
    _duels_percentage = 0.5

    _win       = 50
    _wounds    = -100
    _timewaste = -10
    _duels_rules = {('Dove', 'Dove'):(_win+_timewaste, _timewaste),
                    ('Dove', 'Hawk'):(0, _win),
                    ('Hawk', 'Dove'):(_win, 0),
                    ('Hawk', 'Hawk'):(_win ,_wounds)}
    def __init__(self):
        ''' Population composition '''
        n_doves = 10
        n_all   = 100
        self.counter = {'Dove': 0, 'Hawk' : 0, 'all' : 0}
        self.bird    = {'Dove':Dove, 'Hawk':Hawk}
        self.members = []
        species      = ['Dove', 'Hawk']
        for i in range(n_all):
            index = i in range(n_doves, n_all)
            spec = species[index] 
            self.add_member(spec)
        # data for the plots
        self.ratio = []
        self.doves = []
        self.hawks = []

    def add_member(self, species):
        ''' adds a new member to the Population '''
        member = self.bird[species]()
        self.members.append(member)
        self.counter[species] += 1
        self.counter['all'  ] += 1

    def remove_member(self, index):
        ''' remove the given member from the Population '''
        species = self.members[index].__class__.__name__
        del self.members[index]
        self.counter[species] -= 1
        self.counter['all']   -= 1

    def reproduction(self):
        ''' reproduction of individuals depending on their HP '''
        print('-> reproduction')
        # copy the original list
        members = list(self.members)
        for member in members:
            litter_size = member.litter()
            # print('{} of HP:{:d} has {:d} children'.format(member.species, member.HP, litter_size))
            for _ in range(litter_size):
                species = member.__class__.__name__
                self.add_member(species)

    def mass_extinction(self):
        ''' if Population is overcrowded '''
        if self.counter['all'] > Population._limit:
            self.print_members()
            extinction_factor = random.choice(Population._extinction_factors)
            print('->>> MASS EXTINCTION <<<-')
            print('extinction factor: ', extinction_factor)
            fatalities = int(extinction_factor*self.counter['all'])
            for _ in range(fatalities):
                index  = random.choice(xrange(self.counter['all']))
                self.remove_member(index)

    def extinction(self):
        ''' old and injured members die out, others get older '''
        print('-> extinction')
        # died = 0
        members = list(self.members)
        index = 0
        for member in members:
            member.age += 1
            if member.HP < 0 or member.age == Bird._max_age:
                # print('{} of HP {} dies'.format(member.species, member.HP))
                self.remove_member(index)
            else:
                index += 1
                # died += 1
        # print('died: ', died)

    def duel(self, index1, index2):
        ''' duel between 2 individuals '''
        player1     = self.members[index1]
        player2     = self.members[index2]
        results     = self._duels_rules[player1.__class__.__name__, 
                                        player2.__class__.__name__]
        player1.HP += results[0]
        player2.HP += results[1]
        # print('duel: {} {}:{:d} vs {} {}:{:d}'.format(self.counter, self.ID, self.HP, 
        #                                         opponent.species, opponent.ID, opponent.HP))

    def duels(self):
        ''' set up duels between pairs of members '''
        n_duels = int(Population._duels_percentage*self.counter['all'])
        print('-> duels')
        # print('=== {} duels ==='.format(n_duels))
        indices = range(self.counter['all'])
        for i in range(n_duels):
            # if i%1000 == 0:
            #     print('duel {} out of {}'.format(i, n_duels))
            index1 = random.choice(indices)
            index2 = random.choice(indices)
            while index1 == index2:
                index2 = random.choice(indices)
            self.duel(index1, index2)

    def update_plot_data(self):
        ''' update info about the number of each species '''
        doves = self.counter['Dove']
        hawks = self.counter['Hawk']
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
        ax1.text(2, 0.75, 'max_age: {}\nthresholds: {}, {}, {}'.format(Bird._max_age, 
            Bird._litter_thr1, Bird._litter_thr2, Bird._litter_thr3))
        ax2.plot(self.doves, 'o--', ms=5)
        # ax2.xlabel('epochs')
        # ax2.ylabel('Doves')
        ax2.plot(self.hawks, 'yo--', ms=5)
        # ax3.xlabel('epochs')
        # ax3.ylabel('Hawks')
        plt.show()
        # plt.savefig(plotpath)

    def introduce_perturbation(self):
        ''' check if a one-species Population is stable '''
        ''' by adding an admixture of the other species '''
        pass

    def print_members(self):
        ''' print members '''
        # print('=== print members ===')
        counter = self.counter
        print('all: ', counter['all'], 'Doves: ', counter['Dove'], 'Hawks: ', counter['Hawk'])
        # for member in list(self.members):
        #     print(member.__class__.__name__, member.HP, member.age)

    def evolution(self):
        ''' simulates the evolution of the Population '''
        self.update_plot_data()
        for epoch in range(Population._evolution_time):
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
    my_Population = Population()
    my_Population.evolution()
    # for member in my_Population.members.values():
    #     print(member.ID, member.species)
    

if __name__ == '__main__':
    main()
