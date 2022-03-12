from functions import Circle, clip_set_to_list_on_xaxis, palette_swap
from supports import ManaCrystal
import pygame
import time
import os

path = os.path.dirname(os.path.realpath(__file__))


class Boomshroom:
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
            f"{path}/assets/boomshroom.png")
        self.idx = 0

        # Palettes
        blink_palette = {
            (9, 10, 20): (9, 10, 20),
            (16, 20, 31): (218, 134, 62),
            (21, 29, 40): (222, 158, 65),
            (32, 46, 55): (232, 193, 112),
            (57, 74, 80): (231, 213, 179),
            (165, 48, 48): (235, 237, 233)}
        hit_palette = {
            (9, 10, 20): (9, 10, 20),
            (16, 20, 31): (168, 181, 178),
            (21, 29, 40): (199, 207, 204),
            (32, 46, 55): (168, 181, 178),
            (57, 74, 80): (199, 207, 204),
            (165, 48, 48): (235, 237, 233)}

        # Images
        self.images = {
            "default": clip_set_to_list_on_xaxis(spriteset),
            "blink": clip_set_to_list_on_xaxis(
                palette_swap(spriteset.convert(), blink_palette)),
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
        # Range
        self.attack_range = Circle(
            self.rect.center, 80)
        
        # Trigger
        self.triggered = False

        # Blink
        self.last_blink = time.perf_counter()
        self.time_fuze = 500  # milliseconds
        self.blink_count = 0

        # Explode
        self.explode = False

    def init_hit(self):
        self.last_hit = time.perf_counter()
        self.hit_time = 300  # milliseconds

    def init_status(self):
        self.max_health = 12
        self.health = 12
        self.is_dead = False

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

        # !!!
        center = self.attack_range.center
        radius = self.attack_range.radius
        pygame.draw.circle(
            display, (255, 0, 0), center, radius, 1)

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
        self.trigger_detection(player)
        self.update_fuze()

    # Hit 
    def hit_timer(self):
        if self.image_used == "hit":
            dt = time.perf_counter() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"

    # Functions --------------------------------------------------- #
    # Attack
    def trigger_detection(self, player):
        if self.attack_range.colliderect(player.rect):
            self.triggered = True

    def update_fuze(self):
        if self.triggered and self.blink_count / 2 < 3:
            dt = time.perf_counter() - self.last_blink
            if dt * 1000 >= self.time_fuze:
                self.image_used = "blink" if self.image_used != "blink" else "default"
                self.blink_count += 1
                self.last_blink = time.perf_counter()
        elif self.blink_count / 2 >= 3:
            self.explode = True

    # Hit
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True

        self.image_used = "hit"
        self.last_hit = time.perf_counter()

    # Mana
    def mana_reward(self, mana_crystals):
        for _ in range(round(self.max_health * 1.5)):
            mana_crystals.append(ManaCrystal(self.rect.center))
