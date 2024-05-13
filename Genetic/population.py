from genetic.network import Genome, FeedForwardNetwork, default_config
from genetic.utility import odds
from random import choice

class Population:

    def __init__(self,config, structure : 'list[int]'):
        self.config = config
        self.structure = structure
        self.genomes = [Genome(config, structure) for i in range(self.config['population_size'])]

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
                    new_genome = self.genomes[i].get_mutated()

                    # Cross-over
                    if i != 0 and odds(self.config["cross_over_chance"]):
                        cross_over_genome = choice(self.genomes[0:i])
                        new_genome = new_genome.get_cross_over(cross_over_genome)

                    new_genomes.append(new_genome)

        self.genomes.extend(new_genomes)
        self.genomes = self.genomes[0:self.config["population_size"]]

    def report(self):

        fitnesses = [genome.fitness for genome in self.genomes]
        avg = sum(fitnesses)/len(fitnesses)
        stddev = sum([abs(fitness-avg) for fitness in fitnesses])/len(fitnesses)

        #print(f"Population size : {len(fitnesses)}")
        print(f"Best fitness: {max(fitnesses)}")
        print(f"Average fitness: {avg}")
        print(f"Standard deviation: {stddev}")

    def evolve(self, evaluator_function, generations : int, report_interval = 1) -> Genome:

        for generation in range(generations):
            
            # Reporting
            print(f"\nRunning generation: {generation+1}\n------------------------------------------")

            # Reset fitness and create networks
            [genome.reset_fitness() for genome in self.genomes]
            networks = [FeedForwardNetwork(genome) for genome in self.genomes]

            # Evaluate networks
            evaluator_function(self.genomes,networks)

            if generation % report_interval == 0:
                self.report()

            # rank, kill and regenerate
            self.genomes.sort(key=lambda x : x.fitness, reverse=True)
            self.kill_genomes()
            self.regenerate_genomes()

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



