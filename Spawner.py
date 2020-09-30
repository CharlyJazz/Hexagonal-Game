import pygame
from numpy import random, array
import random as rd
from settings import LIMIT_PROGRESS

class Spawner:
    def __init__(self, hexagon):
        self.hexagon = hexagon
        self.TOP_PROGRESS_USEREVENT = pygame.USEREVENT + 1
        self.TOP_RIGHT_PROGRESS_USEREVENT = pygame.USEREVENT + 2
        self.TOP_LEFT_PROGRESS_USEREVENT = pygame.USEREVENT + 3
        self.BOTTOM_PROGRESS_USEREVENT = pygame.USEREVENT + 4
        self.BOTTOM_RIGHT_PROGRESS_USEREVENT = pygame.USEREVENT + 5
        self.BOTTOM_LEFT_PROGRESS_USEREVENT = pygame.USEREVENT + 6
        self.complexity = [
            [10, 11, 12, 13, 14, 15],
            [15, 15, 8, 10, 11, 12],
            [8, 9, 15, 17, 12, 7]
        ]
        self.angles = ["top","top_right","top_left","bottom","bottom_right","bottom_left"]
        self.create_pattern()

    def create_pattern(self):
        complexity_index = rd.randint(0, 2)
        
        angle_index = rd.randint(0, 5)
        
        self.values = random.permutation(self.complexity[complexity_index])

        progress = {}
        
        for index, angle in enumerate(self.angles):
            if index == angle_index:
                progress[angle] = self.values[index] + LIMIT_PROGRESS
            else:
                progress[angle] = -10 * self.values[index]
        
        self.progress = progress

    def set_timers(self):
        pygame.time.set_timer(self.TOP_PROGRESS_USEREVENT, 30)
        pygame.time.set_timer(self.TOP_RIGHT_PROGRESS_USEREVENT, 30)
        pygame.time.set_timer(self.TOP_LEFT_PROGRESS_USEREVENT, 30)
        pygame.time.set_timer(self.BOTTOM_PROGRESS_USEREVENT, 30)
        pygame.time.set_timer(self.BOTTOM_RIGHT_PROGRESS_USEREVENT, 30)
        pygame.time.set_timer(self.BOTTOM_LEFT_PROGRESS_USEREVENT, 30)
    
    def update(self):
        if pygame.event.get(self.TOP_PROGRESS_USEREVENT):
            if self.progress["top"] <= LIMIT_PROGRESS - self.values[0]:
                self.progress["top"] += self.values[0]

        if pygame.event.get(self.TOP_RIGHT_PROGRESS_USEREVENT):
            if self.progress["top_right"] <= LIMIT_PROGRESS - self.values[1]:
                self.progress["top_right"] += self.values[1]

        if pygame.event.get(self.TOP_LEFT_PROGRESS_USEREVENT):
            if self.progress["top_left"] <= LIMIT_PROGRESS - self.values[2]:
                self.progress["top_left"] += self.values[2]

        if pygame.event.get(self.BOTTOM_PROGRESS_USEREVENT):
            if self.progress["bottom"] <= LIMIT_PROGRESS - self.values[3]:
                self.progress["bottom"] += self.values[3]

        if pygame.event.get(self.BOTTOM_RIGHT_PROGRESS_USEREVENT):
            if self.progress["bottom_right"] <= LIMIT_PROGRESS - self.values[4]:
                self.progress["bottom_right"] += self.values[4]

        if pygame.event.get(self.BOTTOM_LEFT_PROGRESS_USEREVENT):
            if self.progress["bottom_left"] <= LIMIT_PROGRESS - self.values[5]:
                self.progress["bottom_left"] += self.values[5]
        
        if self.progress["top"] >= LIMIT_PROGRESS - self.values[0] and \
            self.progress["top_right"] >= LIMIT_PROGRESS - self.values[1] and \
            self.progress["top_left"] >= LIMIT_PROGRESS - self.values[2] and \
            self.progress["bottom"] >= LIMIT_PROGRESS - self.values[3] and \
            self.progress["bottom_right"] >= LIMIT_PROGRESS - self.values[4] and \
            self.progress["bottom_left"] >= LIMIT_PROGRESS - self.values[5]:
            self.create_pattern()

    def draw_trapezoids(self):
        top = self.hexagon.draw_trapezoid_top(self.progress[self.angles[0]])
        top_right = self.hexagon.draw_trapezoid_top_right(self.progress[self.angles[1]])
        top_left = self.hexagon.draw_trapezoid_top_left(self.progress[self.angles[2]])
        bottom = self.hexagon.draw_trapezoid_bottom(self.progress[self.angles[3]])
        bottom_right = self.hexagon.draw_trapezoid_bottom_right(self.progress[self.angles[4]])
        bottom_left = self.hexagon.draw_trapezoid_bottom_left(self.progress[self.angles[5]])

        return [
            top,
            top_right,
            top_left,
            bottom,
            bottom_right,
            bottom_left,
        ]
