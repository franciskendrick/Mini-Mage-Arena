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
        # Original Spriteset
        spriteset = pygame.image.load(
            path + "/assets/supports" + "/mana_crystals.png")

        # Separated Spritesets
        order = ["small", "medium", "large"]
        mana_spritesets = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))
        mana_spritesets = clip_set_to_dict_on_xaxis(
            mana_spritesets, order)

        # Images
        self.type = 2
        self.images = mana_spritesets[order[self.type]]
        self.idx = 0

    def init_rect(self, center_pos):
        img_rect = self.images[self.idx].get_rect()
        self.rect = pygame.Rect(0, 0, *img_rect.size)
        self.rect.center = center_pos

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        if self.idx >= len(self.images) * 3:
            self.idx = 0

        # Draw
        img = self.images[self.idx // 3]
        display.blit(img, self.rect)

        # Update
        self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self):
        pass

    # Functions --------------------------------------------------- #
