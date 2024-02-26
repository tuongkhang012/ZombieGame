import pygame
import random


class Heart(pygame.sprite.Sprite):
    def __init__(self, Htype, x, y, scale=1):
        fullHeart = pygame.image.load("artwork/HeartFull.png").convert_alpha()
        emptyHeart = pygame.image.load("artwork/HeartEmpty.png").convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        if Htype == 1:
            self.image = fullHeart
        else:
            self.image = emptyHeart
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = random.randint(15, 30)