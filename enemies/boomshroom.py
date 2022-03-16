from functions import Circle, clip_set_to_list_on_xaxis, palette_swap
from supports import ManaCrystal
from windows import window
import pygame
import time
import os

pygame.init()
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
        self.alpha_surface = pygame.Surface(
            window.rect.size, pygame.SRCALPHA)

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

        # Explosion
        explosion_set = pygame.image.load(
            f"{path}/assets/boomshroom_explosion.png")
        self.explosion_images = clip_set_to_list_on_xaxis(explosion_set)
        self.explosion_idx = 0

    def init_rect(self):
        # Sprite
        size = self.images[self.image_used][self.idx].get_rect().size
        self.rect = pygame.Rect(100, 100, *size)

        # Explosion
        explosion_offset = [-9, -19]
        self.resized_explosion_offset = [-10, -19]
        size = self.explosion_images[self.explosion_idx].get_rect().size
        self.explosion_rect = pygame.Rect(
            100 + explosion_offset[0], 100 + explosion_offset[1], *size)

    def init_direction(self):
        self.direction = None

    def init_attack(self):
        # Range
        self.inner_attack_range = Circle(
            self.rect.center, 80)
        self.middle_attack_range = Circle(
            self.rect.center, 160)
        self.outer_attack_range = Circle(
            self.rect.center, 320)
        
        # Trigger
        self.triggered = False

        # Blink
        self.last_blink = time.perf_counter()
        self.time_fuze = 750  # milliseconds
        self.blink_count = 0
        self.blink = False

    def init_hit(self):
        self.last_hit = time.perf_counter()
        self.hit_time = 300  # milliseconds
        self.is_hit = False

    def init_status(self):
        self.max_health = 12
        self.health = 12
        self.is_dead = False
        self.exploded = False
        self.delete = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        if not self.exploded:
            if not self.is_dead:
                if self.blink:
                    self.draw_blink(display)
                self.draw_sprite(display)
        else:
            self.draw_explosion(display)

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

    def draw_blink(self, display):
        # Outer Circle
        center = self.outer_attack_range.center
        radius = self.outer_attack_range.radius
        border_width = radius - self.middle_attack_range.radius
        pygame.draw.circle(
            self.alpha_surface, (255, 255, 0, 80), center, radius, border_width)

        # Middle Circle
        center = self.middle_attack_range.center
        radius = self.middle_attack_range.radius
        border_width = radius - self.inner_attack_range.radius
        pygame.draw.circle(
            self.alpha_surface, (255, 165, 0, 80), center, radius, border_width)

        # Inner Circle
        center = self.inner_attack_range.center
        radius = self.inner_attack_range.radius
        pygame.draw.circle(
            self.alpha_surface, (255, 0, 0, 80), center, radius)

        # Blit on Display 
        display.blit(self.alpha_surface, (0, 0))

    def draw_explosion(self, display):
        # Image & Rectangle
        img = self.explosion_images[self.explosion_idx // 5]
        rect = self.explosion_rect.copy()
        if self.explosion_idx // 5 >= 4:
            # Image
            wd, ht = self.explosion_rect.size
            img = pygame.transform.scale(
                img, (wd * 3, ht * 3))

            # Rectangle
            rect.x += self.resized_explosion_offset[0] * 3
            rect.y += self.resized_explosion_offset[1] * 3

        # Draw
        display.blit(img, rect)

        # Update
        if self.explosion_idx < (len(self.explosion_images) - 1) * 5:
            self.explosion_idx += 1

    # Update ------------------------------------------------------ #
    # Updates
    def update(self, player):
        self.facing(player)
        self.attack(player)
        self.hit_timer()
        self.delete_itself()

    def dead_update(self, _):
        self.delete_itself()

    # Direction
    def facing(self, player):
        if self.rect.centerx - player.rect.centerx > 0:  # left
            self.direction = "left"
        else:  # right
            self.direction = "right"

    # Attack
    def attack(self, player):
        self.trigger_detection(player)
        self.update_fuze(player)

    # Hit 
    def hit_timer(self):
        if self.is_hit:
            dt = time.perf_counter() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default" if not self.blink else "blink"
                self.is_hit = False

    # Functions --------------------------------------------------- #
    # Attack
    def trigger_detection(self, player):
        if self.inner_attack_range.colliderect(player.rect):
            self.triggered = True

    def update_fuze(self, player):
        if self.triggered and self.blink_count / 2 < 3:
            dt = time.perf_counter() - self.last_blink
            if dt * 1000 >= self.time_fuze:
                self.blink = not self.blink
                if self.is_hit:
                    self.image_used = "hit"
                elif self.blink:
                    self.image_used = "blink"
                else:
                    self.image_used = "default"

                self.blink_count += 1
                self.last_blink = time.perf_counter()
        elif not self.exploded and self.blink_count / 2 >= 3:
            self.explode(player)

    def explode(self, player):
        # Hit Player
        if self.inner_attack_range.colliderect(player.rect):
            player.hit(10)
        elif self.middle_attack_range.colliderect(player.rect):
            player.hit(5)
        elif self.outer_attack_range.colliderect(player.rect):
            player.hit(3)

        # Change Status
        self.exploded = True
        self.is_dead = True

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
        if not self.exploded:
            for _ in range(round(self.max_health * 1.5)):
                mana_crystals.append(ManaCrystal(self.rect.center))

    # Kill
    def delete_itself(self):
        in_last_frame = self.explosion_idx // 5 == len(self.explosion_images) * 5
        if self.is_dead and self.exploded and in_last_frame:
            self.delete = True
