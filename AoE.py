import pygame

class AoE(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((22, 22))
        self.rect = self.image.get_rect(center=(x, y))
        self.duration = 1
        self.counter = 1

    def update(self):
        if self.counter <= 0:
            self.kill()  # Remove the AoE sprite from the group when the duration is reached
        else:
            self.counter -= self.duration
            # Update the rect based on the new position (center)
            self.rect.center = (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)

    def get_collision_rect(self):
        return self.rect