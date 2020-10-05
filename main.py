import sys
import pygame

from superhexagon.surface import GameSurface
from superhexagon.settings import *

def main():
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Hexagon Game')
    clock = pygame.time.Clock()
    game = GameSurface(screen)

    while True:
        deltatime = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_left(ARROW_SPEED)
                elif event.key == pygame.K_RIGHT:
                    game.move_right(ARROW_SPEED)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.move_left(0)
                elif event.key == pygame.K_RIGHT:
                    game.move_right(0)

        if game.game_over:
            quit()
                
        screen.fill((0, 0, 0))
        game.deltatime = deltatime
        game.update()
        pygame.display.update()

if __name__=="__main__":
    main()