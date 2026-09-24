import random

def create_individual(n):
    individual = []

    for row in range(n):
        individual.append(random.randint(0, n - 1))

    return individual


"""
    Use this to make a starter population
    Use create_individual and append to population
"""
def create_population(population_size, n):
    population = []

    for i in range(population_size):
        individual = create_individual(n)
        population.append(individual)


    return population

"""
    - Select (1 - r)p individuals at random using selection()
    - use create_child and append to new population
    - Return new population
"""
def selection(population, max_fitness):
    population_fitness_list = []

    for p in population:
        population_fitness_list.append(calculate_fitness(p, max_fitness))

    """"indices = [i for i in range(len(population_fitness_list)) if i != excluded]
    weights = [fitness_values[i] for i in indices]

    if sum(weights) == 0:
        return random.choice(indices)

    return random.choices(indices, weights=weights, k=1)[0]"""
    return population_fitness_list
    


"""
    
"""
def create_child(parent1, parent2):
    pass


"""
    calculate fitness and return for an individual
"""
def calculate_fitness(individual, max_fitness):
    fitness  = max_fitness
    
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            same_row = individual[i] == individual[j]
            same_diagonal = abs(i - j) == abs(individual[i] - individual[j])

            if same_row or same_diagonal:
                fitness -= 1
    
    return fitness

def mutate(individual, mutation_rate):
    pass

def calculate_max_fitness(n):
    return ((n * (n - 1)) / 2)

def main():
    n = 4
    population_size = 3
    population = create_population(population_size, n)
    print("Population: ", population)
    selection_list = selection(population, calculate_max_fitness(n))
    print("Selection: ", selection(population, calculate_max_fitness(n)))



if __name__ == "__main__":
    main()