import pygame
import math
from collision import Vector, collide
from settings import WIDTH, HEIGHT, CENTER_COORDS, RED, GREEN, CIRCLE_RADIUS, CIRCLE_COLOR
from Hexagon import Hexagon
from Player import Player

def main():
    TRAPEZOID_MOVING = pygame.USEREVENT + 1
    pygame.time.set_timer(TRAPEZOID_MOVING, 30)
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    running = True
    small_hexagon = Hexagon(radius=40, color=[255, 0, 0], screen_width=WIDTH, screen_height=HEIGHT, line_width=5, surface=screen)
    big_hexagon = Hexagon(radius=HEIGHT / 2, color=[255, 0, 255], screen_width=WIDTH, screen_height=HEIGHT, line_width=3, surface=screen)
    player = Player(screen_width=WIDTH, screen_height=HEIGHT, radius=60, color=CIRCLE_COLOR, surface=screen)
    y = 0
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == TRAPEZOID_MOVING:
                y = y + 1

        screen.fill((0, 0, 0))
        
        collision_trapezoid_top = big_hexagon.draw_trapezoid_top(y)
        collision_trapezoid_bottom = big_hexagon.draw_trapezoid_bottom(y)
        collision_trapezoid_bottom_right = big_hexagon.draw_trapezoid_bottom_right(y)
        collision_trapezoid_bottom_left = big_hexagon.draw_trapezoid_bottom_left(y)
        collision_trapezoid_top_right = big_hexagon.draw_trapezoid_top_right(y)
        collision_trapezoid_top_left = big_hexagon.draw_trapezoid_top_left(y)

        big_hexagon.draw_lines_from_origin_to_vertex()

        small_hexagon.draw_hexagon()

        small_hexagon.draw_hexagon_filled()

        collision_circle = player.update()

        if collide(collision_trapezoid_top, collision_circle):
            running = False

        if collide(collision_trapezoid_bottom, collision_circle):
            running = False

        if collide(collision_trapezoid_bottom_right, collision_circle):
            running = False
        
        if collide(collision_trapezoid_bottom_left, collision_circle):
            running = False

        if collide(collision_trapezoid_top_right, collision_circle):
            running = False
        
        if collide(collision_trapezoid_top_left, collision_circle):
            running = False

        pygame.display.update()
     
if __name__=="__main__":
    main()