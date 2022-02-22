import pygame
import math
import random


class Crosshair:
    def __init__(self, scale):
        image = pygame.image.load('img/button/crosshair.png')
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

        # pygame.mouse.set_visible(False)

    def draw(self, screen):
        mx, my = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        screen.blit(self.image, self.rect)
