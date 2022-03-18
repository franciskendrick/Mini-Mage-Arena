from functions import clip_set_to_list_on_xaxis, palette_swap, rect_edge_collision
from functions import separate_sets_from_xaxis, separate_sets_from_yaxis
from supports import ManaCrystal
import pygame
import time
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class NormalKnight:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_direction()
        self.init_movement()
        self.init_hit()
        self.init_status()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/normal_knight.png")
        self.idx = 0

        # Palettes
        hit_palette = {
            (129, 151, 150): (235, 237, 233),
            (87, 114, 119): (199, 207, 204),
            (57, 74, 80): (168, 181, 178),
            (32, 46, 55): (129, 151, 150),
            (21, 29, 40): (87, 114, 119),
            (9, 10, 20): (9, 10, 20),
            (122, 72, 65): (168, 181, 178),
            (96, 44, 44): (129, 151, 150),
            (207, 87, 60): (235, 237, 233),
            (165, 48, 48): (168, 181, 178),
            (117, 36, 56): (129, 151, 150)}

        # Images
        walking_spriteset, attacking_spriteset = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))
        knight_walking, sword_walking = separate_sets_from_xaxis(
            walking_spriteset, (0, 255, 0))
        knight_attacking, sword_attacking = separate_sets_from_xaxis(
            attacking_spriteset, (0, 255, 0))

        self.images = {
            "sprite": {
                "walking": {
                    "default": clip_set_to_list_on_xaxis(knight_walking),
                    "hit": clip_set_to_list_on_xaxis(
                        palette_swap(knight_walking.convert(), hit_palette))
                },
                "attacking": {
                    "default": clip_set_to_list_on_xaxis(knight_attacking),
                    "hit": clip_set_to_list_on_xaxis(
                        palette_swap(knight_attacking.convert(), hit_palette))
                }
            },
            "sword": {
                "walking": {
                    "default": clip_set_to_list_on_xaxis(sword_walking),
                    "hit": clip_set_to_list_on_xaxis(
                        palette_swap(sword_walking.convert(), hit_palette)),
                },
                "attacking": {
                    "default": clip_set_to_list_on_xaxis(sword_attacking),
                    "hit": clip_set_to_list_on_xaxis(
                        palette_swap(sword_attacking.convert(), hit_palette)),
                }
            }
        }
        self.image_used = "default"
        self.doing = "walking"

    def init_rect(self):
        self.sword_offset = {
            "left": [-9, 2],
            "right": [12, 2]
        }

        # Sprite
        image = self.images["sprite"][self.doing][self.image_used]
        size = image[self.idx].get_rect().size
        self.rect = pygame.Rect(100, 100, *size)

        # Sword
        image = self.images["sword"][self.doing][self.image_used]
        size = image[self.idx].get_rect().size
        self.sword_rect = pygame.Rect(
            100 + self.sword_offset["right"][0], 
            100 + self.sword_offset["right"][1], 
            *size)

    def init_direction(self):
        self.direction = None

    def init_movement(self):
        self.vel = 2

    def init_hit(self):
        self.last_hit = time.perf_counter()
        self.hit_time = 300  # milliseconds
        self.is_hit = False

    def init_status(self):
        self.max_health = 30
        self.health = 30
        self.is_dead = False
        self.delete = False

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        imgs = self.images["sprite"][self.doing][self.image_used]
        if self.idx >= len(imgs) * 5:
            self.idx = 0

        # Draw
        self.draw_sprite(display)
        self.draw_sword(display)

        # Update
        self.idx += 1

    def draw_sword(self, display):
        # Images
        imgs = self.images["sprite"][self.doing][self.image_used]

        # Direction
        img = imgs[self.idx // 5]
        if self.direction == "left":
            img = pygame.transform.flip(img, True, False)

        # Draw
        display.blit(img, self.rect)

    def draw_sprite(self, display):
        # Images
        imgs = self.images["sword"][self.doing][self.image_used]

        # Direction
        img = imgs[self.idx // 5]
        if self.direction == "left":
            img = pygame.transform.flip(img, True, False)

        # Draw
        display.blit(img, self.sword_rect)

    # Update ------------------------------------------------------ #
    def update(self, player):
        self.facing(player)
        self.movement(player)
        self.hit_timer()

    # Direction
    def facing(self, player):
        # Update Direction
        if self.rect.centerx - player.rect.centerx > 0:  # left
            self.direction = "left"
        else:  # right
            self.direction = "right"
        
        # Update Sword Rectangle
        self.update_swordrect()

    # Movement
    def movement(self, player):
        self.move_left(player)
        self.move_right(player)
        self.move_up(player)
        self.move_down(player)

    # Hit
    def hit_timer(self):
        if self.is_hit:
            dt = time.perf_counter() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"
                self.is_hit = False

    # Functions --------------------------------------------------- #
    # Direction
    def update_swordrect(self):
        offset = self.sword_offset[self.direction]
        self.sword_rect = pygame.Rect(
            self.rect.x + offset[0], 
            self.rect.y + offset[1],
            *self.sword_rect.size)

    # Movement
    def move_left(self, player):
        # Handle Rectangles
        handle_sprite_rect = self.rect.copy()
        handle_sword_rect = self.sword_rect.copy()

        # Player in -x Axis
        if player.rect.centerx < self.rect.centerx - self.vel:
            # Move Enemy
            handle_sprite_rect.centerx -= self.vel 
            handle_sword_rect.centerx -= self.vel 

            # Not Colliding with a Wall 
            not_sprite_collision = not rect_edge_collision(handle_sprite_rect)
            not_sword_collision = not rect_edge_collision(handle_sword_rect)
            if not_sprite_collision and not_sword_collision:
                self.rect.centerx -= self.vel
                self.sword_rect.centerx -= self.vel

    def move_right(self, player):
        # Handle Rectangles
        handle_sprite_rect = self.rect.copy()
        handle_sword_rect = self.sword_rect.copy()

        # Player in +x Axis
        if player.rect.centerx > self.rect.centerx + self.vel:
            # Move Enemy
            handle_sprite_rect.centerx += self.vel
            handle_sword_rect.centerx += self.vel

            # Not Colliding with a Wall 
            not_sprite_collision = not rect_edge_collision(handle_sprite_rect)
            not_sword_collision = not rect_edge_collision(handle_sword_rect)
            if not_sprite_collision and not_sword_collision:
                self.rect.centerx += self.vel
                self.sword_rect.centerx += self.vel

    def move_up(self, player):
        # Handle Rectangles
        handle_sprite_rect = self.rect.copy()
        handle_sword_rect = self.sword_rect.copy()

        # Player in -y Axis
        if player.rect.centery < self.rect.centery - self.vel:
            # Move Enemy
            handle_sprite_rect.centery -= self.vel
            handle_sword_rect.centery -= self.vel

            # Not Colliding with a Wall 
            not_sprite_collision = not rect_edge_collision(handle_sprite_rect)
            not_sword_collision = not rect_edge_collision(handle_sword_rect)
            if not_sprite_collision and not_sword_collision:
                self.rect.centery -= self.vel
                self.sword_rect.centery -= self.vel

    def move_down(self, player):
        # Handle Rectangles
        handle_sprite_rect = self.rect.copy()
        handle_sword_rect = self.sword_rect.copy()

        # Player in +y Axis
        if player.rect.centery > self.rect.centery - self.vel:
            # Move Enemy
            handle_sprite_rect.centery += self.vel
            handle_sword_rect.centery += self.vel

            # Not Colliding with a Wall 
            not_sprite_collision = not rect_edge_collision(handle_sprite_rect)
            not_sword_collision = not rect_edge_collision(handle_sword_rect)
            if not_sprite_collision and not_sword_collision:
                self.rect.centery += self.vel
                self.sword_rect.centery += self.vel

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
