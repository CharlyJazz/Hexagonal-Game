from pygame.draw import line as l, polygon as p
from settings import WIDTH, HEIGHT, CIRCLE_RADIUS, RED, CENTER_COORDS, HEXAGON_LINE_COLOR, TRAPEZOID_HEIGHT, TRAPEZOID_COLORS

import math

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

VERTEX_COORDENATES = {
    "CENTER_BOTTOM_30_DEGREES_RIGHT": rotate(CENTER_COORDS, [
        CENTER_COORDS[0], CENTER_COORDS[1] + CIRCLE_RADIUS
    ], math.radians(-30)),
    "CENTER_BOTTOM_30_DEGREES_LEFT": rotate(CENTER_COORDS, [
        CENTER_COORDS[0], CENTER_COORDS[1] + CIRCLE_RADIUS
    ], math.radians(30)),
    "CENTER_RIGHT": [CENTER_COORDS[0] + CIRCLE_RADIUS, CENTER_COORDS[1]],
    "CENTER_LEFT": [CENTER_COORDS[0] - CIRCLE_RADIUS, CENTER_COORDS[1]],
    "CENTER_TOP_30_DEGREES_RIGHT": rotate(CENTER_COORDS, [
        CENTER_COORDS[0], CENTER_COORDS[1] + -1 *CIRCLE_RADIUS
    ], math.radians(30)),
    "CENTER_TOP_30_DEGREES_LEFT": rotate(CENTER_COORDS, [
        CENTER_COORDS[0], CENTER_COORDS[1] + -1 *CIRCLE_RADIUS
    ], math.radians(-30))
}

def DRAW_CASTESIAN_PLANE(surface):
    l(surface, RED, [0, HEIGHT / 2], [WIDTH, HEIGHT / 2], 2)
    l(surface, RED, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 2)

def DRAW_LINES_FROM_ORIGIN_TO_VERTEX(surface):
    # CENTER RIGHT
    l(
        surface, [0, 250, 250], 
        CENTER_COORDS, VERTEX_COORDENATES["CENTER_RIGHT"], 1
    )
    # CENTER BOTTOM 30 DEGREES RIGHT
    l(
        surface, [0, 250, 250], 
        CENTER_COORDS, VERTEX_COORDENATES["CENTER_BOTTOM_30_DEGREES_RIGHT"], 1
    )
    # CENTER BOTTOM 30 DEGREES LEFT
    l(
        surface, [0, 250, 250], 
        CENTER_COORDS, VERTEX_COORDENATES["CENTER_BOTTOM_30_DEGREES_LEFT"], 1
    )
    # CENTER LEFT
    l(
        surface, [0, 250, 250], 
        CENTER_COORDS, VERTEX_COORDENATES["CENTER_LEFT"], 1
    )
    # CENTER TOP 30 DEGREES LEFT
    l(
        surface, [0, 250, 250], 
        CENTER_COORDS, VERTEX_COORDENATES["CENTER_TOP_30_DEGREES_LEFT"], 1
    )
    # CENTER TOP 30 DEGREES RIGHT
    l(
        surface, [0, 250, 250], 
        CENTER_COORDS, VERTEX_COORDENATES["CENTER_TOP_30_DEGREES_RIGHT"], 1
    )

def DRAW_REGULAR_HEXAGON(surface):
    
    # CONNECT VERTEX

    l(
        surface, HEXAGON_LINE_COLOR, 
        VERTEX_COORDENATES["CENTER_BOTTOM_30_DEGREES_LEFT"],
        VERTEX_COORDENATES["CENTER_BOTTOM_30_DEGREES_RIGHT"],
        2
    )
    l(
        surface, HEXAGON_LINE_COLOR, 
        VERTEX_COORDENATES["CENTER_BOTTOM_30_DEGREES_RIGHT"],
        VERTEX_COORDENATES["CENTER_RIGHT"],
        2
    )
    l(
        surface, HEXAGON_LINE_COLOR, 
        VERTEX_COORDENATES["CENTER_BOTTOM_30_DEGREES_LEFT"],
        VERTEX_COORDENATES["CENTER_LEFT"],
        2
    )
    l(
        surface, HEXAGON_LINE_COLOR, 
        VERTEX_COORDENATES["CENTER_TOP_30_DEGREES_RIGHT"],
        VERTEX_COORDENATES["CENTER_RIGHT"],
        2
    )
    l(
        surface, HEXAGON_LINE_COLOR, 
        VERTEX_COORDENATES["CENTER_TOP_30_DEGREES_LEFT"],
        VERTEX_COORDENATES["CENTER_LEFT"],
        2
    )
    l(
        surface, HEXAGON_LINE_COLOR, 
        VERTEX_COORDENATES["CENTER_TOP_30_DEGREES_LEFT"],
        VERTEX_COORDENATES["CENTER_TOP_30_DEGREES_RIGHT"],
        2
    )

