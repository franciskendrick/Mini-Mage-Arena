from windows import window


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
