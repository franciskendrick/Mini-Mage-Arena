from functions import *
import pygame

pygame.init()


class FireBall:
    # Initialize -------------------------------------------------- #
    def __init__(self, origin, target):
        self.circle = Circle(origin, 4)
        self.init_color()
        self.init_movement(target)
        self.init_collision_detection()

    def init_color(self):
        self.color = (222, 158, 65)
    
    def init_movement(self, target):
        target_x, target_y = target
        self.speed = 8
        angle = math.atan2(
            target_y - self.circle.center[1] * window.enlarge, 
            target_x - self.circle.center[0] * window.enlarge)
        self.x_vel = math.cos(angle)
        self.y_vel = math.sin(angle)

    def init_collision_detection(self):
        self.collided = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        center = self.circle.center
        radius = self.circle.radius
        pygame.draw.circle(display, self.color, center, radius)

    # Update ------------------------------------------------------ #
    def update(self):
        if not self.collided:
            self.movement()
            self.wall_collision()

    # Movement
    def movement(self):
        self.circle.center[0] += (self.x_vel * self.speed)
        self.circle.center[1] += (self.y_vel * self.speed)

    # Collisions
    def wall_collision(self):
        if circle_edge_collision(self.circle):
            self.collided = True

    # Functions --------------------------------------------------- #
