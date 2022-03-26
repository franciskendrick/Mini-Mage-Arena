from .color_palette_swap import palette_swap
import pygame


def get_shadow(img, rect, shadow_offset, shadow_color=(57, 74, 80)):
    # Get Palette
    handle_img = img.copy()
    palette = {}
    for x in range(handle_img.get_width()):
        for y in range(handle_img.get_height()):
            color = handle_img.get_at((x, y))

            # if solid, and not in palette
            if color[3] != 0 and tuple(color) not in palette:
                palette[tuple(color)] = shadow_color

    # Palette Swap & Rectangle
    x_offset, y_offset = shadow_offset
    shadow_rect = pygame.Rect(rect.x + x_offset, rect.y + y_offset, *rect.size)
    shadow = palette_swap(handle_img.convert(), palette)

    # Return
    return shadow, shadow_rect
