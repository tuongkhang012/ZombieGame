import pygame
import enemy
import random


class Mutsuki(enemy.Enemy):
    def __init__(self, speed, x, y, target):
        image = pygame.image.load('artwork/kufufu.png').convert_alpha()
        self.hp = 1
        super().__init__(speed, image, x, y, target, hp=1, scale=1)
