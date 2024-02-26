import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, image, death_img, death_sound, x, y, target, channel, hp=1, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.channel = channel
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.death_img = pygame.transform.scale(death_img, (int(width * scale), int(height * scale)))
        self.death_sound = death_sound
        self.death_sound.set_volume(0.05)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alive = True
        self.bonked = False
        self.max_hp = hp
        self.hp = hp
        self.counter = random.randint(15, 30)
        self.is_dying = False
        self.death_cntr = 15

        self.target = target
        # self.bonked_group = pygame.sprite.Group()     # to spawn bonked animation
    def movement(self):
        distance_x = self.target.rect.x - self.rect.x
        distance_y = self.target.rect.y - self.rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        if distance != 0:
            self.rect.x += self.speed * distance_x / distance
            self.rect.y += self.speed * distance_y / distance

    def health_bar(self, screen):
        pass

    def check_AoE(self, aoe_collision_rect):
        if self.rect.colliderect(aoe_collision_rect) and not self.bonked:
            # AoE effect on the enemy
            self.hp -= 1
            self.target.missed -= 1

    def catch_sensei(self):
        if self.rect.colliderect(self.target.rect):
            self.kill()
            if not self.target.invincible:
                self.target.hp -= 1

        if self.hp <= 0 and not self.is_dying:
            #self.bonked = True
            self.target.score += 1
            if self.target.ult != self.target.maxUlt:
                self.target.ult += 1
            self.alive = False

    def check_death(self):
        if not self.alive and not self.is_dying:
            self.speed = 0
            self.is_dying = True
            if not self.channel.get_busy():
                self.channel.play(self.death_sound)
        if self.is_dying:
            self.image = self.death_img
            self.death_cntr -= 1
            if self.death_cntr <= 0:
                self.bonked = True
                self.kill()

    def update(self, screenheight, screenwidth, aoe_group, display):
        self.health_bar(display)
        self.movement()
        self.catch_sensei()
        self.check_death()
        for aoe in aoe_group:
            aoe_collision_rect = aoe.get_collision_rect()
            self.check_AoE(aoe_collision_rect)
