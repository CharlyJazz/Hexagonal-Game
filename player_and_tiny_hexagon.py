import pygame
import math
from settings import WIDTH, HEIGHT, CENTER_COORDS, RED, GREEN, CIRCLE_RADIUS, CIRCLE_COLOR
from Hexagon import Hexagon

TRAPEZOID_MOVING = pygame.USEREVENT + 1
pygame.time.set_timer(TRAPEZOID_MOVING, 50)
clock = pygame.time.Clock()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    running = True
    small_hexagon = Hexagon(radius=40, color=[255, 0, 0], screen_width=WIDTH, screen_height=HEIGHT, line_width=3, surface=screen)
    big_hexagon = Hexagon(radius=HEIGHT / 2, color=[255, 0, 255], screen_width=WIDTH, screen_height=HEIGHT, line_width=3, surface=screen)
    angle = 0
    y = 0
    while running:
        clock.tick(60)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]:
            angle -= .1
        if key_pressed[pygame.K_RIGHT]:
            angle += .1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == TRAPEZOID_MOVING:
                y = y + 1

        circle_x = int(int(math.cos(angle) * (60)) + CENTER_COORDS[0])
        circle_y = int(int(math.sin(angle) * (60)) + CENTER_COORDS[1])

        screen.fill((0, 0, 0))

        big_hexagon.draw_trapezoid_top(y=y)
        
        big_hexagon.draw_lines_from_origin_to_vertex()

        small_hexagon.draw_hexagon()

        circle = pygame.draw.circle(screen, CIRCLE_COLOR, [circle_x, circle_y], 5)

        pygame.display.update()
     
if __name__=="__main__":
    main()