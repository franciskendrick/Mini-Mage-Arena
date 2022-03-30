from functions import clip_set_to_list_on_xaxis, palette_swap, rect_edge_collision
from spells.player import FireBall, Snowbilize
from windows import window
import pygame
import time
import os

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
        self.init_hit()
        self.init_status()
        self.init_healthregen()
        self.init_manaregen()

    def init_images(self):
        # Spriteset
        spriteset = pygame.image.load(
            f"{path}/assets/player.png")
        self.idx = 0

        # Palettes
        hit_palette = {
            (9, 10, 20): (65, 29, 49),
            (30, 29, 57): (117, 36, 56),
            (64, 39, 81): (165, 48, 48),
            (122, 54, 123): (207, 87, 60),
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
        self.rect = pygame.Rect(312, 203, *size)

    def init_direction(self):
        self.direction = None

    def init_movement(self):
        # Velocities
        self.walk_vel = 3
        self.sprint_vel = 5

        # Time
        self.last_sprint = time.perf_counter()
        self.stamina_degenerate = 500  # milliseconds
        self.stamina_regenerate = 500  # milliseconds

    def init_attack(self):
        # Spell in Use
        self.spells_available = {
            "fireball": FireBall,
            "snowbilize": Snowbilize
        }
        self.spell_in_use = self.spells_available["snowbilize"]

        # Attack Lists
        self.attack_list = []
        self.update_attack_list = []
        
        # Time 
        self.last_attack = time.perf_counter()
        self.attack_cooldown = 500  # milliseconds

    def init_hit(self):
        self.last_hit = time.perf_counter()
        self.hit_time = 300  # milliseconds 

    def init_status(self):
        self.maximum_stats = {
            "health": 20,
            "mana": 120,
            "stamina": 20}
        self.stats = self.maximum_stats.copy()

    def init_healthregen(self):
        self.last_healthregen = 0
        self.healthregen_cooldown = 5000  # milliseconds

    def init_manaregen(self):
        self.last_manaregen = 0
        self.manaregen_cooldown = 2000  # milliseconds

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
    def update(self, enemies):
        self.facing()
        self.movement()
        self.attacks(enemies)
        self.hit_timer()
        self.regenerate_health()
        self.regenerate_mana()

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
    def attacks(self, enemies):
        self.append_attack()
        self.update_attack(enemies)

    # Hit
    def hit_timer(self):
        if self.image_used == "hit":
            dt = time.perf_counter() - self.last_hit
            if dt * 1000 >= self.hit_time:
                self.image_used = "default"
                self.last_healthregen = time.perf_counter()

    # Health Regen
    def regenerate_health(self):
        if self.last_healthregen and self.stats["health"] < self.maximum_stats["health"]:
            dt = time.perf_counter() - self.last_healthregen
            if dt * 1000 >= self.healthregen_cooldown:
                self.stats["health"] += 1
                self.last_healthregen = time.perf_counter()

    # Mana Regen
    def regenerate_mana(self):
        if self.last_manaregen and self.stats["mana"] < self.maximum_stats["mana"]:
            dt = time.perf_counter() - self.last_manaregen
            if dt * 1000 >= self.manaregen_cooldown:
                self.stats["mana"] += 1
                self.last_manaregen = time.perf_counter()

    # Functions --------------------------------------------------- #
    # Movement
    def get_velocity(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:  # shift is down
            if self.stats["stamina"] > 0:  # still has stamina
                vel = self.sprint_vel

                # Update Stamina Stat
                dt = time.perf_counter() - self.last_sprint
                if dt * 1000 >= self.stamina_degenerate:
                    self.stats["stamina"] -= 1
                    self.last_sprint = time.perf_counter()
            else:  # no stamina
                vel = self.walk_vel
        else:  # shift is up
            vel = self.walk_vel

            # Update Stamina Stat
            dt = time.perf_counter() - self.last_sprint
            if dt * 1000 >= self.stamina_regenerate:
                if self.stats["stamina"] < 20:
                    self.stats["stamina"] += 1
                self.last_sprint = time.perf_counter()
            
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
            dt = time.perf_counter() - self.last_attack
            if dt * 1000 >= self.attack_cooldown:  # cooldown
                spell_arguments = {
                    FireBall: (self.rect.center, pygame.mouse.get_pos()),
                    Snowbilize: (self.rect.center, pygame.mouse.get_pos())
                }

                # Attack
                arguments = spell_arguments[self.spell_in_use]
                attack = self.spell_in_use(*arguments)

                if self.stats["mana"] - attack.mana_cost >= 0:  # enough mana
                    # Append
                    self.attack_list.append(attack)

                    # Mana
                    self.stats["mana"] -= attack.mana_cost

                    # Time
                    self.last_attack = time.perf_counter()
                    self.last_manaregen = time.perf_counter()

    def update_attack(self, enemies):
        # Attack List
        remove_attack = []
        for attack in self.attack_list:
            attack.update(enemies)
            if attack.collided:
                if not attack.delete:
                    self.update_attack_list.append(attack)
                remove_attack.append(attack)

        for attack in remove_attack:
            self.attack_list.remove(attack)

        # Update Attack List
        print(len(self.update_attack_list))
        remove_attack = []
        for attack in self.update_attack_list:
            attack.update(enemies)
            if attack.delete:
                remove_attack.append(attack)

        for attack in remove_attack:
            self.update_attack_list.remove(attack)

    # Hit
    def hit(self, damage):
        self.stats["health"] -= damage

        self.image_used = "hit"
        self.last_hit = time.perf_counter()

    # Support 
    def add_health(self, points):
        self.stats["health"] += points
        if self.stats["health"] >= self.maximum_stats["health"]:
            self.stats["health"] = self.maximum_stats["health"]

    def add_mana(self, points):
        self.stats["mana"] += points
        if self.stats["mana"] >= self.maximum_stats["mana"]:
            self.stats["mana"] = self.maximum_stats["mana"]
