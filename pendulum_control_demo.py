import pygame
import genetic
from math import atan2
from random import random

genome = genetic.load_genome("40_best.ai")
network = genetic.FeedForwardNetwork(genome)

resolution = pygame.Vector2(1000,300)
window = pygame.display.set_mode(resolution)
pygame.display.set_caption("Cart-Pendulum demo")

def get_ang(vec : pygame.Vector2) -> float:
    return atan2(vec.y, vec.x) + 1.5707963267948966

running = True
clock = pygame.time.Clock()
time = 0

track_size = 600
half_pit = (resolution.x - track_size)/2
half_resolution = resolution.x/2
half_track = track_size / 2.0
half_height = resolution.y / 2.0
pole_length = 100
trolley_speed = 20


trolley_position = pygame.Vector2(half_resolution, half_height)
trolley_collided = False
trolley_position_last = pygame.Vector2(half_resolution, half_height)
pole_position = pygame.Vector2(half_resolution,half_height-100)
pole_position_last = pygame.Vector2(half_resolution,half_height-100)
clock.tick()


while running:

    dt = clock.tick(60)/1000
    window.fill((0,0,0))
    time += dt
    pygame.draw.line(window, (255,255,255), pygame.Vector2(half_pit,half_height), pygame.Vector2(resolution.x-half_pit, half_height),2)
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if mouse_clicked:
        distance = mouse_pos.distance_to(pole_position)
        if distance > 0:
            to_mouse = (mouse_pos-pole_position).normalize()
            pole_position += to_mouse*10*dt

    # check for exits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Calculate angles
    current_ang = get_ang(pole_position-trolley_position)
    last_ang = get_ang(pole_position_last-trolley_position)
    angvel = (current_ang-last_ang)/dt



    # Enforce verlet pole
    pole_vel = pole_position-pole_position_last
    pole_position_last = pole_position.copy()
    pole_position += pole_vel
    pole_position.y += 10*dt

    # if genetic.utility.odds(0.001):
    #     pole_position.x += (random()*10-5)

    # Enforce verlet trolley
    trolley_vel = trolley_position-trolley_position_last
    trolley_position_last = trolley_position.copy()
    trolley_position += trolley_vel


    # Enforce constraints
    distance = pole_position.distance_to(trolley_position)
    if distance != pole_length and distance != 0:
        to_pole = (pole_position-trolley_position).normalize()
        delta = pole_length-distance
        pole_position+=delta*to_pole

    # if genetic.utility.odds(0.01):
    #     pole_position.x += (random()*10-5)

    # Query network and fitness
    if not trolley_collided:

        # Slide off track
        if trolley_position.x < half_pit:
            trolley_collided = True
        if trolley_position.x > resolution.x-half_pit:
            trolley_collided = True
        if pole_position.y > half_height:
            trolley_collided = True

        inputs = [current_ang, angvel, (trolley_position.x-half_resolution)/(half_track), trolley_vel.x]
        outputs = network.activate(inputs)
        choice = outputs.index(max(outputs))
        moves = [pygame.Vector2(-1,0), pygame.Vector2(1,0)]
        trolley_position += moves[choice]*dt*trolley_speed

    else:
        trolley_position.y += 10*dt

    

    pygame.draw.line(window, (255,255,255), pole_position, trolley_position, 1)
    pygame.draw.circle(window, (0,255,255), pole_position, 10)
    pygame.draw.circle(window, (100,100,100), trolley_position, 10)




    pygame.display.update()