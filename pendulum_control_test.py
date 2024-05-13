import genetic
import pygame
from math import atan2

# Window
resolution = pygame.Vector2(1000,500)
window = pygame.display.set_mode(resolution)

# Genetic algo init
config = genetic.load_config('./pendulum_config.txt')
population = genetic.Population(config, [3,6,2])

# Utility
def get_ang(vec : pygame.Vector2) -> float:
    return atan2(vec.y, vec.x)


# Define evaluator

def eval_genomes(genomes, networks):

    # Init gamevar
    clock = pygame.time.Clock()
    time = 0
    half_track = resolution.x / 2.0
    half_height = resolution.y / 2.0
    population_size = len(networks)
    pole_length = 100
    trolley_speed = 600


    # Define positions (Verlet)
    trolley_positions = [pygame.Vector2(half_track, half_height) for i in range(population_size)]
    pole_positions = [pygame.Vector2(half_track,half_height+100) for i in range(population_size)]
    pole_positions_last = [pygame.Vector2(half_track,half_height+100) for i in range(population_size)]


    while time < 5:

        # Per game-loop basis
        dt = clock.tick(60)/100000
        window.fill((0,0,0))
        time += dt
        pygame.draw.line(window, (255,255,255), pygame.Vector2(0,half_height), pygame.Vector2(resolution.x, half_height),2)



        # Per genome basis
        for i in range(population_size):

            # get related var
            genome = genomes[i]
            network = networks[i]
            trolley_position = trolley_positions[i]
            pole_position = pole_positions[i]
            pole_position_last = pole_positions_last[i]

            # Calculate angles
            current_ang = get_ang(pole_position-trolley_position)
            last_ang = get_ang(pole_position_last-trolley_position)
            angvel = (current_ang-last_ang)/dt

            # Query network
            inputs = [current_ang, angvel, (trolley_position.x-half_track)/half_track]
            outputs = network.activate(inputs)
            choice = outputs.index(max(outputs))
            moves = [pygame.Vector2(-1,0), pygame.Vector2(1,0)]
            trolley_position += moves[choice]*dt*trolley_speed

            # Enforce constraints
            to_pole = pole_position-trolley_position
            distance = to_pole.magnitude()
            if distance != pole_length and distance != 0:
                to_pole = to_pole.normalize()
                delta = pole_length-distance
                pole_position+=delta*to_pole

            # Draw
            pygame.draw.line(window, (255,255,255), pole_position, trolley_position, 1)
            pygame.draw.circle(window, (0,255,255), pole_position, 10)
            pygame.draw.circle(window, (0,0,255), trolley_position, 20)


            # Enforce verlet
            vel = pole_position-pole_position_last
            pole_position_last = pole_position.copy()
            pole_position += vel
            #pole_position.y += 0*dt




            # fitness
            genome.fitness += (trolley_position.y-pole_position.y)*dt
            genome.fitness -= abs(trolley_position.x-half_track)*dt

















        # Check quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()




best_genome = population.evolve(eval_genomes, 100)