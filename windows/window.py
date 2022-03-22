import pygame

pygame.init()


class Window:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 640, 360)
        self.enlarge = 2

        # Framerate
        self.framerate = 30

        # Game
        self.arena_rect = pygame.Rect(15, 43, 610, 306)
        self.statbar_rect = pygame.Rect(0, 0, 640, 38)


window = Window()
