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
        self.invincible = False
        self.explosion = False
        self.score = 0
        self.missed = 0
        self.ult = 0
        self.maxUlt = 10
        
        self.enemies = enemies
        self.explosion_group = pygame.sprite.Group()

        self.explosion_sound = pygame.mixer.Sound('sound/explosion.mp3')
        self.explosion_sound.set_volume(0.1)
        
    def check_death(self):
        if self.hp <= 0 and self.alive:
            self.alive = False
        if not self.alive and not self.explosion:
            explosion = Explosion(self.explosion_group, self.rect.centerx, self.rect.centery)
            self.invincible = True
            self.kill()
            self.explosion = True
            self.explosion_sound.play()

        if self.explosion and len(self.explosion_group) == 0:
            return True

    def update(self):
        self.check_death()