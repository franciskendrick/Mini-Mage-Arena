from functions import *
import pygame
import random
import math
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


class HealingPotion:
    # Initialize -------------------------------------------------- #
    def __init__(self):
        self.init_images()
        self.init_rect()
        self.init_points()
        self.absorbed = False

    def init_images(self):
        # Original Spriteset
        spriteset = pygame.image.load(
            path + "/assets/supports" + "/healing_potion.png")

        # Separated Spritesets
        self.order = ["small", "medium", "large"]
        potion_spritesets = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))
        self.mana_spritesets = clip_set_to_dict_on_xaxis(
            potion_spritesets, self.order)

        # Images
        self.type = 0
        self.images = self.mana_spritesets[self.order[self.type]]
        self.idx = 0

    def init_rect(self):
        img_rect = self.images[self.idx].get_rect()
        self.rect = pygame.Rect(200, 200, *img_rect.size)

    def init_points(self):
        points_map = {0: 2, 1: 4, 2: 6}
        self.points = points_map[self.type]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        if self.idx >= len(self.images) * 3:
            self.idx = 0

        # Draw
        img = self.images[self.idx // 3]
        display.blit(img, self.rect)

        # Update 
        self.idx += 1

    # Update ------------------------------------------------------ #
    def update(self, player):
        self.player_collision(player)

    # Collisions
    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.add_health(self.points)
            self.absorbed = True


class ManaCrystal:
    # Initialize -------------------------------------------------- #
    def __init__(self, center_pos):
        self.init_images()
        self.init_rect(center_pos)
        self.init_drop()
        self.init_playermagnet()
        self.init_points()
        self.absorbed = False

    def init_images(self):
        # Original Spriteset
        spriteset = pygame.image.load(
            path + "/assets/supports" + "/mana_crystals.png")

        # Separated Spritesets
        self.order = ["small", "medium", "large"]
        mana_spritesets = separate_sets_from_yaxis(
            spriteset, (255, 0, 0))
        self.mana_spritesets = clip_set_to_dict_on_xaxis(
            mana_spritesets, self.order)

        # Images
        self.type = 0
        self.images = self.mana_spritesets[self.order[self.type]]
        self.idx = 0

    def init_rect(self, center_pos):
        img_rect = self.images[self.idx].get_rect()
        self.rect = pygame.Rect(0, 0, *img_rect.size)
        self.rect.center = center_pos

    def init_drop(self):
        # Speed & Angle
        speed = random.randint(2, 5)
        angle = math.atan2(
            random.uniform(-1, 1),
            random.uniform(-1, 1))

        # Velocities
        x_vel = math.cos(angle) * speed
        y_vel = math.sin(angle) * speed
        self.drop_velocities = [x_vel, y_vel]

        # Status
        self.dropped = True        

    def init_playermagnet(self):
        # Range
        self.magent_range = Circle(
            self.rect.center, 56)

        # Distance
        keys = [key for key in range(56 + 1)]
        values = [value for value in reversed(range(56 + 1))]
        self.invert_distance = {
            key: value for key, value in zip(keys, values)}

    def init_points(self):
        self.points_map = {0: 1, 1: 4, 2: 16}
        self.points = self.points_map[self.type]

    # Draw -------------------------------------------------------- #
    def draw(self, display):
        # Reset
        if self.idx >= len(self.images) * 3:
            self.idx = 0

        # Draw
        img = self.images[self.idx // 3]
        display.blit(img, self.rect)

        # Update
        self.idx += 1

        # !!!
        center = self.magent_range.center
        radius = self.magent_range.radius
        pygame.draw.circle(display, (0, 0, 255), center, radius, 1)

    # Update ------------------------------------------------------ #
    def update(self, player, mana_crystals):
        self.movement(player, mana_crystals)
        self.player_collision(player)

    # Movement
    def movement(self, player, mana_crystals):
        if self.dropped:
            self.drop_movement()
        else:
            self.fusion_magnet(mana_crystals)
        self.player_magnet(player)

        self.magent_range.center = self.rect.center

    # Collisions
    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.add_mana(self.points)
            self.absorbed = True

    # Functions --------------------------------------------------- #
    # Drop 
    def drop_movement(self):
        # Get Velocities
        x_vel, y_vel = self.drop_velocities

        # Move
        self.move_x(x_vel)
        self.move_y(y_vel)

        # Modify X Velocity
        modify_x = random.uniform(0.2, 0.4)
        if x_vel > 0:  # positive
            x_vel = self.modify_positive_drop_xvel(
                x_vel, modify_x)
        else:  # negative
            x_vel = self.modify_negative_drop_xvel(
                x_vel, modify_x)

        # Modify Y Velocity
        modify_y = random.uniform(0.2, 0.4)
        if y_vel > 0:  # positive
            y_vel = self.modify_positive_drop_yvel(
                y_vel, modify_y)
        else:  # negative
            y_vel = self.modify_negative_drop_yvel(
                y_vel, modify_y)

        # Update Drop Velocities
        self.drop_velocities = [x_vel, y_vel]

        # Update Dropped
        if not x_vel and not y_vel:
            self.dropped = False

    def modify_positive_drop_xvel(self, x_vel, modify_x):
        if x_vel - modify_x <= 0:
            x_vel = 0
        else:
            x_vel -= modify_x

        return x_vel

    def modify_negative_drop_xvel(self, x_vel, modify_x):
        if x_vel + modify_x > 0:
            x_vel = 0
        else:
            x_vel += modify_x

        return x_vel

    def modify_positive_drop_yvel(self, y_vel, modify_y):
        if y_vel - modify_y <= 0:
            y_vel = 0
        else:
            y_vel -= modify_y

        return y_vel

    def modify_negative_drop_yvel(self, y_vel, modify_y):
        if y_vel + modify_y > 0:
            y_vel = 0
        else:
            y_vel += modify_y

        return y_vel

    # Fusion Magnet
    def fusion_magnet(self, mana_crystals):
        remove_mana = []
        handle_crystals = mana_crystals.copy()
        handle_crystals.remove(self)
        for mana in handle_crystals:
            # Current Not at Maximum 
            not_at_max = self.type < 2

            # New Mana is in Magnet Range of Current Mana
            newmana_in_magnetrange = self.magent_range.colliderect(mana.rect)
            # Current Mana and New Mana are Same Types 
            same_types = self.type == mana.type
            # "Current Points + Fusing Points" is in the Next Level of Crystals
            newpoint_in_nextlevel = not_at_max and self.points + mana.points <= self.points_map[self.type+1]
            
            # if All that has been Said is True
            if newmana_in_magnetrange and same_types and newpoint_in_nextlevel:
                # Current Mana has not Collided with New Mana 
                if not self.rect.colliderect(mana.rect):
                    # Move
                    x_vel, y_vel = self.get_velocities(mana.rect.center)
                    self.move_x(x_vel / 10)
                    self.move_y(y_vel / 10)
                # Mana has Collided with New Mana
                else:
                    # Fuse
                    self.points += mana.points
                    if self.points >= self.points_map[self.type+1]:
                        self.type += 1
                        self.images = self.mana_spritesets[self.order[self.type]]

                    mana.absorbed = True
                    remove_mana.append(mana)

        for mana in remove_mana:
            mana_crystals.remove(mana)

    # Mana to Player Magnet
    def player_magnet(self, player):
        if self.magent_range.colliderect(player.rect):
            x_vel, y_vel = self.get_velocities(player.rect.center)
            self.move_x(x_vel)
            self.move_y(y_vel)

    # Movement
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

    def get_velocities(self, target):
        target_x, target_y = target

        # Get Speed
        distance = math.hypot(
            self.rect.centerx - target_x, self.rect.centery - target_y)
        distance_lookup = int(round(distance / window.enlarge, 0))
        speed = self.invert_distance[distance_lookup] / 8

        # Get Direction
        angle = math.atan2(
            target_y - self.rect.centery,
            target_x - self.rect.centerx)

        # Get Velocities
        x_vel = math.cos(angle) * speed
        y_vel = math.sin(angle) * speed

        # Return
        return (x_vel, y_vel)
