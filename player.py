import pygame
import random
from effect import Explosion
sensei = pygame.image.load("artwork/sensei.png")


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, enemies, hp=3, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(sensei,
                                            (int(sensei.get_width() * scale), int(sensei.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hp = hp
        self.alive = True
        self.explosion = False
        
        self.enemies = enemies
        self.explosion_group = pygame.sprite.Group()
        
    def check_death(self):
        if not self.alive and not self.explosion:
            explosion = Explosion(self.explosion_group, self.rect.centerx, self.rect.centery)
            self.explosion = True
            self.explosion_sound.play()

        if self.explosion and len(self.explosion_group) == 0:
            self.kill()

    def update(self):
        self.check_death()
