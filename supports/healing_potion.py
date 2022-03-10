from functions import clip_set_to_dict_on_xaxis, separate_sets_from_yaxis
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class HealingPotion:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_points()
        self.absorbed = False

    def init_images(self):
        # Original Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/healing_potion.png")

        # Separated Spritesets
        self.order = ["small", "medium", "large"]
        potion_spritesets = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))
        self.mana_spritesets = clip_set_to_dict_on_xaxis(
            potion_spritesets, self.order)

        # Images
        self.type = 0
        self.images = self.mana_spritesets[self.order[self.type]]
        self.idx = 0

    def init_rect(self):
        img_rect = self.images[self.idx].get_rect()
        self.rect = pygame.Rect(200, 200, *img_rect.size)

    def init_points(self):
        points_map = {0: 2, 1: 4, 2: 6}
        self.points = points_map[self.type]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        if self.idx >= len(self.images) * 3:
            self.idx = 0

        # Draw
        img = self.images[self.idx // 3]
        display.blit(img, self.rect)

        # Update 
        self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self, player):
        self.player_collision(player)

    # Collisions
    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.add_health(self.points)
            self.absorbed = True
