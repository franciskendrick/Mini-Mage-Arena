from functions import Circle, clip_set_to_list_on_xaxis, palette_swap
from supports import ManaCrystal
import pygame
import time
import os

path = os.path.dirname(os.path.realpath(__file__))


class Mushroom:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_direction()
        self.init_attack()
        self.init_hit()
        self.init_status()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/mushroom.png")
        self.idx = 0

        # Palettes
        hit_palette = {
            (9, 10, 20): (9, 10, 20),
            (30, 29, 57): (168, 181, 178),
            (64, 39, 81): (199, 207, 204),
            (122, 54, 123): (235, 237, 233),
            (215, 181, 148): (168, 181, 178),
            (231, 213, 179): (199, 207, 204),
            (235, 237, 233): (235, 237, 233)}

        # Images
        self.images = {
            "default": clip_set_to_list_on_xaxis(spriteset),
            "hit": clip_set_to_list_on_xaxis(
                palette_swap(spriteset.convert(), hit_palette))
        }
        self.image_used = "default"

    def init_rect(self):
        size = self.images[self.image_used][self.idx].get_rect().size
        self.rect = pygame.Rect(100, 100, *size)

    def init_direction(self):
        self.direction = None

    def init_attack(self):
        # Damage
        self.damage = 1

        # Range
        self.attack_range = Circle(
            self.rect.center, 80)
        self.range_visibility = False

        # Time
        self.last_attack = time.perf_counter()
        self.attack_cooldown = 1_000  # milliseconds

    def init_hit(self):
        self.last_hit = time.perf_counter()
        self.hit_time = 300  # milliseconds
        self.is_hit = False

    def init_status(self):
        self.max_health = 12
        self.health = 12
        self.is_dead = False
        self.delete = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        imgs = self.images[self.image_used]
        if self.idx >= len(imgs) * 5:
            self.idx = 0

        # Direction
        img = imgs[self.idx // 5]
        if self.direction == "left":
            img = pygame.transform.flip(img, True, False)

        # Draw
        display.blit(img, self.rect)
        if self.range_visibility:
            center = self.attack_range.center
            radius = self.attack_range.radius
            pygame.draw.circle(
                display, (122, 54, 123), center, radius, 1)

        # Update
        self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self, player):
        self.facing(player)
        self.attack(player)
        self.hit_timer()

    # Direction
    def facing(self, player):
        if self.rect.centerx - player.rect.centerx > 0:  # left
            self.direction = "left"
        else:  # right
            self.direction = "right"

    # Attack
    def attack(self, player):
        if self.attack_range.colliderect(player.rect):
            self.range_visibility = True
            dt = time.perf_counter() - self.last_attack
            if dt * 1000 >= self.attack_cooldown:  # cooldown
                player.hit(self.damage)
                self.last_attack = time.perf_counter()
        else:
            self.range_visibility = False

    # Hit
    def hit_timer(self):
        if self.is_hit:
            dt = time.perf_counter() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"
                self.is_hit = False

    # Functions --------------------------------------------------- #
    # Hit
    def hit(self, damage):
        self.is_hit = True
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True
            self.delete = True

        self.image_used = "hit"
        self.last_hit = time.perf_counter()

    # Mana
    def mana_reward(self, mana_crystals):
        for _ in range(round(self.max_health * 1.5)):
            mana_crystals.append(ManaCrystal(self.rect.center))
