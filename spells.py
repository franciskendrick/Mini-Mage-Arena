from functions import *
import pygame

pygame.init()


class FireBall:
    # Initialize -------------------------------------------------- #
    def __init__(self, origin, target):
        self.circle = Circle(origin, 4)
        self.init_color()

    def init_color(self):
        self.color = (222, 158, 65)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        center = self.circle.center
        radius = self.circle.radius
        pygame.draw.circle(display, self.color, center, radius)

    # Update ------------------------------------------------------ #
    def update(self):
        pass
