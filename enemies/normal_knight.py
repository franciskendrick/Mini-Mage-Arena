from functions import clip_set_to_list_on_xaxis, palette_swap
from functions import separate_sets_from_xaxis, separate_sets_from_yaxis
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class NormalKnight:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_status()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/normal_knight.png")
        self.idx = 0

        # Palettes
        hit_palette = {
            (129, 151, 150): (235, 237, 233),
            (87, 114, 119): (199, 207, 204),
            (57, 74, 80): (168, 181, 178),
            (32, 46, 55): (129, 151, 150),
            (21, 29, 40): (87, 114, 119),
            (9, 10, 20): (9, 10, 20),
            (122, 72, 65): (168, 181, 178),
            (96, 44, 44): (129, 151, 150),
            (207, 87, 60): (235, 237, 233),
            (165, 48, 48): (168, 181, 178),
            (117, 36, 56): (129, 151, 150)}

        # Images
        walking_spriteset, attacking_spriteset = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))
        knight_walking, sword_walking = separate_sets_from_xaxis(
            walking_spriteset, (0, 255, 0))
        knight_attacking, sword_attacking = separate_sets_from_xaxis(
            attacking_spriteset, (0, 255, 0))

        self.images = {
            "default": {
                "walking": [
                    clip_set_to_list_on_xaxis(knight_walking),
                    clip_set_to_list_on_xaxis(sword_walking)],
                "attacking": [
                    clip_set_to_list_on_xaxis(knight_attacking),
                    clip_set_to_list_on_xaxis(sword_attacking)]
            }
        }
        self.image_used = "default"
        self.doing = "walking"

    def init_rect(self):
        image = self.images[self.image_used][self.doing]
        sword_offset = [12, 2]

        # Sprite
        size = image[0][self.idx].get_rect().size
        self.sprite_rect = pygame.Rect(100, 100, *size)

        # Sword
        size = image[1][self.idx].get_rect().size
        self.sword_rect = pygame.Rect(
            100 + sword_offset[0], 100 + sword_offset[1], *size)

    def init_status(self):
        self.is_dead = False
        self.delete = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        imgs = self.images[self.image_used][self.doing][0]
        if self.idx >= len(imgs) * 5:
            self.idx = 0

        # Draw
        self.draw_sword(display)
        self.draw_sprite(display)

        # Update
        self.idx += 1

    def draw_sword(self, display):
        imgs = self.images[self.image_used][self.doing][0]
        img = imgs[self.idx // 5]
        display.blit(img, self.sprite_rect)

    def draw_sprite(self, display):
        imgs = self.images[self.image_used][self.doing][1]
        img = imgs[self.idx // 5]
        display.blit(img, self.sword_rect)

    # Update ------------------------------------------------------ #
    def update(self, player):
        pass

    # Functions --------------------------------------------------- #
