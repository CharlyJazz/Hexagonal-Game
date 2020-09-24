import pygame
from settings import WIDTH, HEIGHT, CENTER_COORDS, RED, GREEN, CIRCLE_RADIUS
from helpers import DRAW_CASTESIAN_PLANE, DRAW_REGULAR_HEXAGON, DRAW_LINES_FROM_ORIGIN_TO_VERTEX

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.draw.circle(screen, GREEN, CENTER_COORDS, CIRCLE_RADIUS)
        DRAW_CASTESIAN_PLANE(screen)
        DRAW_REGULAR_HEXAGON(screen)
        DRAW_LINES_FROM_ORIGIN_TO_VERTEX(screen)
        pygame.display.update()
     
if __name__=="__main__":
    main()