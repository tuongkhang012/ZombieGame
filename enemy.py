import pygame

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y, player_group):

        self.screen = pygame.display.get_surface()

        # groups
        self.player_group = player_group     # to check collision with player
        #self.bonked_group = pygame.sprite.Group()     # to spawn bonked animation

        # img
        self.image = pygame.image.load('artwork/nihaha.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = (x+25,y+25))

        # movement
        self.direction = (-1, 0)    # choose direction
        self.speed = 2
        self.timer = 0

        # enemy stats
        self.health = 2
        self.alive = True

        self.bonked = False

    def movement(self):
        pass

    def catch_sensei(self):
        for player in self.player_group:
            if self.rect.colliderect(player.rect):
                self.health -= 50
                if not player.invincible:
                    player.health -= 1

        if self.health <= 0:
            self.alive = False

    def check_death(self):
        if not self.alive and not self.bonked:
            self.speed = 0
            # add animation bonked
            self.bonked = True

        if self.bonked and len(self.explosion_group) == 0:
            self.kill()


    def update(self):
        self.movement()


