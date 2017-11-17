from population import Population
from matplotlib import pyplot as plt

def main():
    ''' main '''
    numbers = [10,90]
    for number in numbers:
        print '=====' + str(number) + '====='
        my_Population = Population(number,100)
        my_Population.evolution()
        plt.plot(my_Population.ratio, 'o--', ms = 4, label = str(number)+'%')
    plt.axhline(y=5./7., color = 'g', label = 'stable ratio')
    plt.xlabel('epoch')
    plt.ylabel('ratio')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
