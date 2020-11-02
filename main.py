import sys
import pygame
import random

from superhexagon.surface import GameSurface
from superhexagon.settings import *

def main():
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Hexagon Game')
    clock = pygame.time.Clock()
    game = GameSurface(screen)
    MOVING = pygame.USEREVENT + 1
    EXPANSION = pygame.USEREVENT + 2
    EXPANSION_VALUE = 0
    EXPANSION_SIGN = 1
    VARIABLE = 0
    ORIENTATION = 1
    ANGLE_PER_ORIENTATION = 35
    pygame.time.set_timer(MOVING, 1000)
    pygame.time.set_timer(EXPANSION, 75)
    while True:
        deltatime = clock.tick(60) / 1000
        VARIABLE += ORIENTATION * (ANGLE_PER_ORIENTATION * deltatime)
        game.set_rotation(VARIABLE)
        game.set_expantion(EXPANSION_VALUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == EXPANSION:
                EXPANSION_VALUE = EXPANSION_SIGN + EXPANSION_VALUE
                if EXPANSION_SIGN == 1 and EXPANSION_VALUE >= 10:
                    EXPANSION_SIGN = -1    
                if EXPANSION_SIGN == -1 and EXPANSION_VALUE <= 0:
                    EXPANSION_SIGN = 1
            elif event.type == MOVING:
                # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
                if (bool(random.getrandbits(1))):
                    ORIENTATION = ORIENTATION * -1
                    ANGLE_PER_ORIENTATION = random.choice(ANGLES_PER_DELTATIME)
                pass
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
