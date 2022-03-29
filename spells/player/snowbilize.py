from functions import Circle, circle_edge_collision
from windows import window
import pygame
import math
import time

pygame.init()


class Snowbilize:
    # Initialize -------------------------------------------------- #
    def __init__(self, origin, target):
        self.circle = Circle(origin, 4)
        self.init_color()
        self.init_movement(target)
        self.init_attack()
        self.init_freeze()
        self.mana_cost = 6
        self.collided = False

    def init_color(self):
        self.color = (164, 221, 219)

    def init_movement(self, target):
        target_x, target_y = target
        self.speed = 6
        angle = math.atan2(
            target_y - self.circle.center[1] * window.enlarge, 
            target_x - self.circle.center[0] * window.enlarge)
        self.x_vel = math.cos(angle)
        self.y_vel = math.sin(angle)

    def init_attack(self):
        self.direct_damage = 5
        self.indirect_damage = 1

    def init_freeze(self):
        # Range
        self.freeze_radius = 64
        self.enemies_freezing = []

        # Time
        self.time_of_freeze = None
        self.freeze_cooldown = 5000  # milliseconds

    def draw(self, display):
        center = self.circle.center
        radius = self.circle.radius
        pygame.draw.circle(display, self.color, center, radius)

    # Update ------------------------------------------------------ #
    def update(self, enemies):
        if not self.collided:
            self.movement()
            self.wall_collision()
            self.entity_collision(enemies)

    # Movement
    def movement(self):
        self.circle.center[0] += (self.x_vel * self.speed)
        self.circle.center[1] += (self.y_vel * self.speed)

    # Collisions
    def wall_collision(self):
        if circle_edge_collision(self.circle):
            self.collided = True

    def entity_collision(self, enemies):
        for enemy in enemies:
            if self.circle.colliderect(enemy.rect):
                self.collided = True

                # Freeze
                self.time_of_freeze = time.perf_counter()
                enemy.hit(self.direct_damage)
                enemy.immobilized = True
                enemy.image_used = "immobilized"

                hit_enemy = enemy

                # Freeze Surrounding Enemies
                freeze_range = self.get_freeze_range(hit_enemy)
                handle_enemies = enemies.copy()
                handle_enemies.remove(hit_enemy)
                for enemy in handle_enemies:
                    if freeze_range.colliderect(enemy.rect):
                        # Freeze
                        self.enemies_freezing.append(enemy)
                        enemy.hit(self.indirect_damage)
                        enemy.immobilized = True
                        enemy.image_used = "immobilized"

                break

    # Functions --------------------------------------------------- #
    def get_freeze_range(self, enemy):
        radius = (max(enemy.rect.width, enemy.rect.height) / 2) + self.freeze_radius
        freeze_range = Circle(enemy.rect.center, radius)

        return freeze_range
