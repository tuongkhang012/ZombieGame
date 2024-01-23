import pygame
import enemy
import random


class Koyuki(enemy.Enemy):
    def __init__(self, speed, x, y, target):
        image = pygame.image.load('artwork/nihaha.png').convert_alpha()
        self.hp = 1
        super().__init__(speed, image, x, y, target, hp=1, scale=1)

    def movement(self):
        self.counter -= 1

        if self.counter == 0:
            self.rect.x += random.choice([1, 0, -1]) * 25
            self.rect.y += random.choice([1, 0, -1]) * 25

            self.counter = random.randint(15, 30)
        else:
            distance_x = self.target.rect.x - self.rect.x
            distance_y = self.target.rect.y - self.rect.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            if distance != 0:
                self.rect.x += self.speed * distance_x / distance
                self.rect.y += self.speed * distance_y / distance
