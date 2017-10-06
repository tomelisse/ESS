class Bird(object):
    ''' class for individual birds '''
    _max_age   = 1
    # thresholds for increasing numer of offspring
    _thr1 = 50
    _thr2 = 100
    _thr3 = 150

    def __init__(self):
        ''' bird's characteristics '''
        self.age     = 0
        self.HP      = 100

    def litter(self):
        ''' litter size, dependant on HP'''
        return int(float(self.HP)/10)
        # if self.HP < Bird._thr1:
        #     return 0
        # if self.HP < Bird._thr2:
        #     return 1
        # if self.HP < Bird._thr3:
        #     return 2
        # else:
        #     return 3

class Dove(Bird):
    ''' dove class '''
    pass

class Hawk(Bird):
    ''' hawk class '''
    pass
