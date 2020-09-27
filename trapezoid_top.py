import pygame
from settings import WIDTH, HEIGHT, CENTER_COORDS, RED, GREEN, CIRCLE_RADIUS
from helpers import DRAW_CASTESIAN_PLANE, DRAW_REGULAR_HEXAGON, DRAW_LINES_FROM_ORIGIN_TO_VERTEX, DRAW_TRAPEZOID_TOP

TRAPEZOID_TOP_MOVING = pygame.USEREVENT + 1
pygame.time.set_timer(TRAPEZOID_TOP_MOVING, 50)
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
            if event.type == TRAPEZOID_TOP_MOVING:
                y = y + 1

        DRAW_LINES_FROM_ORIGIN_TO_VERTEX(screen)
        DRAW_TRAPEZOID_TOP(screen, y)

        pygame.display.update()
     
if __name__=="__main__":
    main()