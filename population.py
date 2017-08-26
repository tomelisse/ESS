from __future__ import print_function
from animals import Dove, Hawk 
from matplotlib import pyplot as plt
import random
import string

class Population(object):
    ''' class for a population of birds '''
    _evolution_time  = 10
    _limit           = 400000 
    # percentage of population removed during mass extinction
    _extinction_factors = [ 0.6, 0.7, 0.8, 0.9]
    # number of duels wrt number of members
    _duels_percentage = 0.5
    _ID_length = 7 

    _win       = 50 
    _wounds    = -100
    _timewaste = -10
    _duels_rules = {('Dove', 'Dove'):(_win+_timewaste, _timewaste),
                    ('Dove', 'Hawk'):(0, _win),
                    ('Hawk', 'Dove'):(_win, 0),
                    ('Hawk', 'Hawk'):(_win ,_wounds)}
    def __init__(self):
        ''' Population composition '''
        n_doves = 50
        n_all   = 100
        self.counter = {'Dove': 0, 'Hawk' : 0, 'all' : 0}
        self.bird    = {'Dove':Dove, 'Hawk':Hawk}
        self.members = dict()
        species      = ['Dove', 'Hawk']
        for i in range(n_all):
            index = i in range(n_doves, n_all)
            spec = species[index] 
            self.add_member(spec)
        # data for the plots
        self.ratio = []
        self.doves = []
        self.hawks = []

    def generate_ID(self):
        ''' generates unique ID for the birs '''
        ID = ''.join([random.choice(string.ascii_letters) 
                      for _ in range(self.__class__._ID_length)])
        if ID in self.members:
            ID = self.generate_ID()
        return ID

    def add_member(self, species):
        ''' adds a new member to the Population '''
        ID = self.generate_ID()
        member = self.bird[species]()
        self.members[ID]       = member
        self.counter[species] += 1 
        self.counter['all'  ] += 1

    def remove_member(self, ID):
        ''' remove the given member from the Population '''
        species = self.members[ID].__class__.__name__
        del self.members[ID]
        self.counter[species] -= 1 
        self.counter['all']   -= 1

    def reproduction(self):
        ''' reproduction of individuals depending on their HP '''
        print('-> reproduction')
        # copy the original list
        members = list(self.members.values())
        for member in members:
            litter_size = member.litter()
            # print('{} of HP:{:d} has {:d} children'.format(member.species, member.HP, litter_size))
            for _ in range(litter_size):
                species = member.__class__.__name__
                self.add_member(species)

    def remove_random_member(self, IDs):
        ''' mass extinction helper '''
        ID = random.choice(IDs)
        try: 
            self.remove_member(ID)
        except KeyError:
            self.remove_random_member(IDs)

    def mass_extinction(self):
        ''' if Population is overcrowded '''
        if self.counter['all'] > Population._limit:
            self.print_members()
            extinction_factor = random.choice(Population._extinction_factors)
            print('->>> MASS EXTINCTION <<<-')
            print('extinction factor: ', extinction_factor)
            fatalities = int(extinction_factor*self.counter['all'])
            IDs = self.members.keys()
            for _ in range(fatalities):
                self.remove_random_member(IDs)

    def extinction(self):
        ''' old and injured members die out, others get older '''
        print('-> extinction')
        for ID, member in self.members.items():
            member.age += 1
            if member.HP < 0 or member.age == member.__class__._max_age:
                self.remove_member(ID)

    def duel(self, ID1, ID2):
        ''' duel between 1 individuals '''
        player1     = self.members[ID1]
        player2     = self.members[ID2]
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
        IDs = list(self.members.keys())
        for i in range(n_duels):
            # if i%999 == 0:
            #     print('duel {} out of {}'.format(i, n_duels))
            ID1 = random.choice(IDs)
            ID2 = random.choice(IDs)
            while ID1 == ID2:
                ID2 = random.choice(IDs)
            self.duel(ID1, ID2)

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
        f.tight_layout()
        f.set_size_inches(10.5, 10.5)
        ax1.plot(self.ratio, 'mo--', ms=5)
        ax1.text(2, 0.75, 'max_age: {}\nthresholds: {}, {}, {}'.format(Dove._max_age, 
            Dove._thr1, Dove._thr2, Dove._thr3))
        ax1.set_xlabel('epoch')
        ax1.set_ylabel('ratio')
        ax2.plot(self.doves, 'o--', ms=5, label = 'doves')
        ax2.plot(self.hawks, 'yo--', ms=5, label = 'hawks')
        ax2.set_xlabel('epoch')
        ax2.set_ylabel('bird count')
        ax2.legend()
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

