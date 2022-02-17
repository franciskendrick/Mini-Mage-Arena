from windows import window
import pygame
import math
import os

pygame.init()
path = os.path.dirname(os.path.realpath("main.py"))


class Circle:
    def __init__(self, center, radius):
        self.center = list(center)
        self.radius = radius

    # Collision
    def colliderect(self, rect):
        distance_x = abs(self.center[0] - rect.centerx)
        distance_y = abs(self.center[1] - rect.centery)
        if distance_x > rect.width / 2 + self.radius or distance_y > rect.height / 2 + self.radius:
            return False
        if distance_x <= rect.width / 2 or distance_y <= rect.height / 2:
            return True

        corner_x = distance_x - rect.width / 2
        corner_y = distance_y - rect.height / 2
        corner_distance_sq = corner_x ** 2 + corner_y ** 2
        return corner_distance_sq <= self.radius ** 2

    def collidecircle(self, circle):
        x1, y1 = self.center
        x2, y2 = circle.center

        distance = math.hypot(x2 - x1, y2 - y1)
        if distance < self.radius + circle.radius:
            return True
        else:
            return False

    def collidepoint(self, point):
        p_x, p_y = point
        self_x, self_y = self.center

        distance = math.hypot(self_x - p_x, self_y - p_y)
        if distance <= self.radius:
            return True
        else:
            return False


# Clip Image
def clip(set, pos, size):
    clip_rect = pygame.Rect(pos, size)
    set.set_clip(clip_rect)
    img = set.subsurface(set.get_clip())

    return img


def clip_set_to_list(set):
    images = []

    # Loop Over every Pixel in Tileset
    for y in range(set.get_height()):
        for x in range(set.get_width()):
            pixel = set.get_at((x, y))

            # A Sprite/Tile is Found
            if pixel == (255, 0, 255, 255):  # magenta
                wd = 0
                ht = 0

                # Find the End of Sprites/Tiles in the X Coordinate
                while True:
                    wd += 1
                    pixel = set.get_at((x + wd, y))
                    if pixel == (0, 255, 255, 255):  # cyan
                        break

                # Find the End of Sprites/Tiles in the Y Coordinate
                while True:
                    ht += 1
                    pixel = set.get_at((x, y + ht))
                    if pixel == (0, 255, 255, 255):  # cyan
                        break

                # Clip Image
                img = clip(
                    set,
                    (x + 1, y + 1),
                    (wd - 1, ht - 1))

                # Append
                images.append(img)
    
    # Unpack Images if Less Than One
    [images] = [images] if len(images) > 1 else images

    return images


# Collisions
def edge_collision(entity_hitbox):
    left = window.rect.left < entity_hitbox.left
    right = window.rect.right > entity_hitbox.right
    top = window.rect.top < entity_hitbox.top
    bottom = window.rect.bottom > entity_hitbox.bottom

    if left and right and top and bottom:
        return False
    else:
        return True
