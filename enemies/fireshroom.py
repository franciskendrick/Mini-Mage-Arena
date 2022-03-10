from functions import clip_set_to_list_on_xaxis, palette_swap
from windows import window
from functions import Circle
from supports import ManaCrystal
from enemy_spells import DarkFireBall
import pygame
import time
import os

path = os.path.dirname(os.path.realpath(__file__))


class Fireshroom:
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
            f"{path}/assets/fireshroom.png")
        self.idx = 0

        # Palettes
        hit_palette = {
            (9, 10, 20): (9, 10, 20),
            (117, 36, 56): (168, 181, 178),
            (165, 48, 48): (199, 207, 204),
            (207, 87, 60): (235, 237, 233),
            (215, 181, 148): (168, 181, 178),
            (231, 213, 179): (199, 207, 204),
            (218, 134, 62): (235, 237, 233)}

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
        # Range
        self.attack_range = Circle(
            self.rect.center, 80)
        self.range_visibility = False

        # Targets
        target_directions = [
            (x, y) for x in range(-1, 2) for y in range(-1, 2) if (x, y) != (0, 0)
        ]

        self.targets = []
        for direction in target_directions:
            target = (
                (self.rect.centerx * window.enlarge) + direction[0],
                (self.rect.centery * window.enlarge) + direction[1])
            self.targets.append(target) 

        # Attack List
        self.attack_list = []

        # Time
        self.last_attack = time.perf_counter()
        self.attack_cooldown = 1_200  # milliseconds

    def init_hit(self):
        self.last_hit = time.perf_counter()
        self.hit_time = 300  # milliseconds

    def init_status(self):
        self.max_health = 12
        self.health = 12
        self.is_dead = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        self.draw_sprite(display)
        self.draw_attacks(display)

    def draw_sprite(self, display):
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

        # Update
        self.idx += 1

    def draw_attacks(self, display):
        # Range
        if self.range_visibility:
            center = self.attack_range.center
            radius = self.attack_range.radius
            pygame.draw.circle(
                display, (165, 48, 48), center, radius, 1)

        # Attacks
        for attack in self.attack_list:
            attack.draw(display)

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
            self.append_attack()
        else:
            self.range_visibility = False
        self.update_attack(player)

    # Hit
    def hit_timer(self):
        if self.image_used == "hit":
            dt = time.perf_counter() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"

    # Functions --------------------------------------------------- #
    # Attacks
    def append_attack(self):
        dt = time.perf_counter() - self.last_attack
        if dt * 1000 >= self.attack_cooldown:  # cooldown
            for target in self.targets:
                attack = DarkFireBall(self.rect.center, target)
            
                self.attack_list.append(attack)
                self.last_attack = time.perf_counter()

    def update_attack(self, player):
        remove_attack = []

        # Update Attacks
        for attack in self.attack_list:
            attack.update(player)
            if attack.collided:
                remove_attack.append(attack)

        # Remove Attacks
        for attack in remove_attack:
            self.attack_list.remove(attack)

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
