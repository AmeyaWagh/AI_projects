#!/usr/bin/python

from solver import *
# import solver


table = [(0,1,6,8,1),
            (4,0,3,4,2),
            (2,5,0,2,9),
            (5,7,4,0,7),
            (2,1,6,3,0)]

state = [0,2,1]
# genePool = [0,1,2] 
genePool=range(5)

def printTable():
    for row in table:
        print(row)

def getMSTDist(state):
    MSTdist=0
    for i in range(len(state)-1):
        MSTdist += table[state[i]][state[i+1]]
        # print table[state[i]][state[i+1]]
    # print 'MST',MSTdist
    return MSTdist

def getFitness(state):
    return 1.0/(1.0+getMSTDist(state)) 


if __name__ == '__main__':
    print('-'*80)
    printTable()
    print('-'*80)
    print(getMSTDist(state))

    population = init_population(15,genePool)
    # print 'population',population
    fitNode = genetic_algorithm(population,
                                getFitness,
                                genePool,
                                f_thres=0.5,
                                ngen=10000,
                                pmut=0.5)
    
    print fitNode,'fitness:',getFitness(fitNode),'MST:',getMSTDist(fitNode)