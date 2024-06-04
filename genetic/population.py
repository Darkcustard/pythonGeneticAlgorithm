from genetic.network import Genome, FeedForwardNetwork, default_config
from genetic.utility import odds
from  genetic.persist import save_genome
from random import choice, seed

class Population:

    def __init__(self,config, structure : 'list[int]'):
        self.config = config
        self.structure = structure
        self.genomes = [Genome(config, structure) for i in range(self.config['population_size'])]
        self.stagnation = 0

    def kill_genomes(self):

        surviving_genomes = []
        for i in range(len(self.genomes)):
            
            # Ignore top networks
            # if i <= self.config['elitism']:
            #     continue
            
            # Calculate survival odds
            rank = i/(len(self.genomes)-1)
            survival_probability = -rank/(2*self.config['survival_rate']) + 1
            if odds(survival_probability): surviving_genomes.append(self.genomes[i])

        self.genomes = surviving_genomes

    def regenerate_genomes(self):

        new_genomes = []
        quota = self.config['population_size']-len(self.genomes)

        while len(new_genomes) < quota:
            for i in range(len(self.genomes)):
                
                # Better genomes are more likely to reproduce
                rank = i/(len(self.genomes)-1)
                reproduction_probability = -rank/(2*self.config['survival_rate']) + 1
                
                # Specific genome reproduces
                if odds(reproduction_probability):

                    # Create child genome
                    new_genome = self.genomes[i].copy()

                    # Cross-over
                    if odds(self.config["cross_over_chance"]):
                        cross_over_genome = choice(self.genomes)
                        new_genome = new_genome.get_cross_over(cross_over_genome)

                    # Mutations
                    new_genome = new_genome.get_mutated()

                    new_genomes.append(new_genome)

        self.genomes.extend(new_genomes)
        self.genomes = self.genomes[0:self.config["population_size"]]

    def calculate_metrics(self, report : bool ):

        self.fitnesses = [genome.fitness for genome in self.genomes]
        self.avg = sum(self.fitnesses)/len(self.fitnesses)
        self.stddev = sum([abs(fitness-self.avg) for fitness in self.fitnesses])/len(self.fitnesses)

        if report:
            print(f"Best fitness: {max(self.fitnesses)}")
            print(f"Average fitness: {self.avg}")
            print(f"Standard deviation: {self.stddev}")
            print(f"Stagnation : {self.stagnation}/{self.config['max_stagnation']} | Target : {self.best_average}")


    def evolve(self, evaluator_function, generations : int, report_interval = 1) -> Genome:

        self.best_average = None
        self.stagnation = 0
        generation = 0

        while generation < generations:
            
            # Reporting
            print(f"\nRunning generation: {generation+1}\n------------------------------------------")

            # Reset fitness and create networks
            [genome.reset_fitness() for genome in self.genomes]
            networks = [FeedForwardNetwork(genome) for genome in self.genomes]

            # Evaluate networks
            evaluator_function(self.genomes,networks)
            
            # Calculate metrics and report
            self.calculate_metrics(generation % report_interval == 0)

            # Calculate stagnation
            if self.best_average != None:
                if self.avg <= self.best_average:
                    self.stagnation += 1
                else: self.stagnation = 0; self.best_average = self.avg
            else: self.best_average = self.avg

            # Check max stagnation reached
            if self.stagnation > self.config['max_stagnation']:
                print(f"Max Stagnation reached. Resetting population.")
                self.stagnation = 0
                generation = 0
                self.genomes = [Genome(self.config, self.structure) for i in range(self.config['population_size'])]
                continue

            # rank, kill and regenerate
            self.genomes.sort(key=lambda x : x.fitness, reverse=True)
            self.kill_genomes()
            self.regenerate_genomes()

            generation += 1

        return self.genomes[0]

# Testing
if __name__ == "__main__":


    # XOR test
    config = default_config
    population = Population(config, [2,4,1])
    
    def evaluate(genomes, networks):

        x = [[1,0],[0,1],[1,1],[0,0]]
        y = [1,1,0,0]

        for i in range(len(genomes)):
            
            # Fetch genome and network
            genome = genomes[i]
            network = networks[i]

            # evaluate for each example
            for j in range(len(x)):

                sx = x[j]
                sy = y[j]

                # MSE
                result = network.activate(sx)[0]
                loss = (result-sy)**2
                genome.fitness -= loss

    winner = population.evolve(evaluate,1000,10)
    winning_network = FeedForwardNetwork(winner)

    print(winning_network.activate([0,1]))
    print(winning_network.activate([1,0]))
    print(winning_network.activate([1,1]))
    print(winning_network.activate([0,0]))



