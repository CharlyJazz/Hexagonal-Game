import pygame
import math
from collision import Vector, collide
from settings import WIDTH, HEIGHT, CENTER_COORDS, RED, GREEN, CIRCLE_RADIUS, CIRCLE_COLOR, SMALL_HEXAGON_RADIUS
from Hexagon import Hexagon
from Player import Player
from Spawner import Spawner

def main():
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Hexagon Game')
    small_hexagon = Hexagon(radius=SMALL_HEXAGON_RADIUS, color=CIRCLE_COLOR, screen_width=WIDTH, screen_height=HEIGHT, line_width=5, surface=screen)
    big_hexagon = Hexagon(radius=CIRCLE_RADIUS, color=CIRCLE_COLOR, screen_width=WIDTH, screen_height=HEIGHT, line_width=3, surface=screen)
    player = Player(screen_width=WIDTH, screen_height=HEIGHT, radius=60, color=CIRCLE_COLOR, surface=screen)
    spawner = Spawner(hexagon=big_hexagon)
    spawner.set_timers()
    clock = pygame.time.Clock()
    pygame.init()
    running = True
    while running:
        clock.tick(60)
        
        if pygame.event.get(pygame.QUIT):
            running = False
                
        screen.fill((0, 0, 0))

        spawner.update()
        
        trapezoids = spawner.draw_trapezoids()

        big_hexagon.draw_lines_from_origin_to_vertex()

        small_hexagon.draw_hexagon()

        small_hexagon.draw_hexagon_filled()

        circle = player.update()

        for i in trapezoids:
            if collide(i, circle):
                running = False

        pygame.display.update()
     
if __name__=="__main__":
    main()
