import random

class Individual:
    #individuals of population
    #Paths for our problem
    def __init__(self,gene_length,random,path):
        self.fitness = -1
        if random == True:
            self.path = self.generatePathRandom(gene_length)
        else:
            self.path = path

    def generatePathRandom(self,gene_length):
        path = []
        for _ in range(gene_length):
            path.append( random.randint(1,4) )

        return path

    def swap(self,g1,g2):
        self.path[0]
        a, b = self.path.index(g1), self.path.index(g2)
        self.path[b], self.path[a] = self.path[a], self.path[b]


    def setFitness(self,fitness):
        self.fitness = fitness
    
    def toString(self):
        
        result = "Fitness: %f" %self.fitness
        result +="\nPath: "
        for i in range(len(self.path)):
            result+= str(self.path[i])
            result+= " "
        
        return result

class Population:
    #Population of individuals
    def __init__(self,population_size,gene_length,is_random,individuals):
        self.population_size = population_size
        if is_random:
            self.individuals = []
            for _ in range(population_size):
                self.individuals.append( Individual(gene_length,True,[]) )
        else:
            self.individuals = individuals
    
    def addIndividual(self,individual):
        self.individuals.append(individual)

    def removeIndividual(self,individual):
        self.individuals.remove(individual)

    def getIndividualCount(self):
        return len(self.individuals)

    def getFittest(self):
        fittest = self.individuals[0]
        for path in self.individuals:
            if path.fitness > fittest.fitness:
                fittest = path
        
        return fittest
    
    def calculateAverageFitness(self):
        total = 0
        for ind in self.individuals:
            total += ind.fitness

        return total / self.population_size