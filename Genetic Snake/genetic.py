
class Individual:
    #individuals of population
    #Paths for our problem

    def __init__(self,genes):
        assert(len(genes) > 3)
        self.genes = genes
        self.__reset_params()

    def swap(self,g1,g2):
        #swaps two gene for individual
        self.genes[0]
        a, b = self.genes.index(g1),self.genes.index(g2)
        self.genes[b], self.genes[a] = self.genes[a], self.genes[b]
        self.__reset_params()

    def __reset_params(self):
        self.__travel_cost = 0
        self.__fitness = 0


class population:
    #Population of individuals
    def __init__(self,individuals):
        self.individuals = individuals

    @staticmethod
    def gen_individuals(size,genes):
        individuals =[size]
        for _ in range(size):
            individuals.append()