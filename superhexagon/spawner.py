import pygame
import random as rd

from numpy import random, array

from superhexagon.settings import LIMIT_PROGRESS

class Spawner:
    def __init__(self, hexagon):
        # A Hexagon instance
        self.hexagon = hexagon
        # Complexities
        self.complexity = [
            [1, 1, 1, 1, 1, 1],
            [5, 10, 15, 20, 25, 30]
        ]
        # Just to a property to help to access a the hexagon angles
        # Maybe remove in the future
        self.angles = ["top","top_right","top_left","bottom","bottom_right","bottom_left"]
        # Angle index to not show polygon
        self.angle_index = None
        # Create first pattern
        self.create_pattern()
        # With this line with define a relative velocity, 
        # depending of the size of the hexagon
        self.velocity = self.hexagon.radius / 2

    def get_delta_velocity(self, deltatime):
        """
        Get velocity using deltatime
        """
        return self.velocity * deltatime

    def create_pattern(self):
        """
        This function define the pattern to create
        Some pattern are most hard that others
        Select one array from self.complexity, permute it
        and create a random number and use it to that polygon far away
        and create the safe area.
        Then re define self.progress to create and begin the polygon movement
        """
        complexity_index = rd.randint(0, len(self.complexity) - 1)
        new_angle = rd.randint(0, 5)

        # Avoid repeat safe area
        while new_angle == self.angle_index:
            new_angle = rd.randint(0, 5)
            
        self.angle_index = new_angle
        
        self.values = random.permutation(self.complexity[complexity_index])

        progress = {}
        
        for index, angle_name in enumerate(self.angles):
            if index == self.angle_index:
                progress[angle_name] = self.values[index] + LIMIT_PROGRESS
            else:
                progress[angle_name] = -10 * self.values[index]
        
        self.progress = progress

    def update(self, deltatime):
        """
        Update in each frame, accumulate polygon progress 
        and check if we need create new polygon pattern
        """
        self.accumulate_progress(deltatime)
        self.pattern_creation(deltatime)

    def accumulate_progress(self, deltatime):
        """
        Accumulate polygon progress using deltatime
        and the property velocity
        """
        v = self.get_delta_velocity(deltatime)

        if self.progress["top"] <= LIMIT_PROGRESS - v:
            self.progress["top"] += v

        if self.progress["top_right"] <= LIMIT_PROGRESS - v:
            self.progress["top_right"] += v

        if self.progress["top_left"] <= LIMIT_PROGRESS - v:
            self.progress["top_left"] += v

        if self.progress["bottom"] <= LIMIT_PROGRESS - v:
            self.progress["bottom"] += v

        if self.progress["bottom_right"] <= LIMIT_PROGRESS - v:
            self.progress["bottom_right"] += v
        
        if self.progress["bottom_left"] <= LIMIT_PROGRESS - v:
            self.progress["bottom_left"] += v
        

    def pattern_creation(self, deltatime):
        """
        Check if we need create a new pattern
        """
        v = self.get_delta_velocity(deltatime)
        if self.progress["top"] >= LIMIT_PROGRESS - v and \
            self.progress["top_right"] >= LIMIT_PROGRESS - v and \
            self.progress["top_left"] >= LIMIT_PROGRESS - v and \
            self.progress["bottom"] >= LIMIT_PROGRESS - v and \
            self.progress["bottom_right"] >= LIMIT_PROGRESS - v and \
            self.progress["bottom_left"] >= LIMIT_PROGRESS - v:
            self.create_pattern()

    def draw_trapezoids(self):
        """
        Draw trapezoids of the hexagon instance and return a
        array of Polygons
        """
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
