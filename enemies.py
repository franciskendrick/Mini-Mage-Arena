from functions import *
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
        spriteset = pygame.image.load(
            path + "/assets/sprites" + "/slime.png")
        self.idx = 0

        self.images = clip_set_to_list(spriteset)

    def init_rect(self):
        size = self.images[self.idx].get_rect().size
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
        self.attack_limit = 750  # milliseconds

    def init_hit(self):
        self.last_hit = time.time()
        self.hit_time = 300  # milliseconds

    def init_status(self):
        self.health = 12
        self.is_dead = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
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
    def update(self, player):
        self.facing(player)
        self.movement(player)
        self.attack(player)

    # Direction
    def facing(self, player):
        if self.rect.centerx - player.rect.centerx > 0:  # left
            self.direction = "left"
        else:  # face right
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
            if dt * 1000 >= self.attack_limit:  # spam limit
                player.hit(self.damage)
                self.last_attack = time.time()

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
