from windows import window
import pygame
import math
import os

pygame.init()
path = os.path.dirname(os.path.realpath("main.py"))


# Clip Image
def clip(set, pos, size):
    clip_rect = pygame.Rect(pos, size)
    set.set_clip(clip_rect)
    img = set.subsurface(set.get_clip())

    return img


# Clip ImageSet to List
def clip_set_to_list_on_xaxis(set):
    images = []

    # Loop Over every Pixel in Tileset
    for x in range(set.get_width()):
        pixel = set.get_at((x, 0))

        # A Sprite/Tile is Found
        if pixel == (255, 0, 255, 255):  # magenta
            wd = 0
            ht = 0

            # Find the End of Sprites/Tiles in the X Coordinate
            while True:
                wd += 1
                pixel = set.get_at((x + wd, 0))
                if pixel == (0, 255, 255, 255):  # cyan
                    break

            # Find the End of Sprites/Tiles in the Y Coordinate
            while True:
                ht += 1
                pixel = set.get_at((x, ht))
                if pixel == (0, 255, 255, 255):  # cyan
                    break

            # Clip Image
            img = clip(
                set,
                (x + 1, 1),
                (wd - 1, ht - 1))

            # Append
            images.append(img)

    # Unpack Images if Less Than One
    [images] = [images] if len(images) > 1 else images

    return images


def clip_set_to_list_on_yaxis(set):
    images = []

    # Loop Over every Pixel in Tileset
    for y in range(set.get_height()):
        pixel = set.get_at((0, y))

        # A Sprite/Tile is Found
        if pixel == (255, 0, 255, 255):  # magenta
            wd = 0
            ht = 0

            # Find the End of Sprites/Tiles in the X Coordinate
            while True:
                wd += 1
                pixel = set.get_at((wd, y))
                if pixel == (0, 255, 255, 255):  # cyan
                    break

            # Find the End of Sprites/Tiles in the Y Coordinate
            while True:
                ht += 1
                pixel = set.get_at((0, y + ht))
                if pixel == (0, 255, 255, 255):  # cyan
                    break

            # Clip Image
            img = clip(
                set,
                (1, y + 1),
                (wd - 1, ht - 1))

            # Append
            images.append(img)

    # Unpack Images if Less Than One
    [images] = [images] if len(images) > 1 else images

    return images


# Clip ImageSet to Dictionary
def clip_set_to_dict_on_xaxis(sets, order):
    dict_images = {}
    for name, set in zip(order, sets):
        image = clip_set_to_list_on_xaxis(set)
        dict_images[name] = image
    
    return dict_images


def clip_set_to_dict_on_yaxis(sets, order):
    dict_images = {}
    for name, set in zip(order, sets):
        image = clip_set_to_list_on_yaxis(set)
        dict_images[name] = image
    
    return dict_images


# Separate ImageSets
def separate_sets_from_xaxis(set_img, separator_color):
    separated_sets = []
    current_wd = 0
    for x in range(set_img.get_width()):
        pixel = set_img.get_at((x, 0))

        # Found a Separator
        if pixel == separator_color:
            # Clip Image
            set = clip(
                set_img,
                (x - current_wd, 0),
                (current_wd, set_img.get_height()))

            # Append
            separated_sets.append(set)
            current_wd = 0
        else:
            current_wd += 1 

    return separated_sets


def separate_sets_from_yaxis(set_img, separator_color):
    separated_sets = []
    current_ht = 0
    for y in range(set_img.get_height()):
        pixel = set_img.get_at((0, y))

        # Found a Separator
        if pixel == separator_color:
            # Clip Image
            set = clip(
                set_img,
                (0, y - current_ht),
                (set_img.get_width(), current_ht))

            # Append
            separated_sets.append(set)
            current_ht = 0
        else:
            current_ht += 1 

    return separated_sets


# Palette Swap
def color_swap(img, old_color, new_color):
    handle_img = pygame.Surface(img.get_size())
    handle_img.fill(new_color)
    img.set_colorkey(old_color)
    handle_img.blit(img, (0, 0))

    return handle_img


def palette_swap(img, palette):
    for old_color in palette:
        new_color = palette[old_color]
        img = color_swap(img, old_color, new_color)
    img.set_colorkey((0, 0, 0))

    return img


# Collisions
def rect_edge_collision(rect):
    left = window.arena_rect.left < rect.left
    right = window.arena_rect.right > rect.right
    top = window.arena_rect.top < rect.top
    bottom = window.arena_rect.bottom > rect.bottom

    if left and right and top and bottom:
        return False
    else:
        return True


def circle_edge_collision(circle):
    left = window.arena_rect.left < circle.center[0] - circle.radius
    right = window.arena_rect.right > circle.center[0] + circle.radius
    top = window.arena_rect.top < circle.center[1] - circle.radius
    bottom = window.arena_rect.bottom > circle.center[1] + circle.radius

    if left and right and top and bottom:
        return False
    else:
        return True
