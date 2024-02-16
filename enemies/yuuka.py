import pygame
import enemy
import random


class Yuuka(enemy.Enemy):
    def __init__(self, speed, x, y, target):
        image = pygame.image.load('artwork/yuukafumo.png').convert_alpha()
        self.hp = 3
        super().__init__(speed, image, x, y, target, hp=3, scale=1)

    def movement(self):
        distance_x = self.target.rect.x - self.rect.x
        distance_y = self.target.rect.y - self.rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        if distance != 0:
            self.rect.x += self.speed * distance_x / distance
            self.rect.y += self.speed * distance_y / distance

    def health_bar(self, screen):
        ratio = self.hp / self.max_hp

        pygame.draw.rect(screen, "black", (self.rect.x + 6, self.rect.y - 13, 52, 6))
        pygame.draw.rect(screen, "red", (self.rect.x + 7, self.rect.y - 12, 50, 4))
        pygame.draw.rect(screen, "green", (self.rect.x + 7, self.rect.y - 12, 50 * ratio, 4))