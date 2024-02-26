import pygame
from enemies import enemy


class Mutsuki(enemy.Enemy):
    def __init__(self, speed, x, y, target, channel):
        image = pygame.image.load('artwork/kufufu0.png').convert_alpha()
        death_img = pygame.image.load('artwork/kufufu1.png').convert_alpha()
        death_sound = pygame.mixer.Sound("sound/kufufuded.mp3")
        self.hp = 1
        super().__init__(speed, image, death_img, death_sound, x, y, target, channel, hp=2, scale=1)

    def health_bar(self, screen):
        ratio = self.hp / self.max_hp

        pygame.draw.rect(screen, "black", (self.rect.x - 1, self.rect.y - 13, 32, 6))
        pygame.draw.rect(screen, "red", (self.rect.x, self.rect.y - 12, 30, 4))
        pygame.draw.rect(screen, "green", (self.rect.x, self.rect.y - 12, 30 * ratio, 4))