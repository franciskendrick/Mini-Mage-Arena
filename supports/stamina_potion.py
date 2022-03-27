from functions import clip_set_to_list_on_xaxis
import pygame
import time
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class StaminaPotion:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_status()

    def init_images(self):
        spriteset = pygame.image.load(
            f"{path}/assets/stamina_potion.png")

        # Images
        self.images = clip_set_to_list_on_xaxis(spriteset)
        self.idx = 0
    
    def init_rect(self):
        img_rect = self.images[self.idx].get_rect()
        self.rect = pygame.Rect(200, 200, *img_rect.size)

    def init_status(self):
        # Absorbed
        self.absorbed = False
        self.absorbed_time = None

        # Effect
        self.effect_time = 5000  # milliseconds
        self.effect_lasted = False

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
        self.update_effect(player)

    # Collisions
    def player_collision(self, player):
        if not self.absorbed and self.rect.colliderect(player.rect):
            player.stamina_regenerate = 50  # milliseconds

            self.absorbed = True
            self.absorbed_time = time.perf_counter()

    # Effect
    def update_effect(self, player):
        if self.absorbed:
            dt = time.perf_counter() - self.absorbed_time
            if dt * 1000 >= self.effect_time:

                player.stamina_regenerate = 500  # milliseconds
                self.effect_lasted = True
