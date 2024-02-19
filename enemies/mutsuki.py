import pygame
import enemy
import random


class Mutsuki(enemy.Enemy):
    def __init__(self, speed, x, y, target):
        image = pygame.image.load('artwork/kufufu0.png').convert_alpha()
        self.hp = 1
        super().__init__(speed, image, x, y, target, hp=1, scale=1)

    def health_bar(self, screen):
        ratio = self.hp / self.max_hp

        pygame.draw.rect(screen, "black", (self.rect.x - 1, self.rect.y - 13, 32, 6))
        pygame.draw.rect(screen, "red", (self.rect.x, self.rect.y - 12, 30, 4))
        pygame.draw.rect(screen, "green", (self.rect.x, self.rect.y - 12, 30 * ratio, 4))