from functions import *
from windows import window
from spells import FireBall
import pygame
import os
import time

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

    
class Player:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_direction()
        self.init_movement()
        self.init_attack()
        self.init_status()

    def init_images(self):
        spriteset = pygame.image.load(
            path + "/assets/sprites" + "/player_mage.png")
        self.idx = 0

        self.images = clip_set_to_list(spriteset)

    def init_rect(self):
        size = self.images[self.idx].get_rect().size
        self.rect = pygame.Rect(320, 180, *size)

    def init_direction(self):
        self.direction = None

    def init_movement(self):
        # Velocities
        self.walk_vel = 3
        self.sprint_vel = 5

        # Time
        self.last_sprint = time.time()
        self.stamina_time = 500  # milliseconds

    def init_attack(self):
        # Spell in Use
        self.spells_available = {
            "fireball": FireBall
        }
        self.spell_in_use = self.spells_available["fireball"]

        # Attack Lists
        self.attack_list = []
        
        # Time 
        self.last_attack = time.time()
        self.attack_limit = 500  # milliseconds

    def init_status(self):
        self.maximum_stats = {
            "health": 20,
            "mana": 20,  # 120 !!!
            "stamina": 20}
        self.stats = self.maximum_stats.copy()

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        self.draw_sprite(display)
        self.draw_attacks(display)

    def draw_sprite(self, display):
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

    def draw_attacks(self, display):
        for attack in self.attack_list:
            attack.draw(display)

    # Update ------------------------------------------------------ #
    def update(self):
        self.facing()
        self.movement()
        self.attacks()

    # Direction
    def facing(self):
        m_x, _ = pygame.mouse.get_pos()
        if (self.rect.centerx * window.enlarge) - m_x > 0:  # left
            self.direction = "left" 
        else:  # right
            self.direction = "right" 

    # Movment
    def movement(self):
        keys = pygame.key.get_pressed()

        # Sprint
        vel = self.get_velocity()

        # Movement
        if keys[pygame.K_a]:  # left
            self.move_x(-vel)
        if keys[pygame.K_d]:  # right
            self.move_x(vel)
        if keys[pygame.K_w]:  # up
            self.move_y(-vel)
        if keys[pygame.K_s]:  # down
            self.move_y(vel)

    # Attacks
    def attacks(self):
        self.append_attack()
        self.update_attack()

    # Functions --------------------------------------------------- #
    # Movement
    def get_velocity(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:  # shift is down
            if self.stats["stamina"] > 0:  # still has stamina
                vel = self.sprint_vel

                # Update Stamina Stat
                dt = time.time() - self.last_sprint
                if dt * 1000 >= self.stamina_time:
                    self.stats["stamina"] -= 1
                    self.last_sprint = time.time()
            else:  # no stamina
                vel = self.walk_vel
        else:  # shift is up
            vel = self.walk_vel

            # Update Stamina Stat
            dt = time.time() - self.last_sprint
            if dt * 1000 >= self.stamina_time:
                if self.stats["stamina"] < 20:
                    self.stats["stamina"] += 1
                self.last_sprint = time.time()
            
        return vel

    def move_x(self, vel):
        handle_rect = self.rect.copy()
        handle_rect.x += vel
        if not rect_edge_collision(handle_rect):
            self.rect.x += vel

    def move_y(self, vel):
        handle_rect = self.rect.copy()
        handle_rect.y += vel
        if not rect_edge_collision(handle_rect):
            self.rect.y += vel

    # Attacks
    def append_attack(self):
        left_click, _, _ = pygame.mouse.get_pressed()
        if left_click:  # left click is pressed 
            dt = time.time() - self.last_attack
            if dt * 1000 >= self.attack_limit:  # spam limit
                spell_arguments = {
                    FireBall: (self.rect.center, pygame.mouse.get_pos())
                }

                arguments = spell_arguments[self.spell_in_use]
                attack = self.spell_in_use(*arguments)

                self.attack_list.append(attack)
                self.last_attack = time.time()

    def update_attack(self):
        remove_attack = []

        # Update Attacks
        for attack in self.attack_list:
            attack.update()
            if attack.collided:
                remove_attack.append(attack)

        # Remove Attacks
        for attack in remove_attack:
            self.attack_list.remove(attack)
