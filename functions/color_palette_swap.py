import pygame

pygame.init()


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
