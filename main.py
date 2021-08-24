import sys
import pygame
import random
import time
import numpy

from threading import Timer
from superhexagon.surface import GameSurface
from superhexagon.settings import *
from superhexagon.chords import CHORDS
from pyfluidsynth import fluidsynth

def main():
    fs = fluidsynth.Synth()
    fs.start(driver = DRIVER)
    sfid = fs.sfload(SOUNDFONT) 
    fs.program_select(0, sfid, 0, 16)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Hexagon Game')
    clock = pygame.time.Clock()
    game = GameSurface(screen)
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
            # Sound a random chord when the hexagons group dissapear
            elif event.type == HEXAGON_DISSAPEAR:
                chord_notes = CHORDS[numpy.random.randint(0, len(CHORDS))]["midi_notes"]
                
                for i in chord_notes:
                    fs.noteon(0, i, 25)
                
                def chord_end(fs, chord_notes_arg):
                    for i in chord_notes_arg:
                        fs.noteoff(0, i)

                # Off notes in another thread in about one second
                Timer(1.0, chord_end, [fs, chord_notes]).start()
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
    fs.delete()
if __name__=="__main__":
    main()
