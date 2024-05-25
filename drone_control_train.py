import pygame
import genetic

# Window
resolution = pygame.Vector2(1000,1000)
window = pygame.display.set_mode(resolution)

# Genetic algorithm
config = genetic.load_config('drone_config.txt')
population = genetic.Population(config, [6,20,20,20,4])

class Drone:
    
    length = 100
    strength = 100

    left_angle = 0
    right_angle = 0


    def __init__(self, pos : 'tuple[float,float]'):

        self.left_thruster_pos = pygame.Vector2(pos[0]-self.length/2, pos[1])
        self.right_thruster_pos = pygame.Vector2(pos[0]+self.length/2, pos[1])
        self.color = (0,255,0)
    
    def draw(self, window):

        # Frame
        pygame.draw.circle(window, (100,100,100), self.left_thruster_pos, 15)
        pygame.draw.circle(window, (100,100,100), self.right_thruster_pos, 15)
        pygame.draw.line(window, (100,100,100), self.left_thruster_pos, self.right_thruster_pos, 10)

        # Thruster
        


        # Accent
        pygame.draw.circle(window, self.color, self.left_thruster_pos, 10)
        pygame.draw.circle(window, self.color, self.right_thruster_pos, 10)
        pygame.draw.line(window, self.color, self.left_thruster_pos, self.right_thruster_pos, 4)






# Evaluator
def evaluate_genomes(genomes, networks):

    # Init
    clock = pygame.time.Clock()
    time = 0
    max_time = 30

    test = Drone((500,500))

    while time < max_time:


        # Tickwise
        dt = clock.tick(60)/1000
        time += dt
        window.fill((0,125,125))

        test.draw(window)









        # Check quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()



        pygame.display.update()

winner = population.evolve(evaluate_genomes, 100)
genetic.save_genome(winner)