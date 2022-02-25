from re import A
from functions import *
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class ManaCrystal:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()

    def init_images(self):
        spriteset = pygame.image.load(
            path + "/assets/supports" + "/mana_crystals.png")
        mana_spritesets = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))
        order = ["small", "medium", "large"]
        self.type = 0
        
        self.images = mana_spritesets[order[self.type]]
        self.idx = 0

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass

    # Update ------------------------------------------------------ #
    def update(self):
        pass

    # Functions --------------------------------------------------- #
