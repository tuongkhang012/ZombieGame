import pygame
import random
import AoE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, image, x, y, target, hp=1, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alive = True
        self.bonked = False
        self.hp = hp
        self.counter = random.randint(15, 30)
        self.target = target
        # self.bonked_group = pygame.sprite.Group()     # to spawn bonked animation

    def check_bonk(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and not self.bonked:
            self.target.score += 1
            self.hp -= 50
            self.bonked = True

        if not self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.target.missed += 1

    def check_AoE(self, aoe_collision_rect):
            if self.rect.colliderect(aoe_collision_rect) and not self.bonked:
                # AoE effect on the enemy
                self.target.score += 1
                self.hp -= 50
                self.bonked = True

    def catch_sensei(self):
        if self.rect.colliderect(self.target.rect):
            self.hp -= 50
            if not self.target.invincible:
                self.target.hp -= 1

        if self.hp <= 0:
            self.alive = False

    def check_death(self):
        if not self.alive and not self.bonked:
            self.speed = 0
            # add animation bonked
            self.bonked = True

        if self.bonked: #and len(self.bonked_group) == 0:
            self.kill()

    def update(self, screenheight, screenwidth, aoe_group):
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

        self.check_bonk()
        self.catch_sensei()
        self.check_death()
        for aoe in aoe_group:
            aoe_collision_rect = aoe.get_collision_rect()
            self.check_AoE(aoe_collision_rect)