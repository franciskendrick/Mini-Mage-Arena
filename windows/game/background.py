from functions import clip_set_to_list_on_xaxis
from windows import window
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Background:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()

    def init_images(self):
        spriteset = pygame.image.load(
            f"{path}/assets/arena.png")
        
        # Images
        self.images = {}
        y_values = {
            "black": 0,
            "top": 18,
            "bottom": 32,
            "sides": 46,
            "wall": 64,
            "floor": 82}
        for (name, y) in y_values.items():
            images = clip_set_to_list_on_xaxis(spriteset, y)
            self.images[name] = images
        
    # Draw -------------------------------------------------------- #
    def draw(self, display):
        self.draw_statusbar(display)

    def draw_statusbar(self, display):
        image = self.images["black"]
        wd, ht = image.get_rect().size
        x = 0
        y = 0
        for _ in range(2):
            for _ in range(window.rect.width // wd):
                display.blit(image, (x, y))
                x += wd
            y += 16
            x = 0


background = Background()
