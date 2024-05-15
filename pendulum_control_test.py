import genetic
import pygame
from math import atan2, sin
from random import random

import genetic.utility

# Window
resolution = pygame.Vector2(1000,300)
window = pygame.display.set_mode(resolution)
pygame.display.set_caption("Cart-Pendulum Test")

# Genetic algo ini
config = genetic.load_config('./pendulum_config.txt')
population = genetic.Population(config, [4,10,10,10,2])

# Utility
def get_ang(vec : pygame.Vector2) -> float:
    return atan2(vec.y, vec.x) + 1.5707963267948966

# Define evaluator

def eval_genomes(genomes, networks):

    # Init gamevar
    clock = pygame.time.Clock()
    time = 0
    track_size = 600
    half_pit = (resolution.x - track_size)/2

    half_resolution = resolution.x/2
    half_track = track_size / 2.0
    half_height = resolution.y / 2.0
    population_size = len(networks)
    pole_length = 100
    trolley_speed = 20



    # Define positions (Verlet)
    trolley_positions = [pygame.Vector2(half_resolution, half_height) for i in range(population_size)]
    trolley_collided = [False for i in range(population_size)]
    trolley_positions_last = [pygame.Vector2(half_resolution, half_height) for i in range(population_size)]


    pole_positions = [pygame.Vector2(half_resolution,half_height-100) for i in range(population_size)]
    pole_positions_last = [pygame.Vector2(half_resolution,half_height-100) for i in range(population_size)]


    while time < 20:

        # Per game-loop basis
        dt = clock.tick(60)/500
        window.fill((0,0,0))
        time += dt
        pygame.draw.line(window, (255,255,255), pygame.Vector2(half_pit,half_height), pygame.Vector2(resolution.x-half_pit, half_height),2)
        fitnesses = [genome.fitness for genome in genomes]
        best_genome_index = fitnesses.index(max(fitnesses))


        # Per genome basis
        for i in range(population_size):

            # get related var
            genome = genomes[i]
            network = networks[i]
            trolley_position = trolley_positions[i]
            trolley_position_last = trolley_positions_last[i]
            pole_position = pole_positions[i]
            pole_position_last = pole_positions_last[i]
            

            # Calculate angles
            current_ang = get_ang(pole_position-trolley_position)
            last_ang = get_ang(pole_position_last-trolley_position)
            angvel = (current_ang-last_ang)/dt



            # Enforce verlet pole
            pole_vel = pole_position-pole_position_last
            pole_positions_last[i] = pole_position.copy()
            pole_positions[i] += pole_vel
            pole_position.y += 10*dt

            if genetic.utility.odds(0.001):
                pole_position.x += (random()*10-5)

            # Enforce verlet trolley
            trolley_vel = trolley_position-trolley_position_last
            trolley_positions_last[i] = trolley_position.copy()
            trolley_positions[i] += trolley_vel


            # Enforce constraints
            distance = pole_position.distance_to(trolley_position)
            if distance != pole_length and distance != 0:
                to_pole = (pole_position-trolley_position).normalize()
                delta = pole_length-distance
                pole_position+=delta*to_pole

            all_dead = True
            for status in trolley_collided:
                if not status:
                    all_dead = False
            if all_dead:
                time = 9999

            # Query network and fitness
            if not trolley_collided[i]:

                # Slide off track
                if trolley_position.x < half_pit:
                    trolley_collided[i] = True
                if trolley_position.x > resolution.x-half_pit:
                    trolley_collided[i] = True
                if pole_position.y > half_height:
                    trolley_collided[i] = True

                inputs = [current_ang, angvel, (trolley_position.x-half_resolution)/(half_track), trolley_vel.x]
                outputs = network.activate(inputs)
                choice = outputs.index(max(outputs))
                moves = [pygame.Vector2(-1,0), pygame.Vector2(1,0)]
                trolley_positions[i] += moves[choice]*dt*trolley_speed

                # Fitness
                height = (trolley_position.y+pole_length)-pole_position.y
                distance = max(1,abs(trolley_position.x-half_resolution))
                trolley_velocity_magnitude = max(1,abs(trolley_vel.x))
                pole_velocity_magnitude = max(1,abs(angvel))
                
                genome.fitness += (height/(distance**0.5))*dt
            else:
                trolley_positions[i].y += 10*dt

            
            # Draw
            if i == best_genome_index:
                pygame.draw.line(window, (255,255,0), pole_position, trolley_position, 1)
                pygame.draw.circle(window, (255,255,0), pole_position, 10)
                pygame.draw.circle(window, (255,255,0), trolley_position, 10)

            else:
                pygame.draw.line(window, (255,255,255), pole_position, trolley_position, 1)
                pygame.draw.circle(window, (0,255,255), pole_position, 10)
                pygame.draw.circle(window, (100,100,100), trolley_position, 10)


            

            





        # Check quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()




best_genome = population.evolve(eval_genomes, 1000)
genetic.save_genome(best_genome,"1000_best.ai")