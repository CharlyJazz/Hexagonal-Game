import pygame
import math

from collision import Circle, Vector

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image_file = pygame.image.load('assets/images/arrow.png').convert_alpha()
        self.arrow = pygame.transform.scale(self.image_file, (13, 8))
        self.mask = pygame.mask.from_surface(self.arrow)
        self.pump = 0
        self.image = self.arrow
        self.rect = self.image.get_rect()
        self.center_point = (0, 0)
        self.angle = 0
        self.r = 60
        self.left = 0
        self.right = 0
        self.screen_rotation_speed = 0
        self.circle_radius = 5

    @property
    def angle(self):
        return self.theta
    
    @angle.setter
    def angle(self, value):
        degrees = 180 + value * 180 / math.pi
        self.image = pygame.transform.rotate(self.arrow, degrees)
        self.theta = value

    def set_center_point(self, x, y):
        self.center_point = x, y

    def update(self):
        self.angle += self.left - self.right - self.screen_rotation_speed
        self.rect.centerx = int(self.center_point[0] + (self.r + self.pump) * math.sin(self.theta))
        self.rect.centery = int(self.center_point[1] + (self.r + self.pump) * math.cos(self.theta))
        self.circle = Circle(Vector(self.rect.centerx, self.rect.centery), self.circle_radius)
