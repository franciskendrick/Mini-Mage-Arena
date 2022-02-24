from functions import *
import pygame

pygame.init()


class DarkFireBall:
    # Initialize -------------------------------------------------- #
    def __init__(self, origin, target):
        self.circle = Circle(origin, 4)
        self.init_color()

    def init_color(self):
        self.color = (168, 202, 88)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        center = self.circle.center
        radius = self.circle.radius
        pygame.draw.circle(display, self.color, center, radius)

    # Update ------------------------------------------------------ #
    def update(self, player):
        pass

    # Functions --------------------------------------------------- #