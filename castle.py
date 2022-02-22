import pygame
import math
from bullet import Bullet


# Castle class
class Castle:

    def __init__(self,  screen, image100, image50, image25, x, y, scale):
        self.screen = screen
        self.health = 1000
        self.max_health = self.health
        self.fired = False
        self.money = 0
        self.score = 0

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (
            int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self, bullet_group):
        bullet_img = pygame.image.load('img/button/bullet.png').convert_alpha()
        b_w = bullet_img.get_width()
        b_h = bullet_img.get_height()
        bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.075), int(b_h * 0.075)))

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0]
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1] > 70:
            self.fired = True
            bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            bullet_group.add(bullet)
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

    def draw(self):
        if self.health <= 250:
            self.image = self.image25
        elif self.health <= 500:
            self.image = self.image50
        else:
            self.image = self.image100

        self.screen.blit(self.image, self.rect)

    def repair(self):
        if self.money >= 1000 and self.health < self.max_health:
            self.health += 500
            self.money -= 1000
            from main import castle
            if castle.health > castle.max_health:
                castle.health = castle.max_health

    def armour(self):
        if self.money >= 500 and self.health < self.max_health:
            self.max_health += 250
            self.money -= 500
