from functions import *
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class StatusBar:
    # Initialize -------------------------------------------------- #
    def __init__(self, status):
        self.init_images()

    def init_images(self):
        spriteset = pygame.image.load(
            path + "/assets/windows" + "/statusbar.png")
        order = ["bar", "icon", "progress"]
    
        self.images = {}
        separated_sets = separate_sets_from_yaxis(spriteset, (255, 0, 0))
        for name, separated_set in zip(order, separated_sets):
            image = clip_set_to_list(separated_set)
            self.images[name] = image

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        pass


s = StatusBar([])
