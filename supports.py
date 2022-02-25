from re import A
from functions import *
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class ManaCrystal:
    # Initialize -------------------------------------------------- #
    def __init__(self, center_pos):
        self.init_images()
        self.init_rect(center_pos)

    def init_images(self):
        spriteset = pygame.image.load(
            path + "/assets/supports" + "/mana_crystals.png")
        mana_spritesets = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))
        order = ["small", "medium", "large"]
        self.type = 0

        self.images = mana_spritesets[order[self.type]]
        self.idx = 0

    def init_rect(self, center_pos):
        img_rect = self.images[self.idx].get_rect()
        self.rect = pygame.Rect(0, 0, *img_rect.size)
        self.rect.center = center_pos

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass

    # Update ------------------------------------------------------ #
    def update(self):
        pass

    # Functions --------------------------------------------------- #
