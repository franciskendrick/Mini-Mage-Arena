from functions import Circle
from windows import window
import pygame
import math

pygame.init()


class WaterDrop:
    # Initialize -------------------------------------------------- #
    def __init__(self, origin, target):
        self.circle = Circle(origin, 4)
        self.init_color()
        self.init_movement(target)
        self.damage = 3
        self.mana_cost = 6
        self.init_status()

    def init_color(self):
        self.color = (79, 143, 186)

    def init_movement(self, target):
        target_x, target_y = target
        self.speed = 10
        angle = math.atan2(
            target_y - self.circle.center[1] * window.enlarge, 
            target_x - self.circle.center[0] * window.enlarge)
        self.x_vel = math.cos(angle)
        self.y_vel = math.sin(angle)

    def init_status(self):
        self.collided = False
        self.delete = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass

    # Update ------------------------------------------------------ #
    def update(self, enemies):
        pass
