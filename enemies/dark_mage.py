from functions import clip_set_to_list_on_xaxis, palette_swap
from supports import ManaCrystal
from spells.enemy import DarkFireBall
from windows import window
import pygame
import time
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class DarkMage:
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
            f"{path}/assets/dark_mage.png")
        self.idx = 0

        # Palettes
        hit_palette = {
            (9, 10, 20): (9, 10, 20),
            (25, 51, 45): (168, 181, 178),
            (37, 86, 46): (199, 207, 204),
            (70, 130, 50): (235, 237, 233),
            (165, 48, 48): (235, 237, 233)}

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
        # Attack Lists
        self.attack_list = []

        # Time
        self.last_attack = time.perf_counter()
        self.attack_cooldown = 1_200  # milliseconds

    def init_hit(self):
        self.last_hit = time.perf_counter()
        self.hit_time = 300  # milliseconds

    def init_status(self):
        self.max_health = 20
        self.health = 20
        self.is_dead = False
        self.delete = False

    # Draw -------------------------------------------------------- #
    # Draws
    def draw(self, display):
        if not self.is_dead:
            self.draw_sprite(display)
        self.draw_attacks(display)

    # Sub-draws
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
        for attack in self.attack_list:
            attack.draw(display)

    # Update ------------------------------------------------------ #
    # Updates
    def update(self, player):
        self.facing(player)
        self.attack(player)
        self.hit_timer()
        self.delete_itself()

    def dead_update(self, player):
        self.update_attack(player)
        self.delete_itself()

    # Direction
    def facing(self, player):
        if self.rect.centerx - player.rect.centerx > 0:  # left
            self.direction = "left"
        else:  # right
            self.direction = "right"

    # Attack
    def attack(self, player):
        self.append_attack(player)
        self.update_attack(player)

    # Hit
    def hit_timer(self):
        if self.image_used == "hit":
            dt = time.perf_counter() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"

    # Functions --------------------------------------------------- #
    # Attacks
    def append_attack(self, player):
        dt = time.perf_counter() - self.last_attack
        if dt * 1000 >= self.attack_cooldown:  # cooldown
            target = (
                player.rect.centerx * window.enlarge,
                player.rect.centery * window.enlarge)

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
            self.delete = True
        
        self.image_used = "hit"
        self.last_hit = time.perf_counter()

    # Mana
    def mana_reward(self, mana_crystals):
        for _ in range(round(self.max_health * 1.5)):
            mana_crystals.append(ManaCrystal(self.rect.center))

    # Kill
    def delete_itself(self):
        if self.is_dead and len(self.attack_list) == 0:
            self.delete = True
