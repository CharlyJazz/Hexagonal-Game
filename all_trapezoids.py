import pygame
from settings import WIDTH, HEIGHT, CENTER_COORDS, RED, GREEN, CIRCLE_RADIUS
from helpers import DRAW_CASTESIAN_PLANE, DRAW_REGULAR_HEXAGON, DRAW_LINES_FROM_ORIGIN_TO_VERTEX, \
DRAW_TRAPEZOID_TOP_LEFT, DRAW_TRAPEZOID_TOP_RIGHT, DRAW_TRAPEZOID_BOTTOM_LEFT, DRAW_TRAPEZOID_BOTTOM_RIGHT, DRAW_TRAPEZOID_BOTTOM, DRAW_TRAPEZOID_TOP

TRAPEZOID_MOVING = pygame.USEREVENT + 1
pygame.time.set_timer(TRAPEZOID_MOVING, 50)
clock = pygame.time.Clock()

def main():
    y = 0
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == TRAPEZOID_MOVING:
                y = y + 1

        screen.fill((0, 0, 0))
        DRAW_TRAPEZOID_TOP(screen, y)
        DRAW_TRAPEZOID_TOP_LEFT(screen, y)
        DRAW_TRAPEZOID_TOP_RIGHT(screen, y)
        DRAW_TRAPEZOID_BOTTOM(screen, y)
        DRAW_TRAPEZOID_BOTTOM_LEFT(screen, y)
        DRAW_TRAPEZOID_BOTTOM_RIGHT(screen, y)
        DRAW_LINES_FROM_ORIGIN_TO_VERTEX(screen)
        pygame.display.update()
     
if __name__=="__main__":
    main()