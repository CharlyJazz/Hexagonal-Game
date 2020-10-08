import math
import pygame

from collision import Vector, Concave_Poly, collide

from superhexagon.settings import TRAPEZOID_COLORS

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
        self.vertex = self.create_vertex(0)
        self.line_width = line_width
        self.surface = surface
        self.trapezoid_height = 40
        self.rotation = 0

    def draw_hexagon(self):
        """
        Draw Regular Hexagon without fill
        """
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
        """"
        Lines from center of screen to vertex of the hexagon
        """
        for key, value in self.vertex.items():
            pygame.draw.line(
                self.surface, 
                self.color, 
                self.center_coords, value, 
                4
            )

    def draw_trapezoid_top(self, y=0):
        """
          " " " "  <---  
         "       "
        "         "
        """
        polygon = Concave_Poly(Vector(0, 0),
            [
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + -1 *(self.radius - y)
                    ], 
                    math.radians(-30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + -1 *(self.radius - y)
                    ], 
                    math.radians(30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + -1 *(self.radius - y) + self.trapezoid_height
                    ], 
                    math.radians(30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + -1 *(self.radius - y) + self.trapezoid_height
                    ], 
                    math.radians(-30 + self.rotation)
                ),
            ]
        )
        pygame.draw.polygon(
            self.surface, 
            TRAPEZOID_COLORS['TOP'], 
            (polygon.rel_points[0],polygon.rel_points[1],polygon.rel_points[2],polygon.rel_points[3])
        )
        return polygon

    def draw_trapezoid_bottom(self, y=0):
        """
        "             "
         "           "
          "         "
           " " " " " <--
        """
        polygon = Concave_Poly(Vector(0, 0),
            [
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + (self.radius - y)
                    ], 
                    math.radians(-30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + (self.radius - y)
                    ], 
                    math.radians(30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + (self.radius - y) - self.trapezoid_height
                    ], 
                    math.radians(30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + (self.radius - y) - self.trapezoid_height
                    ], 
                    math.radians(-30 + self.rotation)
                )
            ]
        )
        pygame.draw.polygon(
            self.surface, 
            TRAPEZOID_COLORS['TOP'], 
            (polygon.rel_points[0],polygon.rel_points[1],polygon.rel_points[2],polygon.rel_points[3])
        )
        return polygon

    def draw_trapezoid_bottom_right(self, y):
        """
                  "
            -->  "
                "
        " " " "
        """
        polygon = Concave_Poly(Vector(0, 0),
            [
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0] + (self.radius - y), 
                        self.center_coords[1]
                    ],
                    math.radians(0 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0], 
                        self.center_coords[1] + (self.radius - y)
                    ], 
                    math.radians(-30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0], 
                        self.center_coords[1] + (self.radius - y) - self.trapezoid_height
                    ], 
                    math.radians(-30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0] + (self.radius - y) - self.trapezoid_height,
                        self.center_coords[1]
                    ],
                    math.radians(0 + self.rotation)
                ),
            ]
        )
        pygame.draw.polygon(
            self.surface, 
            TRAPEZOID_COLORS['TOP'], 
            (polygon.rel_points[0],polygon.rel_points[1],polygon.rel_points[2],polygon.rel_points[3])
        )
        return polygon
    
    def draw_trapezoid_bottom_left(self, y):
        """ 
        "
         "   <--
          "
           " " " "
        """
        polygon = Concave_Poly(Vector(0, 0),
            [
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0] - (self.radius - y),
                        self.center_coords[1]
                    ],
                    math.radians(0 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0], 
                        self.center_coords[1] + (self.radius - y)
                    ], 
                    math.radians(30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + (self.radius- y) - self.trapezoid_height
                    ], 
                    math.radians(30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0] - (self.radius- y) + self.trapezoid_height, 
                        self.center_coords[1]
                    ],
                    math.radians(0 + self.rotation)
                ),
            ]
        )
        pygame.draw.polygon(
            self.surface, 
            TRAPEZOID_COLORS['TOP'], 
            (polygon.rel_points[0],polygon.rel_points[1],polygon.rel_points[2],polygon.rel_points[3])
        )
        return polygon

    def draw_trapezoid_top_right(self, y):
        """
        " " " "
        ->      " 
                  "
        """
        polygon = Concave_Poly(Vector(0, 0),
            [
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0] + (self.radius - y),
                        self.center_coords[1]
                    ], 
                    math.radians(0 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0], 
                        self.center_coords[1] + -1 *(self.radius - y)
                    ], 
                    math.radians(30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + -1 *(self.radius - y) + self.trapezoid_height
                    ], 
                    math.radians(30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0] + (self.radius - y) - self.trapezoid_height,
                        self.center_coords[1]
                    ], 
                    math.radians(0 + self.rotation)
                ),
            ]
        )
        pygame.draw.polygon(
            self.surface, 
            TRAPEZOID_COLORS['TOP'], 
            (polygon.rel_points[0],polygon.rel_points[1],polygon.rel_points[2],polygon.rel_points[3])
        )
        return polygon

    def draw_trapezoid_top_left(self, y):
        """
          " " " "    
         " <-
        "
        """
        polygon = Concave_Poly(Vector(0, 0),
            [
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0] - (self.radius - y),
                        self.center_coords[1]
                    ],
                    math.radians(0 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + -1 *(self.radius - y)
                    ], 
                    math.radians(-30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0],
                        self.center_coords[1] + -1 *(self.radius - y) + self.trapezoid_height
                    ], 
                    math.radians(-30 + self.rotation)
                ),
                self.rotate_and_get_a_vector(
                    [
                        self.center_coords[0] - (self.radius - y) + self.trapezoid_height,
                        self.center_coords[1]
                    ],
                    math.radians(0 + self.rotation)
                )
            ]
        )
        pygame.draw.polygon(
            self.surface, 
            TRAPEZOID_COLORS['TOP'], 
            (polygon.rel_points[0],polygon.rel_points[1],polygon.rel_points[2],polygon.rel_points[3])
        )
        return polygon

    def draw_hexagon_filled(self):
        """
        Draw a hexagon filled with black color, useful for the center of the screen
        """
        pygame.draw.polygon(self.surface, [0, 0, 0], [
            self.vertex["CENTER_LEFT"],
            self.vertex["CENTER_BOTTOM_30_DEGREES_LEFT"],
            self.vertex["CENTER_BOTTOM_30_DEGREES_RIGHT"],
            self.vertex["CENTER_RIGHT"],
            self.vertex["CENTER_TOP_30_DEGREES_RIGHT"],
            self.vertex["CENTER_TOP_30_DEGREES_LEFT"],
        ])

    def update_vertex(self, rotation):
        self.rotation = rotation
        self.vertex = self.create_vertex(rotation)

    def create_vertex(self, rotation):
        """
        To avoid memorizing the coordinates of the 6 hexagon vertices, keep them in a dictionary
        Updating with totation and set the rotation to use in the drawing of trapezoids
        """
        self.rotation = rotation
        width, height = self.center_coords
        return {
            "CENTER_BOTTOM_30_DEGREES_RIGHT": self.rotate([width, height + self.radius], math.radians(-30 + rotation)),
            "CENTER_BOTTOM_30_DEGREES_LEFT": self.rotate([width, height + self.radius], math.radians(30 + rotation)),
            "CENTER_RIGHT": self.rotate([width + self.radius, height], math.radians(0 + rotation)),
            "CENTER_LEFT": self.rotate([width - self.radius, height], math.radians(0 + rotation)),
            "CENTER_TOP_30_DEGREES_RIGHT": self.rotate([width, height + -1 *self.radius], math.radians(30 + rotation)),
            "CENTER_TOP_30_DEGREES_LEFT": self.rotate([width, height + -1 *self.radius], math.radians(-30 + rotation))
        }

    def rotate(self, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = self.center_coords
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy
    
    def rotate_and_get_a_vector(self, point, angle):
        """
        Return Vector from check collision
        """
        qx, qy = self.rotate(point, angle)
        return Vector(qx, qy)