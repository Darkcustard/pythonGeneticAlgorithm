import pygame
import genetic
from math import cos, sin, pi, atan2
from random import randint, seed, random

# Window
resolution = pygame.Vector2(1000,1000)
window = pygame.display.set_mode(resolution)


# Genetic algorithm
config = genetic.load_config('drone_config.txt')
population = genetic.Population(config, [7,20,20,20,4])

def clamp(x:float,x1:float,x2:float) -> float:
    if x < x1:
        return x1
    if x > x2:
        return x2
    return x

def sign(x : float) -> float:
    return 1 if x >= 0 else -1

class Drone:
    
    length = 100
    strength = 15
    thruster_max_ang = 0.5
    thruster_turn_rate = 2.0
    thruster_strength_change_rate = 2
    thruster_draw_size = 30
    thruster_jet_size = 50
    checkpoint_max_time = 1
    g = 9.8


    checkpoints = [pygame.Vector2(200,200), pygame.Vector2(400,700),pygame.Vector2(500,500),pygame.Vector2(277,800),pygame.Vector2(800,277),pygame.Vector2(653,700),pygame.Vector2(300,300),pygame.Vector2(750,340),pygame.Vector2(700,700),pygame.Vector2(780,250)]
    checkpoint_colors = [(randint(0,255),randint(0,255),randint(0,255)) for i in range(10)]


    def __init__(self, pos : 'tuple[float,float]'):

        # Positions for verlet
        self.left_thruster_pos = pygame.Vector2(pos[0]-self.length/2, pos[1])
        self.right_thruster_pos = pygame.Vector2(pos[0]+self.length/2, pos[1])
        self.left_thruster_pos_last = self.left_thruster_pos.copy()
        self.right_thruster_pos_last = self.right_thruster_pos.copy()
        self.alive = True
        self.color = (0,255,0)
        self.checkpoint_time = 0

        # Inputs
        self.angle = -atan2(self.right_thruster_pos.y-self.left_thruster_pos.y, self.right_thruster_pos.x - self.left_thruster_pos.x)
        self.angle_last = self.angle
        self.midpoint = (self.right_thruster_pos-self.left_thruster_pos)/2 + self.left_thruster_pos
        self.midpoint_last = (self.right_thruster_pos-self.left_thruster_pos)/2 + self.left_thruster_pos
        self.vel = pygame.Vector2(0,0) #self.midpoint.distance_to(self.midpoint_last)/1
        self.angvel = 0#(self.angle-self.angle_last)/1


        # Thrusters
        self.left_angle = 0
        self.right_angle = 0
        self.left_thrust = 0
        self.right_thrust = 0

        self.left_desired_thrust = 0
        self.right_desired_thrust = 0
        self.left_desired_angle = 0
        self.right_desired_angle = 0

        # Target
        self.checkpoint_index = 0
        self.total_checkpoints = 0


    def update(self, dt, resolution):
        
        # Verlet integration
        left_vel = self.left_thruster_pos - self.left_thruster_pos_last
        right_vel = self.right_thruster_pos - self.right_thruster_pos_last
        self.left_thruster_pos_last = self.left_thruster_pos.copy()
        self.right_thruster_pos_last = self.right_thruster_pos.copy()
        self.left_thruster_pos += left_vel
        self.right_thruster_pos += right_vel

        # Forces
        self.left_thruster_pos.y += self.g * dt
        self.right_thruster_pos.y += self.g * dt

        # Turn
        self.left_angle = clamp(self.left_angle + sign(self.left_desired_angle-self.left_angle)*self.thruster_turn_rate*dt, -self.thruster_max_ang, self.thruster_max_ang)
        self.right_angle = clamp(self.right_angle + sign(self.right_desired_angle-self.right_angle)*self.thruster_turn_rate*dt, -self.thruster_max_ang, self.thruster_max_ang)
        self.left_thrust = clamp(self.left_thrust + sign(self.left_desired_thrust-self.left_thrust)*self.thruster_strength_change_rate*dt, 0, 1)
        self.right_thrust = clamp(self.right_thrust + sign(self.right_desired_thrust-self.right_thrust)*self.thruster_strength_change_rate*dt, 0, 1)

        # Thrust
        angle = -atan2(self.right_thruster_pos.y-self.left_thruster_pos.y, self.right_thruster_pos.x - self.left_thruster_pos.x)
        self.left_thruster_pos -= pygame.Vector2(cos(3/2*pi+self.left_angle+angle),-sin(3/2*pi+self.left_angle+angle))*self.left_thrust*self.strength*dt
        self.right_thruster_pos -= pygame.Vector2(cos(3/2*pi+self.right_angle+angle),-sin(3/2*pi+self.right_angle+angle))*self.right_thrust*self.strength*dt

        # Inputs
        self.angle_last = self.angle
        self.angle = -atan2(self.right_thruster_pos.y-self.left_thruster_pos.y, self.right_thruster_pos.x - self.left_thruster_pos.x)
        self.angvel = (self.angle-self.angle_last)/dt
        self.midpoint_last = self.midpoint
        self.midpoint = (self.right_thruster_pos-self.left_thruster_pos)/2 + self.left_thruster_pos
        self.vel = (self.midpoint-self.midpoint_last)/dt

        # Twisting and falling
        if abs(self.angle) > pi/2:
            self.alive = False


        # Constraint
        distance = self.left_thruster_pos.distance_to(self.right_thruster_pos)
        if distance != self.length and distance != 0:
            quota = -(self.length - distance)/2.0
            left_to_right = (self.right_thruster_pos - self.left_thruster_pos).normalize()
            self.left_thruster_pos += left_to_right * quota
            self.right_thruster_pos -= left_to_right * quota



        

    def turn_thrusters(self, left : float, right : float, dt):
        d_left = clamp(left,-1,1)
        d_right = clamp(1-right,-1,1)
        self.left_desired_angle = d_left
        self.right_desired_angle = d_right


    def change_thrust(self,left : float, right : float, dt):
        d_left = clamp(left,-1,1)
        d_right = clamp(right,-1,1)
        self.left_desired_thrust = d_left
        self.right_desired_thrust = d_right

    def draw(self, window):

        # Frame
        pygame.draw.circle(window, (100,100,100), self.left_thruster_pos, 15)
        pygame.draw.circle(window, (100,100,100), self.right_thruster_pos, 15)
        pygame.draw.line(window, (100,100,100), self.left_thruster_pos, self.right_thruster_pos, 10)

        # Thruster
        angle = -atan2(self.right_thruster_pos.y-self.left_thruster_pos.y, self.right_thruster_pos.x - self.left_thruster_pos.x)
        left_ep = pygame.Vector2(cos(3/2*pi+self.left_angle+angle),-sin(3/2*pi+self.left_angle+angle))*self.thruster_draw_size + self.left_thruster_pos
        right_ep = pygame.Vector2(cos(3/2*pi+self.right_angle+angle),-sin(3/2*pi+self.right_angle+angle))*self.thruster_draw_size + self.right_thruster_pos

        left_thrust_ep = pygame.Vector2(cos(3/2*pi+self.left_angle+angle),-sin(3/2*pi+self.left_angle+angle))*self.thruster_jet_size*self.left_thrust + left_ep
        right_thrust_ep = pygame.Vector2(cos(3/2*pi+self.right_angle+angle),-sin(3/2*pi+self.right_angle+angle))*self.thruster_jet_size*self.right_thrust + right_ep

        pygame.draw.line(window,(255,255,0), left_ep, left_thrust_ep,8)
        pygame.draw.line(window,(255,255,0), right_ep, right_thrust_ep,8)


        pygame.draw.line(window, (100,100,100), self.left_thruster_pos, left_ep,10)
        pygame.draw.line(window, (100,100,100), self.right_thruster_pos, right_ep,10)
        
        # Accent
        self.color = self.checkpoint_colors[self.checkpoint_index]
        pygame.draw.circle(window, self.color, self.left_thruster_pos, 10)
        pygame.draw.circle(window, self.color, self.right_thruster_pos, 10)
        pygame.draw.line(window, self.color, self.left_thruster_pos, self.right_thruster_pos, 4)

