from functions import clip_set_to_list_on_yaxis, get_shadow
from windows import window, background
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Windows
win_size = (
    window.rect.width * window.enlarge,
    window.rect.height * window.enlarge)
win = pygame.display.set_mode(win_size)
display = pygame.Surface(window.rect.size)

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

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        if self.idx >= len(self.frames) * 5:
            self.idx = 0

        # Draw
        img, img_rect, shadow_img, shadow_rect = self.frames[self.idx // 5]
        display.blit(shadow_img, shadow_rect)  # shadow
        display.blit(img, img_rect)  # image

        # Update
        self.idx += 1


class Buttons:
    def __init__(self):
        pass


class Menu:
    def __init__(self):
        wd, ht = window.rect.size
        self.display = pygame.Surface((wd // 2, ht // 2), pygame.SRCALPHA)
        self.display.convert_alpha()
        self.rect = pygame.Rect((0, 0), self.display.get_size())

        self.title = Title()

    def draw(self, display):
        self.display.fill((0, 0, 0, 0))

        # Background
        background.draw_inside_arena(display)
        background.draw_outside_arena(display)
        background.draw_statusbar(display)

        # Title
        self.title.draw(self.display)

        # Blit to Display
        resized_display = pygame.transform.scale(
            self.display, display.get_size())
        display.blit(resized_display, self.rect)


menu = Menu()
