import pygame
import math

from main import SCREEN_WIDTH, SCREEN_HEIGHT


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 10

        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
        if self.rect.right < 0 \
                or self.rect.left > SCREEN_WIDTH \
                or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        self.rect.x += self.dx
        self.rect.y += self.dy
