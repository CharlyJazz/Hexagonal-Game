import pygame
import itertools

class ColorTransition:
    """
    https://stackoverflow.com/questions/51973441/how-to-fade-from-one-colour-to-another-in-pygame
    """
    def __init__(self):
        self.colors = itertools.cycle(['green', 'blue', 'purple', 'pink', 'red', 'orange'])
        self.base_color = next(self.colors)
        self.next_color = next(self.colors)
        self.current_color = self.base_color
        self.change_every_x_seconds = 3.
        self.number_of_steps = self.change_every_x_seconds * 60
        self.step = 1

    def update(self):
        self.step += 1
        if self.step < self.number_of_steps:
            # (y-x)/number_of_steps calculates the amount of change per step required to 
            # fade one channel of the old color to the new color
            # We multiply it with the current step counter
            self.current_color = [
                x + (((y-x)/self.number_of_steps)*self.step) 
                for x, y in zip(
                    pygame.color.Color(self.base_color), 
                    pygame.color.Color(self.next_color)
                )
            ]
        else:
            self.step = 1
            self.base_color = self.next_color
            self.next_color = next(self.colors)

    @property
    def color(self):
        return self.current_color
