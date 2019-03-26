import argparse
from datetime import datetime
import random
import numpy as np
import time

#total generations
#average fitness
#total population
#mutaiton rate

def run(args):

    

    startX = args.startx
    startY = args.starty
    foodCount = args.food_count
    world = generateWorld(args.world_size)

    gene_length = int(args.world_size*args.food_count*0.6)#aka chromosome length (0.6 is random)

    #Generating the Population
    population = []
    for i in range(args.population_size):
        population.append(generatePathRandom(gene_length))
    
    population_finess_values = []
    total_fitness = 0
    max_fitness = 0
    max_fitness_index = 0
    
    for i in range(args.population_size):
        fit = fitness(world,population[i],startX,startY,foodCount)
        population_finess_values.append(fit)
        total_fitness += fit
        if fit > max_fitness : 
            max_fitness = fit
            max_fitness_index = i

    avg_fitness = total_fitness / args.population_size
    

    total_generations = 0

    start_time = time.time()
    elapsed_time = 0

    while elapsed_time > args.duration :## or  avg_fitness >= 2 : #### or enough fit individiual found
        elapsed_time = (time.time() - start_time)##this is as seconds
        total_generations +=1
        #new_population <- empty set
        new_population = []
        for i in range(args.population_size):

           # x = fitness(ma)

            if random.random() < args.mut_rate:
                i=2
              #  mutate(child)

def generateWorld(N = 10,foodCount= 5):

    world = np.zeros( shape=(N,N) )

    food_positions = []

    for _ in range(foodCount):
        food = [random.randint(0,N-1),random.randint(0,N-1)]
        food_positions.append(food)
        world[food[0],food[1]] = 1

    return world

def generatePathRandom(gene_length):
    path = []
    for i in range(gene_length):
        path.append( random.randint(1,4) )

    return path

def mutate(child):
    i = 2

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

def fitness(world,path,startX,startY,foodCount):
    #Return fitness value for path parameter
    #min:0, max:2
    total_path = len(path)
    world_size = len(world[0])

    posX = startX
    posY = startY   

    total_food_count = foodCount
    #food_eaten = 0
    eaten_foods = []

    result = -1
    for i in range(len(path)):

        posX,posY = proceed(posX,posY,path[i])

        collision = checkCollision(world,world_size,eaten_foods,posX,posY) 

        if collision == 0:#no collision
            continue

        elif collision > 0:#collided with food

            if(len(eaten_foods) == foodCount):#eaten all food
                #fitness = food_eaten/total_food_count + i/total_path !!! can it be enhanced ???
                result = 1 + i/total_path
                break
                
        else :# collision < 0 collided with wall ## min:0, max:2
            result = len(eaten_foods)/total_food_count + i/total_path
            break

    if(result == -1):
        result = len(eaten_foods)/total_food_count + 1

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--world_size",type=int,default=11)
    parser.add_argument("--food_count",type=int,default=5)
    parser.add_argument("--population_size",type=int,default=100)
    parser.add_argument('--mut_rate', type=float, default=0.02, help='Mutation rate')
    parser.add_argument('--n_gen', type=int, default=20, help='Number of equal generations before stopping')
    parser.add_argument("--startx",type=int,default=5,help='start position x')
    parser.add_argument("--starty",type=int,default=5,help='start position y')
    parser.add_argument("--duration",type=int,default=5,help='waiting time')


    random.seed(datetime.now())

    args = parser.parse_args()

    run(args)