import pygame
import random

sensei = pygame.image.load("artwork/sensei.png")


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, hp=3, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(sensei,
                                            (int(sensei.get_width() * scale), int(sensei.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hp = hp

    def update(self):
        pass