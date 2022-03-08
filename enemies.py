from functions import *
from windows import window
from enemy_spells import DarkFireBall
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
            path + "/assets/sprites" + "/slime.png")
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
        self.last_attack = time.time()
        self.attack_cooldown = 750  # milliseconds

    def init_hit(self):
        self.last_hit = time.time()
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
            dt = time.time() - self.last_attack
            if dt * 1000 >= self.attack_cooldown:  # cooldown
                player.hit(self.damage)
                self.last_attack = time.time()

    # Hit
    def hit_timer(self):
        if self.image_used == "hit":
            dt = time.time() - self.last_hit
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

        self.image_used = "hit"
        self.last_hit = time.time()

    # Mana
    def mana_reward(self, mana_crystals):
        for _ in range(round(self.max_health * 1.5)):
            mana_crystals.append(ManaCrystal(self.rect.center))


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
            path + "/assets/sprites" + "/dark_mage.png")
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
        self.last_attack = time.time()
        self.attack_cooldown = 1_200  # milliseconds

    def init_hit(self):
        self.last_hit = time.time()
        self.hit_time = 300  # milliseconds

    def init_status(self):
        self.max_health = 20
        self.health = 20
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
        self.append_attack(player)
        self.update_attack(player)

    # Hit
    def hit_timer(self):
        if self.image_used == "hit":
            dt = time.time() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"

    # Functions --------------------------------------------------- #
    # Attacks
    def append_attack(self, player):
        dt = time.time() - self.last_attack
        if dt * 1000 >= self.attack_cooldown:  # cooldown
            target = (
                player.rect.centerx * window.enlarge,
                player.rect.centery * window.enlarge)

            attack = DarkFireBall(self.rect.center, target)
            
            self.attack_list.append(attack)
            self.last_attack = time.time()

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
        self.last_hit = time.time()

    # Mana
    def mana_reward(self, mana_crystals):
        for _ in range(round(self.max_health * 1.5)):
            mana_crystals.append(ManaCrystal(self.rect.center))


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
            path + "/assets/sprites" + "/mushroom.png")
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
        self.last_attack = time.time()
        self.attack_cooldown = 1_000  # milliseconds

    def init_hit(self):
        self.last_hit = time.time()
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
            dt = time.time() - self.last_attack
            if dt * 1000 >= self.attack_cooldown:  # cooldown
                player.hit(self.damage)
                self.last_attack = time.time()
        else:
            self.range_visibility = False

    # Hit
    def hit_timer(self):
        if self.image_used == "hit":
            dt = time.time() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"

    # Functions --------------------------------------------------- #
    # Hit
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True

        self.image_used = "hit"
        self.last_hit = time.time()

    # Mana
    def mana_reward(self, mana_crystals):
        for _ in range(round(self.max_health * 1.5)):
            mana_crystals.append(ManaCrystal(self.rect.center))


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
            path + "/assets/sprites" + "/fireshroom.png")
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
        self.last_attack = time.time()
        self.attack_cooldown = 1_200  # milliseconds

    def init_hit(self):
        self.last_hit = time.time()
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
            dt = time.time() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"

    # Functions --------------------------------------------------- #
    # Attacks
    def append_attack(self):
        dt = time.time() - self.last_attack
        if dt * 1000 >= self.attack_cooldown:  # cooldown
            for target in self.targets:
                attack = DarkFireBall(self.rect.center, target)
            
                self.attack_list.append(attack)
                self.last_attack = time.time()

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
        self.last_hit = time.time()

    # Mana
    def mana_reward(self, mana_crystals):
        for _ in range(round(self.max_health * 1.5)):
            mana_crystals.append(ManaCrystal(self.rect.center))


class Boomshroom:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.is_dead = False

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            path + "/assets/sprites" + "/boomshroom.png")
        self.idx = 0

        # Palettes
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
            "hit": clip_set_to_list_on_xaxis(
                palette_swap(spriteset.convert(), hit_palette))
        }
        self.image_used = "default"

    def init_rect(self):
        size = self.images[self.image_used][self.idx].get_rect().size
        self.rect = pygame.Rect(100, 100, *size)

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        imgs = self.images[self.image_used]
        if self.idx >= len(imgs) * 5:
            self.idx = 0

        # Draw
        img = imgs[self.idx // 5]
        display.blit(img, self.rect)

        # Update
        self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self, player):
        pass

    # Functions --------------------------------------------------- #
