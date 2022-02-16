import pygame
import os

pygame.init()
path = os.path.dirname(os.path.realpath("main.py"))


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
