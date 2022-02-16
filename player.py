from functions import *
from windows import window
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Player:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_movement_direction()

    def init_images(self):
        spriteset = pygame.image.load(
            path + "/assets/sprites" + "/player_mage.png")
        self.idx = 0

        self.images = clip_set_to_list(spriteset)

    def init_rect(self):
        size = self.images[self.idx].get_rect().size
        self.rect = pygame.Rect(320, 180, *size)

    def init_movement_direction(self):
        # Direction
        self.direction = None

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        self.draw_sprite(display)

    def draw_sprite(self, display):
        # Reset
        if self.idx >= len(self.images) * 5:
            self.idx = 0

        # Direction
        img = self.images[self.idx // 5]
        if self.direction == "left":
            img = pygame.transform.flip(img, True, False)

        # Draw
        display.blit(img, self.rect)

        # Update
        self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self):
        self.facing()

    # Direction
    def facing(self):
        m_x, _ = pygame.mouse.get_pos()
        if (self.rect.centerx * window.enlarge) - m_x > 0:  # left
            self.direction = "left" 
        else:  # right
            self.direction = "right" 
