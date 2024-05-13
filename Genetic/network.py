from genetic.utility import randrange, odds, clamp, FloatMatrix
from genetic.config import default_config
from genetic.activation import Activations



class Genome:

    def init_genes(self) -> 'list[float]':
        
        weight_range = (self.config['weight_min'], self.config['weight_max'])
        bias_range = (self.config['bias_min'], self.config["bias_max"])
        genes = []

        # Create weights
        for i in range(len(self.layer_sizes)-1):
            layer_weight_count = self.layer_sizes[i]*self.layer_sizes[i+1]
            for w in range(layer_weight_count):
                genes.append(randrange(weight_range[0],weight_range[1]))

        # Create  biases
        for i in range(len(self.layer_sizes)-1):
            layer_bias_count = self.layer_sizes[i+1]
            for b in range(layer_bias_count):
                genes.append(randrange(bias_range[0], bias_range[1]))

        return genes

    def __init__(self, config : dict, layer_sizes : 'list[int]', genes : 'list[float]' = None) -> 'Genome':
        
        # Init
        self.config = config
        self.layer_sizes = layer_sizes
        self.activation = Activations[config['activation']]
        self.fitness = 0

        # Assign genes
        if genes:
            self.genes = genes
        else:
            self.genes = self.init_genes()

        # Count weights and biases for indexing
        self.bias_count = sum(layer_sizes[1::])
        self.weight_count = len(self.genes)-self.bias_count

    def reset_fitness(self):
        self.fitness = 0

    def get_mutated(self) -> 'Genome':
        
        new_genes = self.genes.copy()
        weight_end_index = self.weight_count-1

        # iterate over genes and apply mutations
        for i,gene in enumerate(new_genes):
            
            # weight
            if i <= weight_end_index:
                # Mutation
                if odds(self.config["weight_mutate_rate"]):
                    new_genes[i] = clamp(gene+self.config['weight_mutate_power']*randrange(-1,1),self.config['weight_min'], self.config['weight_max'])

                # Replacement
                if odds(self.config["weight_replace_rate"]):
                    new_genes[i] = randrange(self.config['weight_min'], self.config['weight_max'])

            # Bias
            else:
                # Mutation
                if odds(self.config["bias_mutate_rate"]):
                    new_genes[i] = clamp(gene+self.config['bias_mutate_power']*randrange(-1,1),self.config['bias_min'], self.config['bias_max'])

                # Replacement
                if odds(self.config["bias_replace_rate"]):
                    new_genes[i] = randrange(self.config['bias_min'], self.config['bias_max'])

        return Genome(self.config, self.layer_sizes, new_genes)

    def get_cross_over(self,other:'Genome') -> 'Genome':
        
        new_genes = self.genes.copy()

        for i in range(len(new_genes)):
            if odds(self.config['cross_over_coefficient']):
                new_genes[i] = other.genes[i]

        return Genome(self.config, self.layer_sizes, new_genes)

    def __str__(self):
        return str(self.genes) 

            


class FeedForwardNetwork:

    def init_weights(self) -> 'list[FloatMatrix]':
        
        start_index = 0
        weight_tensor = []

        for i in range(len(self.layer_sizes)-1):
            from_size, to_size = (self.layer_sizes[i], self.layer_sizes[i+1])
            matrix_size = from_size*to_size
            weight_matrix = FloatMatrix([from_size, to_size])
            weight_matrix.fill_from_linear_source(self.genome.genes,start_index)
            start_index += matrix_size
            weight_tensor.append(weight_matrix)
        
        return weight_tensor

    def init_biases(self) -> 'list[FloatMatrix]':
        
        start_index = self.genome.weight_count
        bias_tensor = []

        for i in range(len(self.layer_sizes)-1):
            layer_size = self.layer_sizes[i+1]
            bias_matrix = FloatMatrix([1,layer_size])
            bias_matrix.fill_from_linear_source(self.genome.genes,start_index)
            start_index += layer_size
            bias_tensor.append(bias_matrix)

        return bias_tensor

    def __init__(self,genome : Genome):
        
        # Grab useful references from genome
        self.genome = genome
        self.layer_sizes = genome.layer_sizes 
        self.activation = genome.activation

        # Initialize parameters from genome
        self.weights = self.init_weights()
        self.biases = self.init_biases()

    def activate(self, inputs : 'list[float]') -> 'list[float]':

        layer_output = FloatMatrix(initial_data=[inputs])

        for i in range(len(self.layer_sizes)-1):

            weights = self.weights[i]
            biases = self.biases[i]

            layer_output *= weights
            layer_output += biases
            layer_output.map_func(self.activation)

        return layer_output.data[0]


# Testing
if __name__ == "__main__":

    print("\nGenome generation test: expecting 6 values")
    test_genome = Genome(default_config, [2,2])
    print(test_genome)

    print("\nGenome weight and bias counting test")
    print('biases',test_genome.bias_count)
    print('weights', test_genome.weight_count)

    print("\nGenome activation test (ReLU)")
    print(test_genome.activation)
    print("A(-5) =", test_genome.activation(-5))
    print("A(10000) =", test_genome.activation(10000))


    print("\nGenome mutation test")
    print("Original", test_genome)
    print("Mutated", test_genome.get_mutated())


    print("\nGenome Cross-over Test")
    gene_donator_genome = Genome(default_config, [2,2])
    print("Original",test_genome)
    print("Gene-Donator",gene_donator_genome)
    print("Result",test_genome.get_cross_over(gene_donator_genome))


    print("\nNetwork Parameter init test")
    test_genome = Genome(default_config, [2,3,2])
    print("Genome: ",test_genome)
    test_network = FeedForwardNetwork(test_genome)
    print("Weights: ")
    [print(matrix,"\n") for matrix in test_network.weights]

    print("Biases: ")
    [print(matrix,"\n") for matrix in test_network.biases]


    print("\nNetwork data parsing test")
    test_genome = Genome(default_config, [2,3,1])
    test_network = FeedForwardNetwork(test_genome)
    inputs = [-0.5,1]
    print("Structure : [2,3,1]")
    print(f"Inputs : {inputs}")
    print(f"Result : {test_network.activate(inputs)}")