from functions import clip_set_to_list_on_xaxis, separate_sets_from_yaxis
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
        order = ["black", "corners", "top", "bottom", "sides", "wall", "floor"]
        separated_sets = separate_sets_from_yaxis(spriteset, (255, 0, 0))
        for name, separated_set in zip(order, separated_sets):
            image = clip_set_to_list_on_xaxis(separated_set)
            self.images[name] = image

    # Draw -------------------------------------------------------- #
    def draw_inside_arena(self, display):
        self.draw_arena_wall(display)
        self.draw_arena_floor(display)

    def draw_outside_arena(self, display):
        self.draw_arena_corners(display)
        self.draw_arena_topedge(display)
        self.draw_arena_bottomedge(display)
        self.draw_arena_leftedge(display)
        self.draw_arena_rightedge(display)

    # Status Bar
    def draw_statusbar(self, display):
        image = self.images["black"]
        wd, ht = image.get_rect().size
        x, y = (0, 0)
        for _ in range(2):  # y axis
            for _ in range(window.rect.width // wd):  # x axis
                display.blit(image, (x, y))
                x += wd
            y += ht
            x = 0

    # Arena's Corners
    def draw_arena_corners(self, display):
        images = self.images["corners"]

        # TopLeft Corner
        display.blit(images[0], (0, 32))

        # TopRight Corner
        display.blit(images[1], (624, 32))

        # BottomLeft Corner
        display.blit(images[2], (0, 348))

        # BottomRight Corner
        display.blit(images[3], (624, 348))

    # Arena's Edges
    def draw_arena_topedge(self, display):
        images = self.images["top"]
        wd, _ = images[0].get_rect().size
        x, y = (16, 32)
        
        # First Top Edge
        display.blit(images[0], (x, y))
        x += wd

        # The Rest of Top Edge
        for _ in range(37):
            display.blit(images[1], (x, y))
            x += wd

    def draw_arena_bottomedge(self, display):
        images = self.images["bottom"]
        wd, _ = images[0].get_rect().size
        x, y = (16, 348)

        # First Bottom Edge
        display.blit(images[0], (x, y))
        x += wd
        
        # The Rest of Bottom Edge
        for _ in range(37):
            display.blit(images[1], (x, y))
            x += wd

    def draw_arena_leftedge(self, display):
        images = self.images["sides"]
        _, ht = images[0].get_rect().size
        x, y = (0, 44)
        for _ in range(19):
            display.blit(images[0], (x, y))
            y += ht

    def draw_arena_rightedge(self, display):
        images = self.images["sides"]
        _, ht = images[1].get_rect().size
        x, y = (624, 44)
        for _ in range(19):
            display.blit(images[1], (x, y))
            y += ht

    # Arena's Wall
    def draw_arena_wall(self, display):
        images = self.images["wall"]
        wd, _ = images.get_rect().size
        x, y = (16, 44)
        for _ in range(38):
            display.blit(images, (x, y))
            x += wd

    # Arena's Floor
    def draw_arena_floor(self, display):
        images = self.images["floor"]
        wd, ht = images.get_rect().size
        x, y = (16, 60)
        # for _ in range(38):  # x axis
        #     for _ in range(18):  # y axis
        #         display.blit(images, (x, y))
        #         x += wd
        #     y += ht
        for _ in range(18):  # y axis
            for _ in range(38):  # x axis
                display.blit(images, (x, y))
                x += wd
            y += ht
            x = 16

        
background = Background()