# Evaluator
def evaluate_genomes(genomes, networks):

    # Init
    clock = pygame.time.Clock()
    time = 0
    max_time = 100
    gamespeed = 2


    # Networks and drones
    drones = []
    for i in range(len(genomes)):
        drones.append(Drone(resolution/2))

    while time < max_time:

        pygame.display.set_caption(f"Drone Training Session | {round(clock.get_fps())} fps")

        # Tickwise
        i = 0
        for drone in drones:
            if drone.alive:
                i += 1
        if not i: break
        dt = clock.tick(60)/1000*gamespeed
        #dt = 1/60*gamespeed
        time += dt
        window.fill((0,30,30))

        for c in range(len(Drone.checkpoints)):
            pygame.draw.circle(window, (Drone.checkpoint_colors[c]), Drone.checkpoints[c], 30)


        # Drones
        fitnesses = [genome.fitness for genome in genomes]
        best_id = fitnesses.index(max(fitnesses))

        for i in range(len(genomes)):

            drone = drones[i]

            if drone.alive:

                # Checkpointing
                checkpoint = drone.checkpoints[drone.checkpoint_index]
                distance = checkpoint.distance_to(drone.midpoint)

                if distance < 30:
                    drone.checkpoint_time += dt
                    genomes[i].fitness += 10*dt

                if drone.checkpoint_time > drone.checkpoint_max_time:
                    drone.checkpoint_index += 1
                    drone.total_checkpoints += 1

                if drone.checkpoint_index > len(Drone.checkpoints)-1:
                    drone.checkpoint_index = 0


                # Bounds
                if drone.midpoint.x < 0 or drone.midpoint.x > resolution.x or drone.midpoint.y < 0 or drone.midpoint.y > resolution.y:
                    drone.alive = False
                    continue
                
                # Activate
                inputs = [

                    drone.vel.x*dt,
                    drone.vel.y*dt,
                    cos(drone.angle),
                    sin(drone.angle),
                    drone.angvel*dt,
                    (checkpoint.x-drone.midpoint.x)/resolution.x,
                    (checkpoint.y-drone.midpoint.y)/resolution.y,
                ]
                outputs = networks[i].activate(inputs)

                # Update and draw
                drone.turn_thrusters(outputs[0], outputs[1],dt)
                drone.change_thrust(outputs[2], outputs[3], dt)
                drone.update(dt, resolution)
                drone.draw(window)

                # Fitness
                genomes[i].fitness += dt/max(1,distance**2)








        # Check quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()



        pygame.display.update()

winner = population.evolve(evaluate_genomes, 4000)
genetic.save_genome(winner,'drone.ai')