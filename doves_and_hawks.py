from population import Population
from matplotlib import pyplot as plt

def main():
    ''' main '''
    f, ax = plt.subplots()
    g, bx = plt.subplots()
    numbers = [10, 30, 50 ,70, 80, 90, 95]
    for number in numbers:
        print '--------' + str(number) + '--------'
        my_Population = Population(number,100)
        my_Population.evolution()
        ax.plot(my_Population.ratio, 'o--', ms = 4, label = str(number)+'%')
        bx.plot(my_Population.doves, my_Population.hawks, 'o-', ms = 4, label = str(number)+'%')
    ax.axhline(y=5./7., color = 'g', label = 'stable ratio')
    ax.set_xlabel('epoch')
    ax.set_ylabel('ratio')
    ax.legend()
    
    bx.set_xlabel('doves')
    bx.set_ylabel('hawks')
    bx.set_xlim([0,1])
    bx.set_ylim([0,1])
    bx.legend()
    f.savefig('ratios.png')
    g.savefig('doves_vs_hawks.png')

if __name__ == '__main__':
    main()
