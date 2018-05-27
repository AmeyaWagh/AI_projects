#!/usr/bin/python

# Genetic Algorithm
import random
from random import shuffle
import bisect


def genetic_algorithm(population, fitness_fn, gene_pool=[0, 1], f_thres=None, ngen=1000, pmut=0.1):  # noqa
    """[Figure 4.8]"""

    bestCase = [population[0],fitness_fn(population[0])]

    for iterations in range(ngen):
        print '\n\n',iterations

        new_population = []
        #create a function pointer for random selection
        random_selection = selection_chances(fitness_fn, population)

        for j in range(len(population)):
            x = random_selection()
            y = random_selection()
            print 'x:',x,'y:',y,
            child = reproduce(x, y)
            print 'child',child,'fitness:',fitness_fn(child)
            if random.uniform(0, 1) < pmut:
                child = mutate(child, gene_pool)
            new_population.append(child)

        population = new_population
        # print 'new population',population

        if f_thres:
            # fittest_individual = argmax(population, key=fitness_fn)
            fittest_individual = getFittestIndividual(population,fitness_fn)
            print 'fittest',fittest_individual,'fval:',fitness_fn(fittest_individual)
            
            if fitness_fn(fittest_individual) > bestCase[1]:
                bestCase = [fittest_individual,fitness_fn(fittest_individual)]


            if fitness_fn(fittest_individual) >= f_thres:
                print ("found fittest Individual")
                return fittest_individual

    print '\n\ncompleted {} generations'.format(ngen)
    # return getFittestIndividual(population, fitness_fn)
    return bestCase[0]


def getFittestIndividual(population,fitness_fn):
    fitness_values = map(fitness_fn,population)
    return population[fitness_values.index(max(fitness_values))]

def init_population(pop_number, gene_pool):
    g = len(gene_pool)
    population = []
    for i in range(pop_number):
        shuffle(gene_pool)
        new_individual = gene_pool[:]

        # make it a complete loop
        new_individual.append(new_individual[0])
        
        # add to population
        population.append(new_individual)
    return population


# roulette wheel selection
def selection_chances(fitness_fn, population):
    fitnesses = map(fitness_fn, population)
    return weighted_sampler(population, fitnesses)


# ordered cross over
def reproduce(x, y):
    #remove initial city from the end to create open loop
    x = x[:-1]
    y = y[:-1]

    n = len(x)
    c = random.randrange(1, n)
    offSpring=x[:c]

    for i in range(n):
        if y[i] not in offSpring:
            offSpring.append(y[i])
    offSpring.append(offSpring[0])
    return offSpring


# Swap Mutation
def mutate(x,gene_pool):
    #remove initial city from the end to create open loop
    x = x[:-1]

    n=len(x)
    # print 'x before',x
    i1 = random.randrange(0, n)
    i2 = random.randrange(0, n)
    gene1 = x[i1]
    gene2 = x[i2]
    x[i1]=gene2
    x[i2]=gene1
    x.append(x[0])
    print 'Mutation:',x
    return x

def weighted_sampler(seq, weights):
    """Return a random-sample function that picks from seq weighted by weights."""
    totals = []
    for w in weights:
        totals.append(w + totals[-1] if totals else w)

    return lambda: seq[bisect.bisect(totals, random.uniform(0, totals[-1]))]