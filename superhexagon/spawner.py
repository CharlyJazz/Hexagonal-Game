import pygame
import random as rd

from numpy import random, array

from superhexagon.settings import *

class Spawner:
    def __init__(self, hexagon):
        # A Hexagon instance
        self.hexagon = hexagon
        # Complexities
        self.complexity = [
            [1, 1, 1, 1, 1, 1]
        ]
        # Just to a property to help to access a the hexagon angles
        # Maybe remove in the future
        self.angles = ["top","top_right","top_left","bottom","bottom_right","bottom_left"]
        # Quantity of patterns
        self.quantity_of_patterns = 1
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

    def get_space(self, i):
        """
        Get the space to split patters
        With the -1 * we move the polygons outside the hexagon
        """
        return -1 * (i * 8)

    def create_pattern(self):
        """
        This function define the pattern to create
        Some pattern are most hard that others
        Select one array from self.complexity, permute it
        and create a random number and use it to that polygon far away
        and create the safe area.
        Then re define self.progress to create and begin the polygon movement
        This method too use a fixed limit to each pattern
        """
        progress = [{} for _ in range(self.quantity_of_patterns)]

        for i in range(len(progress)):
            space = self.get_space(i)
            complexity_index = rd.randint(0, len(self.complexity) - 1)
            pattern_picked = random.permutation(self.complexity[complexity_index])
            angle_index = rd.randint(0, 2)
            for j, angle_name in enumerate(self.angles):
                if j == angle_index:
                    progress[i][angle_name] = {
                        "y": pattern_picked[j] + LIMIT_PROGRESS,
                        "color": [0, 0, 0]
                    }
                else:
                    progress[i][angle_name] = {
                        "y": -10 * pattern_picked[j] + space * self.hexagon.trapezoid_height,
                        "color": [255, 255, 255] # TEMP, We need create color transition
                    }
        
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
        Move trapezoids to the center of the screen
        If there are a trapezoid in the center the fill it BLACK
        """
        v = self.get_delta_velocity(deltatime)

        for i in range(len(self.progress)):
            for j in self.angles:
                if self.progress[i][j]["y"] <= LIMIT_PROGRESS - v:
                    self.progress[i][j]["y"] += v
                else:
                    self.progress[i][j]["color"] = [0, 0, 0]

    def pattern_creation(self, deltatime):
        """
        Check if we need create a new pattern
        Each pattern hace different limit because they init if other distance
        """
        v = self.get_delta_velocity(deltatime)
        
        should_create = False
        
        for i in range(len(self.progress)):
            if self.progress[i]["top"]["y"] >= LIMIT_PROGRESS - v and \
                self.progress[i]["top_right"]["y"] >= LIMIT_PROGRESS - v and \
                self.progress[i]["top_left"]["y"] >= LIMIT_PROGRESS - v and \
                self.progress[i]["bottom"]["y"] >= LIMIT_PROGRESS - v and \
                self.progress[i]["bottom_right"]["y"] >= LIMIT_PROGRESS - v and \
                self.progress[i]["bottom_left"]["y"] >= LIMIT_PROGRESS - v:
                should_create = True
            else:
                should_create = False
                break
        
        if should_create:
            # Choose quantity of pattern for the round
            self.quantity_of_patterns = rd.randint(1, 3)
            self.create_pattern()

    def draw_trapezoids(self):
        """
        Draw trapezoids of the hexagon instance and return a
        array of Polygons
        """
        trapezoids = []

        for i in range(len(self.progress)):
            for j in self.angles:
                trapezoids.append(
                    self.hexagon.draw_trapezoid(
                        j,
                        self.progress[i][j]["y"], 
                        self.progress[i][j]["color"]
                    )
                )

        return trapezoids
