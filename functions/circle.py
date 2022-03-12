import math


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
