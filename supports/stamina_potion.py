from functions import clip_set_to_list_on_xaxis
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class StaminaPotion:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()

    def init_images(self):
        spriteset = pygame.image.load(
            f"{path}/assets/stamina_potion.png")

        # Images
        self.images = clip_set_to_list_on_xaxis(spriteset)
        self.idx = 0
    
    def init_rect(self):
        img_rect = self.images[self.idx].get_rect()
        self.rect = pygame.Rect(200, 200, *img_rect.size)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass

    # Update ------------------------------------------------------ #
    def update(self, player):
        pass
