import pygame

from collision import collide

from superhexagon.settings import *
from superhexagon.hexagon import *
from superhexagon.player import *
from superhexagon.spawner import *
from superhexagon.color_transition import *

class GameSurface(pygame.Surface):
    def __init__(self, screen):
        self.screen = screen
        self.small_hexagon = Hexagon(
            radius=SMALL_HEXAGON_RADIUS,
            color=CIRCLE_COLOR, 
            screen_width=WIDTH, 
            screen_height=HEIGHT, 
            line_width=5, 
            surface=self.screen
        )
        self.big_hexagon = Hexagon(
            radius=CIRCLE_RADIUS, 
            color=CIRCLE_COLOR, 
            screen_width=WIDTH, 
            screen_height=HEIGHT, 
            line_width=3, 
            surface=self.screen
        )
        self.spawner = Spawner(hexagon=self.big_hexagon)
        self.player = Player()
        self.color_transition = ColorTransition()
        self.deltatime = 0
        self.left = 0
        self.right = 0
        self.player.set_center_point(WIDTH//2, HEIGHT//2)
        self.game_over = False
        self.rotation = 0
        self.expand = 0
        super().__init__(self.screen.get_size())

    def update(self):
        self.color_transition.update()
        self.spawner.update(self.deltatime)
        trapezoids = self.spawner.draw_trapezoids()
        self.big_hexagon.draw_lines_from_origin_to_vertex(self.color_transition.color)
        self.player.left = self.left
        self.player.right = self.right
        self.player.update()
        self.screen.blit(self.player.image, self.player.rect)
        self.big_hexagon.update_vertex(self.rotation, 0)
        self.small_hexagon.update_vertex(self.rotation, self.expand)
        self.small_hexagon.draw_hexagon(self.color_transition.color)
        self.small_hexagon.draw_hexagon_filled()
        for i in trapezoids:
            if collide(i, self.player.circle):
                self.game_over = True

    def set_expantion(self, amount):
        self.expand = amount

    def set_rotation(self, amount):
        self.rotation = amount    

    def move_left(self, amount):
        self.left = amount
    
    def move_right(self, amount):
        self.right = amount
