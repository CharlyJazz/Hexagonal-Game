import pygame

from math import cos, sin
from collision import Circle, Vector

class Player:
    def __init__(self, screen_width, screen_height, radius_from_center_screen, color, surface):
        self.angle = 0
        self.center_coords = (int(screen_width / 2), int(screen_height / 2))
        self.center_distance = radius_from_center_screen
        self.color = color
        self.surface = surface
        self.radius_cicle = 5
        self.v = 0.05
        self.image = pygame.image.load('player.png')
        self.width, self.height = self.image.get_size() # 45 37

    def update(self, surface):
        "Update cicle movement"
        return self.movement(surface)

    def movement(self, surface):
        """
        Check Left-Right arrows to move the circle in 
        a uniform circular movement and return a 
        Circle instance
        """
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_LEFT]:
            self.angle -= self.v
        if key_pressed[pygame.K_RIGHT]:
            self.angle += self.v

        x = int(int(cos(self.angle) * (self.center_distance)) + self.center_coords[0])
        y = int(int(sin(self.angle) * (self.center_distance)) + self.center_coords[1])

        pygame.draw.circle(self.surface, self.color, [x, y], self.radius_cicle)
        
        image_coords = [x - int(self.width / 2), y - int(self.height / 2 + self.radius_cicle)]
        
        surface.blit(self.image, image_coords)

        return Circle(Vector(x, y), self.radius_cicle)