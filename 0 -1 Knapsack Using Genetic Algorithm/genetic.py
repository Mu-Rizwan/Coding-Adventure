import random

class Chromosome:    
    def __init__(self, genes, knapsack):
        self.genes = list(genes)
        self.fitness = self.calculate_fitness(knapsack)

    def calculate_fitness(self, knapsack):
        fitness = 0
        ## Implement fitness function ##
        weight_limit = 20
        total_weight = 0
        total_worth = 0
        for i in range(len(self.genes)):
            if self.genes[i] == 1:
                total_worth += knapsack[i][0]
                total_weight += knapsack[i][1]
                
        if total_weight <= weight_limit:
            if total_worth > 0:
                ratio = total_weight / total_worth
                fitness = round(total_worth - ratio,2)
            else:
                fitness = 0
        else:
            fitness = 0
        return fitness

    def __str__(self):
        return f"Fitness: {self.fitness}, Chromosome: {self.genes}"

class GeneticAlgorithm:
    def __init__(self, weight_limit, knapsack, population_size, mutation_rate):
        self.weight_limit = weight_limit
        self.knapsack = knapsack
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def initialize_population(self):
        #Initialize a population with random gene sequences#
        population = []
        ##Implement your logic##
        for i in range(self.population_size):
            genes = [random.randint(0, 1) for j in range(len(self.knapsack))]
            chromosome = Chromosome(genes, self.knapsack)
            population.append(chromosome)
        return population

    def selection(self):
        #Use elitishm and roulette-wheel to select chromosomes#
        elite_count = 3
        selected = []
        population = self.population[:]
        ##Implement your logic##
        sorted_indices = sorted(range(self.population_size), key=lambda i: population[i].fitness, reverse=True)
        elites = [population[i] for i in sorted_indices[:elite_count]]
        selected.extend(elites)
        
        population = [population[i] for i in range(self.population_size) if i not in sorted_indices[:elite_count]]
        total_fitness = sum([c.fitness for c in population])
        probabilities = [c.fitness / total_fitness if total_fitness > 0 else 0 for c in population]
        remaining_count = len(self.population) - elite_count
        for _ in range(remaining_count):
            pick = random.random()
            cumulative = 0
            for i, prob in enumerate(probabilities):
                cumulative += prob
                if pick <= cumulative:
                    selected.append(population[i])
                    break
        return selected

    def crossover(self, parent1, parent2):
        #Perform single-point crossover to create new offsprings#
        crossover_point = len(parent1.genes) // 2
        c1_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
        c2_genes = parent2.genes[:crossover_point] + parent1.genes[crossover_point:]
        ##Generate and return child 1 and child 2##
        child1, child2 = Chromosome(c1_genes, self.knapsack), Chromosome(c2_genes, self.knapsack)
        return child1, child2

    def mutation(self, chromosome):
        #Mutate genes of a chromosome#
        no_of_mutations = int(self.mutation_rate * len(chromosome.genes))
        mutation_indices = random.sample(range(len(chromosome.genes)), no_of_mutations)
        for index in mutation_indices:
            chromosome.genes[index] = 1 - chromosome.genes[index]
        chromosome.fitness = chromosome.calculate_fitness(self.knapsack)
        return chromosome

    def evolve(self):
        ##Evolve and generate new population#
        new_population = []
        selected_parents = self.selection()
        for i in range(0, len(selected_parents), 2):
            if i + 1 < len(selected_parents):
                parent1 = selected_parents[i]
                parent2 = selected_parents[i + 1]

                offspring1, offspring2 = self.crossover(parent1, parent2)
                offspring1 = self.mutation(offspring1)
                offspring2 = self.mutation(offspring2)

                new_population.append(offspring1)
                new_population.append(offspring2)

        self.population = new_population

    def get_solution(self):
        #Fetch the best solution on the basis of fitness#
        return max(self.population, key=lambda c: c.calculate_fitness(self.knapsack))

def build_knapsack(file):
    #Read from test case and build knapsack as a dictionary"
    w = None
    knapsack = dict()
    with open(file,"r") as data:
        lines = data.readlines()
        items, w = map(int, lines[0].strip().split())
        for i in range(1,items+1):
            worth, weight = map(int, lines[i].strip().split())
            knapsack[i-1] = (worth, weight)
    return w, knapsack

if __name__ == "__main__":
    w, knapsack = build_knapsack("test.txt")
    print(f"items: {len(knapsack)}")
    print(f"weight_limit: {w}")
    print(f"knapsack: {knapsack}")
    ga = GeneticAlgorithm(w, knapsack, population_size=10, mutation_rate=0.2)
    print("Initial population:")
    for i in range(ga.population_size):
        print(ga.population[i])
    
    for _ in range(60):
        ga.evolve()
    
    best_solution = ga.get_solution()
    print("Best solution found:", best_solution)
    print("Fitness of best solution:", best_solution.calculate_fitness(knapsack))
