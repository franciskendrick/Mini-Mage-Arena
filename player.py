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
        self.init_direction()
        self.init_movement()

    def init_images(self):
        spriteset = pygame.image.load(
            path + "/assets/sprites" + "/player_mage.png")
        self.idx = 0

        self.images = clip_set_to_list(spriteset)

    def init_rect(self):
        size = self.images[self.idx].get_rect().size
        self.rect = pygame.Rect(320, 180, *size)

    def init_direction(self):
        self.direction = None

    def init_movement(self):
        self.vel = 3

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
        self.movement()

    # Direction
    def facing(self):
        m_x, _ = pygame.mouse.get_pos()
        if (self.rect.centerx * window.enlarge) - m_x > 0:  # left
            self.direction = "left" 
        else:  # right
            self.direction = "right" 

    # Movment
    def movement(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_a]:  # left
            self.move_x(-self.vel)
        if keys[pygame.K_d]:  # right
            self.move_x(self.vel)
        if keys[pygame.K_w]:  # up
            self.move_y(-self.vel)
        if keys[pygame.K_s]:  # down
            self.move_y(self.vel)

    def move_x(self, vel):
        handle_rect = self.rect.copy()
        handle_rect.x += vel
        if not edge_collision(handle_rect):
            self.rect.x += vel

    def move_y(self, vel):
        handle_rect = self.rect.copy()
        handle_rect.y += vel
        if not edge_collision(handle_rect):
            self.rect.y += vel
