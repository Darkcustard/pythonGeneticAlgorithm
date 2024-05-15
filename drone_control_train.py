import pygame
import genetic

# Window
resolution = pygame.Vector2(1000,1000)
window = pygame.display.set_mode(resolution)

# Genetic algorithm
config = genetic.load_config('drone_config.txt')
population = genetic.Population(config, [6,20,20,20,4])


# Evaluator
def evaluate_genomes(genomes, networks):

    # Init
    clock = pygame.time.Clock()
    time = 0
    max_time = 30









    while time < max_time:


        # Tickwise
        dt = clock.tick(60)/1000
        time += dt
        window.fill((0,125,125))










        # Check quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()



        pygame.display.update()