#!/usr/bin/python

import random
import bisect


class geneticAlgorithm:

    def __init__(self, fitnessFn, genePool=[], nGen=10, nSize=1,
                 pMutation=0.1, fitnessThres=None):
        self.genePool = genePool
        self.nGen = nGen
        self.fitnessFn = fitnessFn
        self.population = []
        self.nSize = nSize
        self.pMutation = pMutation
        self.fitnessThres = fitnessThres
        self.initialPopulation()

    def initialPopulation(self):
        individual = self.genePool[:]
        for n in range(self.nSize):
            random.shuffle(individual)
            self.population.append(individual)

    def crossover(self, parentXX, parentXY):
        n = len(parentXX)
        c = random.randrange(1, n)
        offSpring = parentXX[:c]

        # add remaining genes of
        for i in range(n):
            if parentXY[i] not in offSpring:
                offSpring.append(parentXY[i])
        return offSpring

    def mutation(self, child):
        n = len(child)
        i1 = random.randrange(0, n)
        i2 = random.randrange(0, n)
        gene1 = child[i1]
        gene2 = child[i2]
        child[i1] = gene2
        child[i2] = gene1
        return child

    def weighted_sampler(self,seq, weights):
        """Return a random-sample function 
        that picks from seq weighted by weights."""
        totals = []
        for w in weights:
            totals.append(w + totals[-1] if totals else w)

        return lambda: seq[bisect.bisect(
            totals, random.uniform(0, totals[-1]))]

    def rouletteSelection(self):
        fitnesses = map(self.fitnessFn, self.population)
        return self.weighted_sampler(self.population, fitnesses)

    def getFittestIndividual(self):
        fitness_values = map(self.fitnessFn, self.population)
        return self.population[fitness_values.index(max(fitness_values))]

    def evolve(self):

        bestCase = [self.population[0], self.fitnessFn(self.population[0])]

        for generation in range(self.nGen):
            print "generation:",generation
            newPopulation = []
            randomSelector = self.rouletteSelection()

            for individual in range(self.nSize):
                parentXX = randomSelector()
                parentXY = randomSelector()
                child = self.crossover(parentXX, parentXY)
                if random.uniform(0, 1) < self.pMutation:
                    child = self.mutation(child)
                newPopulation.append(child)
            self.population = newPopulation[:]

            if self.fitnessThres:
                fittest_individual = self.getFittestIndividual()
                print 'fittest',fittest_individual,'fval:',self.fitnessFn(fittest_individual)

                if self.fitnessFn(fittest_individual) > bestCase[1]:
                    bestCase = [fittest_individual,
                                self.fitnessFn(fittest_individual)]

                if self.fitnessFn(fittest_individual) >= self.fitnessThres:
                    print ("found fittest Individual")
                    return fittest_individual
        
        print '\n\ncompleted {} generations'.format(self.nGen)
        # return getFittestIndividual(population, fitness_fn)
        return bestCase


if __name__ == '__main__':
    GA = geneticAlgorithm()