def DRAW_TRAPEZOID_TOP(surface, y=0):
    GLOBAL_TOP_TRAPEZOID = p(surface, TRAPEZOID_COLORS['TOP'], [
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + -1 *(CIRCLE_RADIUS - y)
        ], math.radians(-30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + -1 *(CIRCLE_RADIUS - y)
        ], math.radians(30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + -1 *(CIRCLE_RADIUS - y) + TRAPEZOID_HEIGHT
        ], math.radians(30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + -1 *(CIRCLE_RADIUS - y) + TRAPEZOID_HEIGHT
        ], math.radians(-30)),
    ])

def DRAW_TRAPEZOID_BOTTOM(surface, y=0):
    GLOBAL_BOTTOM_TRAPEZOID = p(surface, TRAPEZOID_COLORS['BOTTOM'], [
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + (CIRCLE_RADIUS - y)
        ], math.radians(-30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + (CIRCLE_RADIUS - y)
        ], math.radians(30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + (CIRCLE_RADIUS - y) - TRAPEZOID_HEIGHT
        ], math.radians(30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + (CIRCLE_RADIUS - y) - TRAPEZOID_HEIGHT
        ], math.radians(-30)),
    ])

def DRAW_TRAPEZOID_BOTTOM_RIGHT(surface, y): 
    GLOBAL_BOTTOM_RIGHT_TRAPEZOID = p(surface, TRAPEZOID_COLORS['BOTTOM_RIGHT'], [
        [CENTER_COORDS[0] + (CIRCLE_RADIUS - y), CENTER_COORDS[1]], # x
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + (CIRCLE_RADIUS - y)
        ], math.radians(-30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + (CIRCLE_RADIUS - y) - TRAPEZOID_HEIGHT
        ], math.radians(-30)),
        [CENTER_COORDS[0] + (CIRCLE_RADIUS - y) - TRAPEZOID_HEIGHT, CENTER_COORDS[1]], # x
    ])

def DRAW_TRAPEZOID_BOTTOM_LEFT(surface, y): 
    GLOBAL_BOTTOM_LEFT_TRAPEZOID = p(surface, TRAPEZOID_COLORS['BOTTOM_LEFT'], [
        [CENTER_COORDS[0] - (CIRCLE_RADIUS -y), CENTER_COORDS[1]],
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + (CIRCLE_RADIUS -y)
        ], math.radians(30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + (CIRCLE_RADIUS-y) - TRAPEZOID_HEIGHT
        ], math.radians(30)),
        [CENTER_COORDS[0] - (CIRCLE_RADIUS-y) + TRAPEZOID_HEIGHT, CENTER_COORDS[1]],
    ])

def DRAW_TRAPEZOID_TOP_RIGHT(surface, y):
    GLOBAL_TOP_RIGHT_TRAPEZOID = p(surface, TRAPEZOID_COLORS["TOP_RIGHT"], [
        [CENTER_COORDS[0] + (CIRCLE_RADIUS - y), CENTER_COORDS[1]],
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + -1 *(CIRCLE_RADIUS - y)
        ], math.radians(30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + -1 *(CIRCLE_RADIUS - y) + TRAPEZOID_HEIGHT
        ], math.radians(30)),
        [CENTER_COORDS[0] + (CIRCLE_RADIUS - y) - TRAPEZOID_HEIGHT, CENTER_COORDS[1]],
    ])

def DRAW_TRAPEZOID_TOP_LEFT(surface, y):
    GLOBAL_TOP_LEFT_TRAPEZOID = p(surface, TRAPEZOID_COLORS["TOP_LEFT"], [
        [CENTER_COORDS[0] - (CIRCLE_RADIUS - y), CENTER_COORDS[1]],
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + -1 *(CIRCLE_RADIUS - y)
        ], math.radians(-30)),
        rotate(CENTER_COORDS, [
            CENTER_COORDS[0], CENTER_COORDS[1] + -1 *(CIRCLE_RADIUS - y) + TRAPEZOID_HEIGHT
        ], math.radians(-30)),
        [CENTER_COORDS[0] - (CIRCLE_RADIUS - y) + TRAPEZOID_HEIGHT, CENTER_COORDS[1]],
    ])