from windows import window
import pygame

pygame.init()


class StatusBar:
    def draw(self, display):
        self.draw_background(display)

    def draw_background(self, display):
        pygame.draw.rect(display, (16, 20, 31), window.statbar_rect)


status_bar = StatusBar()
