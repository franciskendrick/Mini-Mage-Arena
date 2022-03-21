from .clip_image import clip


def clip_set_to_list_on_xaxis(set, y=0):
    images = []

    # Loop Over every Pixel in Tileset
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


def clip_set_to_list_on_yaxis(set, x=0):
    images = []

    # Loop Over every Pixel in Tileset
    for y in range(set.get_height()):
        pixel = set.get_at((x, y))

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
                pixel = set.get_at((x, y + ht))
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
