import math
import pygame
from helpers import rotate
from settings import TRAPEZOID_COLORS

class Hexagon:
    def __init__(
        self, 
        radius, 
        color,
        screen_width, 
        screen_height,
        line_width,
        surface,
    ):
        self.color = color
        self.radius = radius
        self.center_coords = (int(screen_width / 2), int(screen_height / 2))
        self.vertex = self.create_vertex()
        self.line_width = line_width
        self.surface = surface
        self.trapezoid_height = 40

    def draw_hexagon(self):
        pygame.draw.line(
            self.surface,
            self.color, 
            self.vertex["CENTER_BOTTOM_30_DEGREES_LEFT"],
            self.vertex["CENTER_BOTTOM_30_DEGREES_RIGHT"],
            self.line_width
        )
        pygame.draw.line(
            self.surface,
            self.color, 
            self.vertex["CENTER_BOTTOM_30_DEGREES_RIGHT"],
            self.vertex["CENTER_RIGHT"],
            self.line_width
        )
        pygame.draw.line(
            self.surface,
            self.color, 
            self.vertex["CENTER_BOTTOM_30_DEGREES_LEFT"],
            self.vertex["CENTER_LEFT"],
            self.line_width
        )
        pygame.draw.line(
            self.surface,
            self.color, 
            self.vertex["CENTER_TOP_30_DEGREES_RIGHT"],
            self.vertex["CENTER_RIGHT"],
            self.line_width
        )
        pygame.draw.line(
            self.surface,
            self.color, 
            self.vertex["CENTER_TOP_30_DEGREES_LEFT"],
            self.vertex["CENTER_LEFT"],
            self.line_width
        )
        pygame.draw.line(
            self.surface,
            self.color, 
            self.vertex["CENTER_TOP_30_DEGREES_LEFT"],
            self.vertex["CENTER_TOP_30_DEGREES_RIGHT"],
            self.line_width
        )

    def draw_lines_from_origin_to_vertex(self):
        for key, value in self.vertex.items():
            pygame.draw.line(
                self.surface, 
                self.color, 
                self.center_coords, value, 
                2
            )

    def draw_trapezoid_top(self, y=0):
        pygame.draw.polygon(
            self.surface, 
            TRAPEZOID_COLORS['TOP'], [
                rotate(self.center_coords, [
                    self.center_coords[0], self.center_coords[1] + -1 *(self.radius - y)
                ], math.radians(-30)),
                rotate(self.center_coords, [
                    self.center_coords[0], self.center_coords[1] + -1 *(self.radius - y)
                ], math.radians(30)),
                rotate(self.center_coords, [
                    self.center_coords[0], self.center_coords[1] + -1 *(self.radius - y) + self.trapezoid_height
                ], math.radians(30)),
                rotate(self.center_coords, [
                    self.center_coords[0], self.center_coords[1] + -1 *(self.radius - y) + self.trapezoid_height
                ], math.radians(-30)),
            ]
        )

    def create_vertex(self):
        width, height = self.center_coords
        return {
            "CENTER_BOTTOM_30_DEGREES_RIGHT": rotate(self.center_coords, [width, height + self.radius], math.radians(-30)),
            "CENTER_BOTTOM_30_DEGREES_LEFT": rotate(self.center_coords, [width, height + self.radius], math.radians(30)),
            "CENTER_RIGHT": [width + self.radius, height],
            "CENTER_LEFT": [width - self.radius, height],
            "CENTER_TOP_30_DEGREES_RIGHT": rotate(self.center_coords, [width, height + -1 *self.radius], math.radians(30)),
            "CENTER_TOP_30_DEGREES_LEFT": rotate(self.center_coords, [width, height + -1 *self.radius], math.radians(-30))
        }