from __future__ import print_function
from animals import Dove, Hawk 
from matplotlib import pyplot as plt
import random
import string

class Population(object):
    ''' class for a population of birds '''
    _evolution_time  = 100
    _limit           = 50000
    # number of duels wrt number of members
    _duels_percentage = 0.5
    _ID_length = 7 

    _win       = 50 
    _wounds    = - 100
    _timewaste = - 10
    _duels_rules = {('Dove', 'Dove'):(_win+_timewaste, _timewaste),
                    ('Dove', 'Hawk'):(0, _win),
                    ('Hawk', 'Dove'):(_win, 0),
                    ('Hawk', 'Hawk'):(_win ,_wounds)}
    def __init__(self, n_doves, n_all):
        ''' Population composition '''
        self.counter = {'Dove': 0, 'Hawk' : 0, 'all' : 0}
        self.bird    = {'Dove':Dove, 'Hawk':Hawk}
        self.members = dict()
        species      = ['Dove', 'Hawk']
        for i in range(n_all):
            index = i in range(n_doves, n_all)
            spec = species[index] 
            self.add_member(spec)
        # data for the plots
        self.plotpath = 'plots/'
        self.name  = str(n_doves) + 'doves_per' + str(n_all) + 'birds'
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
        ''' and extinction of old population members if max_age == 1'''
        print('-> reproduction')
        # copy the original list
        members = list(self.members.values())
        IDs = list(self.members.keys())
        for ID, member in zip(IDs, members):
            litter_size = member.litter()
            # print('{} of HP:{:d} has {:d} children'.format(member.species, member.HP, litter_size))
            for _ in range(litter_size):
                species = member.__class__.__name__
                self.add_member(species)
            if member.__class__._max_age == 1:
                self.remove_member(ID)

    def remove_random_member(self, IDs):
        ''' mass extinction helper '''
        ID = random.choice(IDs)
        try: 
            self.remove_member(ID)
        except KeyError:
            self.remove_random_member(IDs)

    def mass_extinction(self):
        ''' if Population is overcrowded '''
        self.print_members()
        if self.counter['all'] > Population._limit:
            print('->>> MASS EXTINCTION <<<-')
            fatalities = self.counter['all'] - Population._limit
            IDs = self.members.keys()
            for _ in range(fatalities):
                self.remove_random_member(IDs)


    def extinction(self):
        ''' old and injured members die out '''
        ''' only used for max_age > 1 '''  
        if Dove._max_age > 1:
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

    def choose_ID(self, IDs, visited):
        ''' chooses a random ID which was not yet chosen '''
        ID = random.choice(IDs)
        while ID in visited:
            ID = random.choice(IDs)
        visited.add(ID)
        return ID

    def duels(self):
        ''' set up duels between pairs of members '''
        n_duels = int(Population._duels_percentage*self.counter['all'])
        print('-> duels')
        # print('=== {} duels ==='.format(n_duels))
        IDs = self.members.keys()
        visited = set()
        for i in range(n_duels):
            # if i%999 == 0:
            #     print('duel {} out of {}'.format(i, n_duels))
            ID1 = self.choose_ID(IDs, visited)
            ID2 = self.choose_ID(IDs, visited)
            self.duel(ID1, ID2)

    def update_plot_data(self):
        ''' update info about the number of each species '''
        doves = float(self.counter['Dove'])
        hawks = float(self.counter['Hawk'])
        birds = float(self.counter['all'])
        self.doves.append(doves/birds)
        self.hawks.append(hawks/birds)
        self.ratio.append(float(doves)/float(hawks))

    def prepare_plots(self):
        ''' prepares plots '''
        # f, (ax1, ax2) = plt.subplots(2,1)
        # f.tight_layout()
        # f.set_size_inches(10.5, 10.5)
        plt.plot(self.ratio, 'mo--', ms=5, label = 'ratio')
        plt.axhline(y=5./7., color = 'g', label = 'stable ratio')
        n = self.__class__._evolution_time - 1
        initial_ratio = float(self.doves[0])/float(self.hawks[0]) 
        final_ratio   = float(self.doves[n])/float(self.hawks[n]) 
        text_pos_y    = float(initial_ratio + final_ratio)/2
        text_pos_x    = float(n)/2
        plt.text(text_pos_x, text_pos_y, 'initial ratio: {}\nfinal ratio : {}'.format(initial_ratio, final_ratio))
        plt.plot(self.doves, 'o--', ms=5, label = 'doves')
        plt.plot(self.hawks, 'yo--', ms=5, label = 'hawks')
        plt.xlabel('epoch')
        plt.legend()
        plt.savefig(self.plotpath + self.name + '.png')

        plt.clf()
        plt.plot(self.doves, self.hawks, 'ko-')
        plt.xlabel('doves')
        plt.ylabel('hawks')
        plt.xlim([0,1])
        plt.ylim([0,1])
        plt.savefig(self.plotpath + self.name + '2D.png')
        plt.close()

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
            self.reproduction()
            self.extinction()
            self.mass_extinction()
            self.update_plot_data()
        self.print_members()
        # self.prepare_plots()

