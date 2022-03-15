from functions import clip_set_to_list_on_xaxis, palette_swap, rect_edge_collision
from supports import ManaCrystal
import pygame
import time
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class Slime:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_direction()
        self.init_movement()
        self.init_attack()
        self.init_hit()
        self.init_status()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/slime.png")
        self.idx = 0

        # Palettes
        hit_palette = {
            (9, 10, 20): (9, 10, 20),
            (60, 94, 139): (168, 181, 178),
            (79, 143, 186): (199, 207, 204),
            (115, 190, 211): (235, 237, 233),
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

    def init_movement(self):
        self.vel = 2

    def init_attack(self):
        # Damage
        self.damage = 1
        
        # Time
        self.last_attack = time.perf_counter()
        self.attack_cooldown = 750  # milliseconds

    def init_hit(self):
        self.last_hit = time.perf_counter()
        self.hit_time = 300  # milliseconds

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

        # Update
        self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self, player):
        self.facing(player)
        self.movement(player)
        self.attack(player)
        self.hit_timer()

    # Direction
    def facing(self, player):
        if self.rect.centerx - player.rect.centerx > 0:  # left
            self.direction = "left"
        else:  # right
            self.direction = "right"

    # Movement
    def movement(self, player):
        self.move_left(player)
        self.move_right(player)
        self.move_up(player)
        self.move_down(player)

    # Attack
    def attack(self, player):
        if self.rect.colliderect(player.rect):
            dt = time.perf_counter() - self.last_attack
            if dt * 1000 >= self.attack_cooldown:  # cooldown
                player.hit(self.damage)
                self.last_attack = time.perf_counter()

    # Hit
    def hit_timer(self):
        if self.image_used == "hit":
            dt = time.perf_counter() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"

    # Functions --------------------------------------------------- #
    # Movement
    def move_left(self, player):
        handle_rect = self.rect.copy()
        if player.rect.centerx < self.rect.centerx - self.vel:
            handle_rect.centerx -= self.vel
            if not rect_edge_collision(handle_rect):
                self.rect.centerx -= self.vel

    def move_right(self, player):
        handle_rect = self.rect.copy()
        if player.rect.centerx > self.rect.centerx + self.vel:
            handle_rect.centerx += self.vel
            if not rect_edge_collision(handle_rect):
                self.rect.centerx += self.vel

    def move_up(self, player):
        handle_rect = self.rect.copy()
        if player.rect.centery < self.rect.centery - self.vel:
            handle_rect.centery -= self.vel
            if not rect_edge_collision(handle_rect):
                self.rect.centery -= self.vel

    def move_down(self, player):
        handle_rect = self.rect.copy()
        if player.rect.centery > self.rect.centery + self.vel:
            handle_rect.centery += self.vel
            if not rect_edge_collision(handle_rect):
                self.rect.centery += self.vel

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
