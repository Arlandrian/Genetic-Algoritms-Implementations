import argparse
from datetime import datetime
from random import random,sample,randint
import numpy as np
import time
import copy
import random
import math

import matplotlib.pyplot as plt
import matplotlib.colors as colors

from genetic import Individual,Population

#total generations
#average fitness
#total population
#mutaiton rate

class World:
    def __init__(self,world_size,startX,startY,foodCount,muta_rate):
        self.world_size = world_size
        self.startX =startX
        self.startY = startY
        self.foodCount = foodCount
        self.mutation_rate = muta_rate
        self.gene_length = math.floor(world_size*foodCount*1.5)#aka chromosome length
        self.map = self.generateWorld()
    
    #Generates world and places foods
    def generateWorld(self):
        N = self.world_size
        world = np.zeros( shape=(N,N) )

        food_positions = []

        for _ in range(self.foodCount):
            food = [random.randint(0,N-1),random.randint(0,N-1)]
            while food in food_positions:
                food = [random.randint(0,N-1),random.randint(0,N-1)]
            food_positions.append(food)
            world[food[0],food[1]] = 1

        return world

def run(args):

    startX = args.startx
    startY = args.starty
    foodCount = args.food_count

    world = World(args.world_size,args.startx,args.starty,args.food_count,args.mut_rate)

    #Generating the Population
    population = Population(args.population_size,world.gene_length,True,[])

    start_time = time.time()
    elapsed_time = 0
    
    total_fitness = 0
    max_fitness = 0
    max_fitness_index = 0
    i=0
    for individual in population.individuals:
        fit = fitnessFN(world,individual.path,startX,startY,foodCount)
        individual.setFitness(fit)
        total_fitness += fit
        if fit > max_fitness : 
            max_fitness = fit
            max_fitness_index = i
        i+=1

    best_individual = copy.copy(population.individuals[max_fitness_index])

    avg_fitness = total_fitness / population.population_size
    

    total_generations = args.max_generation_number
    generation_counter = 0

    while generation_counter < total_generations and best_individual.fitness < world.foodCount:
        print("Generation : ",generation_counter)
        print("Max fitness: ",best_individual.fitness)
        print("Average fitness: ",avg_fitness)
        population = evolve(world,population)
        new_best_individual = population.getFittest()
        avg_fitness = population.calculateAverageFitness()

        if new_best_individual.fitness > best_individual.fitness:
            generation_counter,best_individual = 0,new_best_individual
        else:
            generation_counter += 1
        

    total_generations = 0

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\n-------------------------------\nElapsed Time: ",elapsed_time," sec")
    print("Population Size: ",args.population_size," World Size: ",args.world_size,"\nStart x, y:",args.startx,",",args.starty," Food Count: ",args.food_count,"\nMutation Rate: ",args.mut_rate)

    print("Result: ",best_individual.toString())
    
    matrix = traverse(best_individual.path,world)
    draw_matrix(matrix,'title')


    
    
def traverse(path, world:World):
    matrix = [[0 for a in range(world.world_size)] for b in range(world.world_size)]
    x,y = world.startX,world.startY

    eaten_foods = []
    matrix[x][y] = 0.22
    for i in range(len(path)):
        x,y = proceed(x,y,path[i])

        collision = checkCollision(world.map,world.world_size,eaten_foods,x,y) 

        if collision == 0:#no collision
            matrix[x][y] = 0.55

        elif collision > 0:#collided with food
            None
            #matrix[x][y] = 1
                
        else :# collision < 0 collided with wall
            if x == world.world_size:
                matrix[x-1][y] = 0.77
            if y == world.world_size:
                matrix[x][y-1] = 0.77
            break

    x,y = world.startX,world.startY
    matrix[x][y] = 0.22
    for i in range(len(eaten_foods)):
        matrix[eaten_foods[i][0]][eaten_foods[i][1]] = 1

    return matrix

