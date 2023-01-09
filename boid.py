import pygame
import numpy as np
from math import pi,sin,cos
import math_helper
from constant import MARGIN, WIDTH, HEIGHT, NEIGHBOURS_DISTANCE, MAX_SPEED, SIZE, MAX_FORCE
import random
import math

class Boid:
    def __init__(self, x_coor, y_coor,):
        self.size = SIZE
        self.position = [x_coor,y_coor]
        self.color = (255, 255, 255) #white
        self.velocity = [random.uniform(-1,1), random.uniform(-1,1)]
        self.acceleration = [0,0]
        self.perception = NEIGHBOURS_DISTANCE
        self.max_speed = MAX_SPEED
        self.max_force = MAX_FORCE
        self.separation_factor = 0.9 #less is more

    def update(self):
        
        self.position[0] = (self.position[0] + self.velocity[0]) % WIDTH
        self.position[1] = (self.position[1] + self.velocity[1]) % HEIGHT

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        movement_factor =math_helper.calculate_hypotenuse(self.velocity)
        if movement_factor > self.max_speed:
            self.velocity[0] = self.velocity[0] / movement_factor * self.max_speed
            self.velocity[1] = self.velocity[1] / movement_factor * self.max_speed
        
        self.acceleration = [0,0]
        
        
    def draw(self, screen: pygame.display):
        pygame.draw.circle(screen, self.color, self.position, self.size)

    def behaviour(self, flock):
        neighbours = self.get_neighbours(flock)
        alignment = self.alignment(neighbours)
        cohesion = self.cohesion(neighbours)
        separation = self.separation(neighbours)

        self.acceleration[0] += alignment[0] + cohesion[0] + separation[0]
        self.acceleration[1] += alignment[1] + cohesion[1] + separation[1]

    def alignment(self, neighbours):
        steering = [0,0]
        wanted_velocity = [0,0]
        for boid in neighbours:
            wanted_velocity[0] += boid.velocity[0]
            wanted_velocity[1] += boid.velocity[1]
        if len(neighbours) > 0:
            wanted_velocity[0] /= len(neighbours)
            wanted_velocity[1] /= len(neighbours)
            average_length = math_helper.calculate_hypotenuse(wanted_velocity)
            wanted_velocity = [wanted_velocity[0] / average_length * self.max_speed,  wanted_velocity[1] / average_length * self.max_speed]
            steering = wanted_velocity[0] - self.velocity[0] , wanted_velocity[1] - self.velocity[1]
        return steering
            
    def cohesion(self, neighbours):
        steering = [0,0]
        wanted_position = [0,0]
        for boid in neighbours:
            wanted_position[0] += boid.position[0]
            wanted_position[1] += boid.position[1]
        if len(neighbours) > 0:
            wanted_position[0] /= len(neighbours)
            wanted_position[1] /= len(neighbours)
            wanted_position = [wanted_position[0] - self.position[0], wanted_position[1] - self.position[1]]
            wanted_position_length = math_helper.calculate_hypotenuse(wanted_position)
            if wanted_position_length > 0:
                wanted_position = [wanted_position[0] / wanted_position_length * self.max_speed, wanted_position[1] / wanted_position_length * self.max_speed]
            steering = [wanted_position[0] - self.velocity[0], wanted_position[1] - self.velocity[1]]
            steering_length = math_helper.calculate_hypotenuse(steering)
            if steering_length > self.max_force:
                steering = [steering[0] / steering_length * self.max_force, steering[1] / steering_length * self.max_force]
        return steering

    def separation(self, neighbours):
        steering = [0,0]
        wanted_position = [0,0]
        for boid in neighbours:
            vector1 = [boid.position[0] - self.position[0], boid.position[1] - self.position[1]]
            vector2 = [WIDTH - boid.position[0] - self.position[0], HEIGHT - boid.position[1] - self.position[1]]
            distance = math_helper.get_distance(vector1, vector2)
            if boid is not self:
                diff = [self.position[0] - boid.position[0], self.position[1] - boid.position[1]]  
                diff[0] /= distance
                diff[1] /= distance
                wanted_position[0] += diff[0]
                wanted_position[1] += diff[1]
        if len(neighbours) > 0:
            wanted_position[0] /= len(neighbours)
            wanted_position[1] /= len(neighbours)
            steering_length = math_helper.calculate_hypotenuse(wanted_position)
            if steering_length > 0:
                wanted_position = wanted_position[0] / steering_length * self.max_speed, wanted_position[1] / steering_length * self.max_speed
            steering = [wanted_position[0] - self.velocity[0], wanted_position[1] - self.velocity[1]]
            steering_length = math_helper.calculate_hypotenuse(steering)
            if steering_length > self.max_force / self.separation_factor:
                steering = steering[0] / steering_length * self.max_force / self.separation_factor, steering[1] / steering_length * self.max_force / self.separation_factor
        return steering

    def get_neighbours(self, flock):
        neighbours = []
        for boid in flock:
            vector1 = [boid.position[0] - self.position[0], boid.position[1] - self.position[1]]
            vector2 = [WIDTH - boid.position[0] - self.position[0], HEIGHT - boid.position[1] - self.position[1]]
            distance = math_helper.get_distance(vector1, vector2)
            if distance <= self.perception:
                neighbours.append(boid)                          
        return neighbours
