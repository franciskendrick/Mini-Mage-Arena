import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Background:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.arena_edges = pygame.image.load(
            f"{path}/assets/arena_edges.png")
        self.arena_inside = pygame.image.load(
            f"{path}/assets/arena_inside.png")
        self.arena_background = pygame.image.load(
            f"{path}/assets/arena_background.png")

    # Draw -------------------------------------------------------- #
    def draw_inside_arena(self, display):
        display.blit(self.arena_inside, (16, 44))

    def draw_outside_arena(self, display):
        display.blit(self.arena_background, (0, 0))
        display.blit(self.arena_edges, (10, 38))

        
background = Background()
