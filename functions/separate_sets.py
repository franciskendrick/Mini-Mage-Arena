from .clip_image import clip


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
