from functions import *
from windows import window
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Window
win_size = (
    window.rect.width * window.enlarge,
    window.rect.height * window.enlarge)
win = pygame.display.set_mode(win_size)

# Json
json_file = open(path + r"/data" + r"/game.json")
game_data = json.load(json_file)
json_file.close()


class Game:
    def draw_statbar_bg(self, display):
        pygame.draw.rect(display, (16, 20, 31), window.statbar_rect)


class PlayerGauge:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_positions()

    def init_images(self):
        spriteset = pygame.image.load(
            path + "/assets/windows" + "/playergauge.png")
        order = ["bar", "icon", "gauge"]

        # Images
        self.images = {}
        separated_sets = separate_sets_from_yaxis(spriteset, (255, 0, 0))
        for name, separated_set in zip(order, separated_sets):
            image = clip_set_to_list(separated_set)
            self.images[name] = image
        
        # Gauge Palette
        self.gauge_palette()

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
            gauge_images = self.images["gauge"][key]
            if key != "mana":
                for (toggle, img_on, img_off) in gauge_images:
                    img = img_on if toggle else img_off
                    display.blit(img, (x, y))
                    x += 7
            else:
                for gauge_idx, (toggle, img_on, img_off) in enumerate(gauge_images, 1):
                    img = img_on if toggle else img_off
                    display.blit(img, (x, y))
                    x += 2 if gauge_idx % 6 == 0 else 1

    # Update ------------------------------------------------------ #
    def update(self, player_status):
        status_items = list(player_status.items())
        for (key, stat) in status_items:
            gauge_images = self.images["gauge"][key]
            for idx, data in enumerate(gauge_images):
                data[0] = True if stat > idx else False

    # Functions --------------------------------------------------- #
    def gauge_palette(self):
        # Palette
        off_palette = {
            "health": {
                (117, 36, 56): (32, 46, 55),
                (165, 48, 48): (57, 74, 80)},
            "mana": {
                (60, 94, 139): (32, 46, 55),
                (79, 143, 186): (57, 74, 80)},
            "stamina": {
                (222, 158, 65): (32, 46, 55),
                (232, 193, 112): (57, 74, 80)}
        }

        # Gauge Images
        gauge_images = {}

        # Gauge Images of Health & Stamina
        keys = {"health": 0, "stamina": 2}
        for (key, idx) in list(keys.items()):
            images = []
            for _ in range(20):
                img_on = self.images["gauge"][idx]
                img_off = palette_swap(
                    img_on.convert(), off_palette[key])
                images.append([True, img_on, img_off])
            gauge_images[key] = images

        # Gauge Images of Mana
        images = []
        for count in range(120):
            # Orig Image
            orig_img = self.images["gauge"][1]

            # Image On
            pos = (0, 0) if count % 6 == 0 else (1, 0)
            img_on = clip(orig_img, pos, (1, orig_img.get_height()))

            # Image Off
            img_off = palette_swap(
                img_on.convert(), off_palette["mana"])

            # Append
            images.append([True, img_on, img_off])
        gauge_images["mana"] = images

        # Append Gauge Images
        self.images["gauge"] = gauge_images


game = Game()
