from functions import *
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

json_file = open(path + r"/data" + r"/game.json")
game_data = json.load(json_file)
json_file.close()


class PlayerGauge:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_positions()

    def init_images(self):
        spriteset = pygame.image.load(
            path + "/assets/windows" + "/playergauge.png")
        order = ["bar", "icon", "gauge"]
    
        self.images = {}
        separated_sets = separate_sets_from_yaxis(spriteset, (255, 0, 0))
        for name, separated_set in zip(order, separated_sets):
            image = clip_set_to_list(separated_set)
            self.images[name] = image

    def init_positions(self):
        self.positions = game_data["playergauge_position"]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        keys = ["health", "mana", "stamina"]
        for idx, key in enumerate(keys):
            # Icon
            icon = self.images["icon"][idx]
            display.blit(icon, self.positions["icon"][key])
    
            # Bar
            bar = self.images["bar"]
            display.blit(bar, self.positions["bar"][key])

            # Gauge
            x, y = self.positions["gauge"][key]
            for _ in range(20):
                image = self.images["gauge"][idx]
                display.blit(image, (x, y))
                x += 7
