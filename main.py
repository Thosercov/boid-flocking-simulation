import pygame
from sys import exit
from boid import Boid
import random
import numpy as np
from constant import WIDTH, HEIGHT, MARGIN, NUM_OF_BOIDS, FPS

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Boids')

clock = pygame.time.Clock()

flock = []
random.seed(NUM_OF_BOIDS)

for i in range(NUM_OF_BOIDS):
    x_coor = random.randint(MARGIN,WIDTH - MARGIN)
    y_coor = random.randint(MARGIN,HEIGHT - MARGIN)
    boid = Boid(x_coor, y_coor)
    flock.append(boid)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    for boid in flock:
        boid.draw(screen)
        boid.update()
        boid.behaviour(flock)


    pygame.display.flip()
    screen.fill((0, 0, 0)) 
    
    # while running at 100 FPS Max
    clock.tick(FPS)