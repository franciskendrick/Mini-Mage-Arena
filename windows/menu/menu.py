from functions import clip_set_to_list_on_yaxis, get_shadow
from windows import window
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Json
with open(f"{path}/data/menu.json") as json_file:
    menu_data = json.load(json_file)

menu_enlarge = menu_data["enlarge"]


class Title:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()

    def init_images(self):
        animation_set = pygame.image.load(
            f"{path}/assets/title_animation.png")
        self.idx = 0

        # Frames
        self.frames = []
        for img in clip_set_to_list_on_yaxis(animation_set):
            # Initialize
            img_rect = pygame.Rect(
                menu_data["title_position"], img.get_size())
            shadow_img, shadow_rect = get_shadow(
                img, img_rect, menu_data["shadow_offset"])

            # Resize
            wd, ht = img.get_size()
            size = (wd * 3, ht * 3)
            img = pygame.transform.scale(img, size)
            shadow_img = pygame.transform.scale(shadow_img, size)

            # Append
            slide = [
                img,  # orig image
                img_rect,  # image rect
                shadow_img,  # shadow
                shadow_rect  # shadow rect
            ]
            self.frames.append(slide)


class Buttons:
    def __init__(self):
        pass


class Menu:
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface((wd, ht))

    def draw(self, display):
        pass
