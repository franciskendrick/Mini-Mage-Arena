from functions import *
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Slime:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()

    def init_images(self):
        spriteset = pygame.image.load(
            path + "/assets/sprites" + "/slime.png")
        self.idx = 0

        self.images = clip_set_to_list(spriteset)

    def init_rect(self):
        size = self.images[self.idx].get_rect().size
        self.rect = pygame.Rect(100, 100, *size)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        if self.idx >= len(self.images) * 5:
            self.idx = 0

        # Direction
        img = self.images[self.idx // 5]
        
        # Draw
        display.blit(img, self.rect)

        # Update
        self.idx += 1

    # Update ------------------------------------------------------ #

    # Functions --------------------------------------------------- #