def draw_matrix(matrix, title=''):
    cmap = colors.ListedColormap(['white','black', 'red', 'green'])
    bounds = [0, 0.2,0.5,0.7, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    plt.matshow(matrix, cmap=cmap, norm=norm, interpolation='none', vmin=0, vmax=4)
    plt.title(title)
    plt.xticks(range(len(matrix[0])))
    plt.yticks(range(len(matrix[0])))
    
    plt.show()

def generatePathRandom(gene_length):
    path = []
    for i in range(gene_length):
        path.append( random.randint(1,4) )

    return path

def proceed(posX,posY,direction):
        if direction == 1:#right
            posX += 1
        elif direction == 2:#up
            posY +=1
        elif direction == 3:#left
            posX -=1
        else :#down
            posY -=1
        return posX,posY
                
def checkCollision(world,world_size,eaten_foods,posX,posY):
    #check if collided with wall
    if posX >= world_size or posY >= world_size or posX < 0 or posY < 0:
        return -1
    #check if collided with food
    if world[posX][posY] == 1 and (posX,posY) not in eaten_foods:
        eaten_foods.append((posX,posY)) 
        return 1
    
    return 0

def fitnessFN(world,path,startX,startY,foodCount):
    #Return fitness value for path parameter
    #min:0, max:2
    total_path = len(path)
    world_size = world.world_size

    posX = startX
    posY = startY   

    total_food_count = foodCount
    #food_eaten = 0
    eaten_foods = []

    result = -1
    for i in range(len(path)):

        posX,posY = proceed(posX,posY,path[i])

        collision = checkCollision(world.map,world_size,eaten_foods,posX,posY) 

        if collision == 0:#no collision
            continue

        elif collision > 0:#collided with food

            if(len(eaten_foods) == foodCount):#eaten all food
                #fitness = food_eaten/total_food_count + i/total_path !!! can it be enhanced ???
                result = foodCount
                break
                
        else :# collision < 0 collided with wall ## min:0, max:2
            result = len(eaten_foods)##/total_food_count + i/total_path - 1
            break

    if(result == -1):
        result = len(eaten_foods)##/total_food_count + 1

    return result

def evolve(world :World, population:Population):

    new_generation = Population(population.population_size,world.gene_length,False,[])
    elitism_number = population.population_size//2

    #Elitism
    for _ in range(elitism_number):
        fittest = population.getFittest()
        new_generation.addIndividual(fittest)
        population.removeIndividual(fittest)

    #Crossover
    for _ in range(elitism_number,population.population_size):
        parent1 = selection(new_generation,world)
        parent2 = selection(new_generation,world)
        child = crossover(parent1,parent2)
        child.setFitness(fitnessFN(world,child.path,world.startX,world.startY,world.foodCount))
        new_generation.addIndividual(child)

    #Mutation
    for i in range(elitism_number,population.population_size):
        mutation(new_generation.individuals[i],world.mutation_rate)
    
    return new_generation

#select n number individual randomly and get fittest amoung them
def selection(population:Population, world:World):
    besafe=0
    while besafe < 10000:
        index  = randint(0,len(population.individuals)-1)
        partner =  population.individuals[index]
        r = random.randint(0,world.foodCount)#############BURAYA bi daha bak

        if r < partner.fitness:
            return partner

        besafe+=1

    index  = randint(0,len(population.individuals)-1)
    partner =  population.individuals[index]
    return partner
   ## return Population(population.population_size,world.gene_length,False,sample(population.individuals,competitors_n)).getFittest()

def crossover(parent1,parent2):

    path_n = len(parent1.path)

    mid = randint(0,path_n-1)  
    child = Individual(path_n,False,[None for _ in range(path_n)])

    for i in range(0, mid):
            child.path[i] = parent1.path[i]

    for i in range(mid, path_n):
            child.path[i] = parent2.path[i]

    return child

def mutation(individual:Individual, mut_rate):
    if random.random() < mut_rate:
        mutate(individual.path)

def mutate(path):
    number_of_mutation = randint(0,len(path)//3)
    for _ in range(number_of_mutation):
        path[randint(0,len(path)-1)] = randint(1,4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--world_size",type=int,default=17)
    parser.add_argument("--food_count",type=int,default=10)
    parser.add_argument("--population_size",type=int,default=200)
    parser.add_argument('--mut_rate', type=float, default=0.2, help='Mutation rate')
    parser.add_argument('--n_gen', type=int, default=20, help='Number of equal generations before stopping')
    parser.add_argument("--startx",type=int,default=5,help='start position x')
    parser.add_argument("--starty",type=int,default=5,help='start position y')
    parser.add_argument("--duration",type=int,default=500,help='waiting time')
    parser.add_argument("--max_generation_number",type=int,default=450,help='Max generation number for stop')


    #random.seed(datetime.now())

    args = parser.parse_args()

    run(args)