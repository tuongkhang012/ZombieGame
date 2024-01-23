import pygame
import random


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
        self.counter = random.randint(3, 9)
        self.target = target
        #self.bonked_group = pygame.sprite.Group()     # to spawn bonked animation

    def catch_sensei(self):
        for player in self.target:
            if self.rect.colliderect(player.rect):
                self.hp -= 50
                player.hp -= 1

        if self.hp <= 0:
            self.alive = False

    def check_death(self):
        if not self.alive and not self.bonked:
            self.speed = 0
            # add animation bonked
            #self.bonked = True

        if self.bonked and len(self.bonked_group) == 0:
            self.kill()
        
    def update(self, screenheight, screenwidth):
        self.counter -= 1

        if self.counter == 0:
            choice = random.randint(1, 3)

            if choice == 1:
                self.rect.x += random.choice([1, -1]) * 15
            elif choice == 2:
                self.rect.y += random.choice([1, -1]) * 15
            else:
                self.rect.x += random.choice([1, -1]) * 15
                self.rect.y += random.choice([1, -1]) * 15

            self.counter = random.randint(3, 9)
        else:
            distance_x = self.target.rect.x - self.rect.x
            distance_y = self.target.rect.y - self.rect.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            if distance != 0:
                self.rect.x += self.speed * distance_x / distance
                self.rect.y += self.speed * distance_y / distance

        #check if out-of-bound
        if self.rect.top > screenheight or self.rect.bottom < 0:
            self.kill()

        if self.rect.left > screenwidth or self.rect.right < 0:
            self.kill()
