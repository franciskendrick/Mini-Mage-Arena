import pygame

pygame.init()


class Window:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 640, 360)
        self.enlarge = 2

        # Framerate
        self.framerate = 30


window = Window()
