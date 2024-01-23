import pygame
import enemy
import random


class Yuuka(enemy.Enemy):
    def __init__(self, speed, x, y, target):
        image = pygame.image.load('artwork/yuukafumo.png').convert_alpha()
        self.hp = 5
        super().__init__(speed, image, x, y, target, hp=5, scale=1)

    def movement(self):
        distance_x = self.target.rect.x - self.rect.x
        distance_y = self.target.rect.y - self.rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        if distance != 0:
            self.rect.x += self.speed * distance_x / distance
            self.rect.y += self.speed * distance_y / distance
