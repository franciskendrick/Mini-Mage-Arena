from windows import window
import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath("main.py"))


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
