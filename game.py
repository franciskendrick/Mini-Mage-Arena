from functions import *
from windows import window
import pygame
import json
import os

pygame.init()
path = os.path.dirname(os.path.realpath(__file__))

# Window
win_size = (
    window.rect.width * window.enlarge,
    window.rect.height * window.enlarge)
win = pygame.display.set_mode(win_size)


class Game:
    def draw_statbar_bg(self, display):
        pygame.draw.rect(display, (16, 20, 31), window.statbar_rect)


game = Game()
