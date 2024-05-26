import pygame
import genetic
from math import cos, sin, pi, atan2
from random import randint, seed

# Window
resolution = pygame.Vector2(1000,1000)
window = pygame.display.set_mode(resolution)

# Genetic algorithm
config = genetic.load_config('drone_config.txt')
population = genetic.Population(config, [10,20,4])

def clamp(x:float,x1:float,x2:float) -> float:
    if x < x1:
        return x1
    if x > x2:
        return x2
    return x

class Drone:
    
    length = 100
    strength = 15
    thruster_max_ang = 1.0
    thruster_turn_rate = 2.0
    thruster_strength_change_rate = 2
    thruster_draw_size = 30
    thruster_jet_size = 50
    g = 9.8
    color_winner = (255,0,0)
    color_normal = (0,255,0)






    def __init__(self, pos : 'tuple[float,float]'):

        # Positions for verlet
        self.left_thruster_pos = pygame.Vector2(pos[0]-self.length/2, pos[1])
        self.right_thruster_pos = pygame.Vector2(pos[0]+self.length/2, pos[1])
        self.left_thruster_pos_last = self.left_thruster_pos.copy()
        self.right_thruster_pos_last = self.right_thruster_pos.copy()
        self.alive = True
        self.color = (0,255,0)

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


        # Constraint
        distance = self.left_thruster_pos.distance_to(self.right_thruster_pos)
        if distance != self.length and distance != 0:
            quota = -(self.length - distance)/2.0
            left_to_right = (self.right_thruster_pos - self.left_thruster_pos).normalize()
            self.left_thruster_pos += left_to_right * quota
            self.right_thruster_pos -= left_to_right * quota

        # Bounds
        if self.midpoint.x < 0 or self.midpoint.x > resolution.x or self.midpoint.y < 0 or self.midpoint.y > resolution.y:
            self.alive = False

        

    def turn_thrusters(self, left : float, right : float, dt):
        d_left = clamp(left,-1,1)
        d_right = clamp(1-right,-1,1)
        self.left_angle = clamp(self.left_angle + self.thruster_turn_rate*dt*d_left,-self.thruster_max_ang,self.thruster_max_ang)
        self.right_angle = clamp(self.right_angle + self.thruster_turn_rate*dt*d_right,-self.thruster_max_ang,self.thruster_max_ang)


    def change_thrust(self,left : float, right : float, dt):
        d_left = clamp(left,-1,1)
        d_right = clamp(right,-1,1)
        self.left_thrust = clamp(self.left_thrust+self.thruster_strength_change_rate*dt*d_left,0,1)
        self.right_thrust = clamp(self.right_thrust+self.thruster_strength_change_rate*dt*d_right,0,1)

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
        pygame.draw.circle(window, self.color, self.left_thruster_pos, 10)
        pygame.draw.circle(window, self.color, self.right_thruster_pos, 10)
        pygame.draw.line(window, self.color, self.left_thruster_pos, self.right_thruster_pos, 4)

# Evaluator
def evaluate_genomes(genomes, networks):

    # Init
    clock = pygame.time.Clock()
    time = 0
    max_time = 30
    target = pygame.Vector2(randint(30,round(resolution.x)-30), randint(30,round(resolution.y)-30))
    target_speed = 200
    waypoint_cooldown = 5
    waypoint_time = 0

    # Networks and drones
    drones = []
    start = (randint(100,round(resolution.x)-100), randint(100,round(resolution.y)-100))
    for i in range(len(genomes)):
        drones.append(Drone(start))



    while time < max_time:


        # Tickwise
        i = 0
        for drone in drones:
            if drone.alive:
                i += 1
        if not i: break

        # closest drone
        drone_distances = [drone.midpoint.distance_to(target) for drone in drones]
        average_drone_pos = drones[drone_distances.index(min(drone_distances))].midpoint


        dt = clock.tick(60)/1000
        time += dt
        waypoint_time += dt

        if waypoint_time > waypoint_cooldown:
            waypoint_time = 0
            target = pygame.Vector2(randint(30,round(resolution.x)-30), randint(30,round(resolution.y)-30))


        window.fill((0,30,30))
        pygame.draw.circle(window, (255,255,255), target,30)

        # Drones
        fitnesses = [genome.fitness for genome in genomes]
        best_id = fitnesses.index(max(fitnesses))

        for i in range(len(genomes)):

            drone = drones[i]

            if drone.alive:
                
                # Activate
                inputs = [

                    drone.vel.x / 900,
                    drone.vel.y / 900,
                    drone.angle,
                    drone.angvel,
                    drone.left_angle/drone.thruster_max_ang,
                    drone.right_angle/drone.thruster_max_ang,
                    drone.left_thrust,
                    drone.right_thrust,
                    (target.x-drone.midpoint.x)/resolution.x,
                    (target.y-drone.midpoint.y)/resolution.y,
                ]


                if i == best_id:
                    drone.color = drone.color_winner
                else:
                    drone.color = drone.color_normal

                outputs = networks[i].activate(inputs)

                # Update and draw
                drone.turn_thrusters(outputs[0], outputs[1],dt)
                drone.change_thrust(outputs[2], outputs[3], dt)
                drone.update(dt, resolution)
                drone.draw(window)

                # Fitness
                distance_to_target = drone.midpoint.distance_to(target)
                genomes[i].fitness += time**2/max(1,distance_to_target)

                # Incentive
                """
                Stay close to target
                Survive

                """







        # Check quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()



        pygame.display.update()

winner = population.evolve(evaluate_genomes, 1000)
genetic.save_genome(winner,'drone.ai')