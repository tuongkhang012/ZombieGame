import pygame
from effect import Explosion

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_group):

        self.screen = pygame.display.get_surface()

        # groups
        self.enemy_group = enemy_group
        self.explosion_group = pygame.sprite.Group()

        # img
        self.image = pygame.image.load('artwork/sensei.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = (x+25,y+25))

        # player stat
        self.health = 1
        self.life = 3

        self.alive = True
        self.explosion = False

        self.invincible = False

        self.bonk = False

    def input(self):
        key = pygame.key.get_pressed()

        if pygame.mouse.get_pressed() == (1, 0, 0) and not self.bonk:
            self.bonk = True
        else:
            self.bonk = False
    def bonking(self):
        pass

    # def check_collision(self):            check collision from enemy.py

    def check_death(self):
        if not self.alive and not self.explosion:
            explosion = Explosion(self.explosion_group, self.rect.centerx, self.rect.centery)
            self.explosion = True
            self.explosion_sound.play()

        if self.explosion and len(self.explosion_group) == 0:
            self.kill()

    def update(self):
        self.input()
        self.bonking()

        self.check_death()