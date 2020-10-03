import pygame, math

from collision import Circle, Vector

class Player:
    def __init__(self, screen_width, screen_height, radius, color, surface):
        self.angle = 0
        self.center_coords = (int(screen_width / 2), int(screen_height / 2))
        self.radius_from_center_screen = radius
        self.color = color
        self.surface = surface
        self.radius_cicle = 5
        self.v = 0.08

    def update(self):
        "Update cicle movement"
        return self.movement()

    def movement(self):
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

        x = int(int(math.cos(self.angle) * (self.radius_from_center_screen)) + self.center_coords[0])
        y = int(int(math.sin(self.angle) * (self.radius_from_center_screen)) + self.center_coords[1])

        pygame.draw.circle(self.surface, self.color, [x, y], self.radius_cicle)

        return Circle(Vector(x, y), self.radius_cicle)