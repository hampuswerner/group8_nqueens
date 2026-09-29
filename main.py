import random
import pandas as pd
import matplotlib.pyplot as plt
import time

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

def create_permutation_individual(n):
    return random.sample(range(n), n)


"""
    Use this to make a starter population
    Use create_individual and append to population
"""
def create_population(population_size, n, permutation):
    population = []

    for i in range(population_size):
        if permutation:
            individual = create_permutation_individual(n)
        else:
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
    

def single_point_crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    child1 = repair_permutation(child1)
    child2 = repair_permutation(child2)

    return child1, child2

def uniform_crossover(parent1, parent2):
    child1 = []
    child2 = []

    for i in range(len(parent1)):
        if random.random() < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])

    child1 = repair_permutation(child1)
    child2 = repair_permutation(child2)

    return child1, child2

def partially_mapped_crossover(parent1, parent2):
    point1, point2 = sorted(random.sample(range(len(parent1)), 2))

    child1 = [None] * len(parent1)
    child2 = [None] * len(parent2)

    child1[point1:point2] = parent1[point1:point2]
    child2[point1:point2] = parent2[point1:point2]

    for i in range(len(parent1)):
        if point1 <= i < point2:
            continue

        value = parent2[i]

        while value in child1[point1:point2]:
            index = parent1.index(value)
            value = parent2[index]

        child1[i] = value

    for i in range(len(parent2)):
        if point1 <= i < point2:
            continue

        value = parent1[i]

        while value in child2[point1:point2]:
            index = parent2.index(value)
            value = parent1[index]
        
        child2[i] = value

    return child1, child2

def order_crossover(parent1, parent2):
    point1, point2 = sorted(random.sample(range(len(parent1)), 2))

    child1 = [None] * len(parent1)
    child2 = [None] * len(parent2)

    child1[point1:point2] = parent1[point1:point2]
    child2[point1:point2] = parent2[point1:point2]

    order1 = parent2[point2:] + parent2[:point2]
    order2 = parent1[point2:] + parent1[:point2]

    # Remove values that is already in the children
    remaining1 = [value for value in order1 if value not in child1]
    remaining2 = [value for value in order2 if value not in child2]

    positions = list(range(point2, len(parent2))) + list(range(0, point1))

    for i, position in enumerate(positions):
        child1[position] = remaining1[i]
        child2[position] = remaining2[i]

    return child1, child2



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

def mutate(individual, permutation):

    if permutation:
        position1, position2 = random.sample(range(len(individual)), 2)
        
        individual[position1], individual[position2] = (individual[position2], individual[position1])
    else:
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

def repair_permutation(individual):
    missing = []

    for value in range(len(individual)):
        if value not in individual:
            missing.append(value)

    seen = set()
    duplicate_positions = []

    for i in range(len(individual)):
        if individual[i] in seen:
            duplicate_positions.append(i)
        else:
            seen.add(individual[i])

    for i in range(len(duplicate_positions)):
        position = duplicate_positions[i]
        individual[position] = missing[i]

    return individual


def main():
    n = [8, 10, 12, 14, 16, 18, 20] # Number of queens / Board size
    population_size = 300
    mutation_rate = 0.2
    r = 0.4 # Replacement rate
    results = [] # For table
    permutation = True
    max_generation = 30000
    runs = 30
        
    for curr_n in n:
        
        max_fitness = calculate_max_fitness(curr_n)
        successful_generation_results = []
        time_results = []
        generation_results = []
        fitness_results = []
        successes = 0

        for run in range(runs):
            random.seed(run)
            start_time = time.perf_counter()
            population = create_population(population_size, curr_n, permutation)
            best_fitness = current_best_fitness(population, max_fitness)
            generation = 0

            while best_fitness < max_fitness and generation < max_generation:
                generation += 1

                new_population = selection(population, max_fitness, r)

                parent_pairs = int((r * population_size) / 2)
                for _ in range(parent_pairs):
                    parent1, parent2 = random.sample(new_population, 2)
                    child1, child2 = single_point_crossover(parent1, parent2)
                    assert sorted(child1) == list(range(curr_n))
                    assert sorted(child2) == list(range(curr_n))
                    new_population.append(child1)
                    new_population.append(child2)

                mutation_amount = int(mutation_rate * len(new_population))
                for _ in range(mutation_amount):
                    mutate(random.choice(new_population), permutation)

                population = new_population

                best_fitness = current_best_fitness(population, max_fitness)

            end_time = time.perf_counter()
            execution_time = end_time - start_time

            solution = find_optimal_solution(population, curr_n)

            generation_results.append(generation)
            time_results.append(execution_time)
            fitness_results.append(best_fitness)

            if solution is not None:
                successes += 1
                successful_generation_results.append(generation)
            
            print(
                f"N={curr_n} | "
                f"Run {run + 1}/{runs} | "
                f"Generations={generation} | "
                f"Best fitness={best_fitness}/{max_fitness} | "
                f"Success={solution is not None}"
            )

        average_generations = (sum(generation_results) / len(generation_results))
        average_time = (sum(time_results) / len(time_results))
        average_fitness = (sum(fitness_results) / len(fitness_results))
        success_rate = (successes / runs) * 100

        if successful_generation_results:
            average_successful_generations = (sum(successful_generation_results) / len(successful_generation_results))
        else:
            average_successful_generations = None

        results.append({
            "N": curr_n,
            "Runs": runs,
            "Population Size": population_size,
            "Mutation Rate": mutation_rate,
            "Replacement Rate": r,
            "Avg Generations": round(average_generations, 2),
            "Avg Successful Generations":
                round(average_successful_generations, 2)
                if average_successful_generations is not None
                else "N/A",
            "Avg Time (s)": round(average_time, 3),
            "Avg Best Fitness": round(average_fitness, 2),
            "Max Fitness": max_fitness,
            "Success Rate (%)": round(success_rate, 1)
        })

    df = pd.DataFrame(results)
    generate_table(df)
            



if __name__ == "__main__":
    main()