from population import Population

def main():
    ''' main '''
    my_Population = Population()
    my_Population.evolution()
    # for member in my_Population.members.values():
    #     print(member.ID, member.species)
    

if __name__ == '__main__':
    main()
