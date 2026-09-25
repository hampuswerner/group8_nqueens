import random
import pandas as pd
import matplotlib.pyplot as plt

def generate_table(dataframe):
    _, ax = plt.subplots(figsize=(12, 4))

    ax.axis("off")

    table = ax.table(
        cellText=dataframe.values,
        colLabels=dataframe.columns,
        loc="center",
        cellLoc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    table.auto_set_column_width(col=list(range(len(dataframe.columns))))

    plt.savefig(
        "table.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


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
def selection(population, max_fitness, replacement_rate):
    population_fitness_list = []

    for p in population:
        population_fitness_list.append(calculate_fitness(p, max_fitness))

    indices = [i for i in range(len(population_fitness_list)) if i != None]
    weights = [population_fitness_list[i] for i in indices]

    new_population = []
    # (1 - r)p
    new_population_length = int((1 - replacement_rate) * len(population))

    if sum(weights) == 0:
        return [
            random.choice(population).copy()
            for _ in range(new_population_length)
        ]

    for i in range(new_population_length):
        selected_index = random.choices(indices, weights=weights, k=1)[0]
        new_population.append(population[selected_index].copy())

    return new_population
    

def crossover(parent_1, parent_2):
    point = random.randint(1, len(parent_1) - 1)
    child_1 = parent_1[:point] + parent_2[point:]
    child_2 = parent_2[:point] + parent_1[point:]
    return child_1, child_2


"""
    calculate fitness and return for an individual
"""
def calculate_fitness(individual, max_fitness):
    fitness  = max_fitness
    
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            same_col = individual[i] == individual[j]
            same_diagonal = abs(i - j) == abs(individual[i] - individual[j])

            if same_col or same_diagonal:
                fitness -= 1
    
    return fitness

def mutate(individual):
    position = random.randrange(len(individual))
    new_value = random.randrange(len(individual))

    while new_value == individual[position]:
        new_value = random.randrange(len(individual))

    individual[position] = new_value

def calculate_max_fitness(n):
    return ((n * (n - 1)) // 2)

def current_best_fitness(population, max_fitness):
    current_best_fitness = 0
    for individual in population:
        fitness = calculate_fitness(individual, max_fitness)
        if fitness > current_best_fitness:
            current_best_fitness = fitness

    return current_best_fitness

def find_optimal_solution(population, n):
    max_fitness = calculate_max_fitness(n)
    for individual in population:
        if calculate_fitness(individual, max_fitness) == max_fitness:
            return individual

    return None


def main():
    n = [4, 6, 8, 10, 12] # Board size
    population_size = 1000
    mutation_rate = 0.2
    r = 0.5 # Replacement rate
    results = [] # For table
        
    for i in range(0, len(n)):
        curr_n = n[i]
        max_fitness = calculate_max_fitness(curr_n)
        population = create_population(population_size, curr_n)
        best_fitness = current_best_fitness(population, max_fitness)
        fitness_threshold = calculate_max_fitness(curr_n)

        generation = 0
        max_generation = 10000

        while (best_fitness < fitness_threshold) and generation < max_generation:
            generation += 1

            new_population = selection(population, max_fitness, r)

            parent_pairs = int((r * population_size) / 2)
            for i in range(parent_pairs):
                parent1, parent2 = random.sample(new_population, 2)
                child1, child2 = crossover(parent1, parent2)
                new_population.append(child1)
                new_population.append(child2)

            mutation_amount = int(mutation_rate * len(new_population))
            for i in range(mutation_amount):
                mutate(random.choice(new_population))

            population = new_population

            best_fitness = current_best_fitness(population, max_fitness)


        solution = find_optimal_solution(population, curr_n)
        results.append({
            "N": curr_n,
            "Population Size": population_size,
            "Mutation Rate": mutation_rate,
            "Replacement Rate": r,
            "Generations": generation,
            "Best Fitness": best_fitness,
            "Max Fitness": max_fitness,
            "Success": solution is not None
        })

        if solution is not None:
            print(f"Optimal solution: {solution} for N = {curr_n}")
        else:
            print(
                f"Didn't find optimal solution for N={curr_n} "
                f"in {generation} generations. "
                f"Best fitness: {best_fitness}/{max_fitness}"
            )

    df = pd.DataFrame(results)
    generate_table(df)
            



if __name__ == "__main__":
    main()