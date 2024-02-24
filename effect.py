import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)

        # explosion img
        self.group = group
        self.image_list = []
        for i in range(5):
            image = pygame.image.load(f"artwork/explosion/{i}.png")
            self.image_list.append(image)

        self.index = 0
        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(self.pre_image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))

    def animation(self):
        self.index += 0.2

        if self.index < len(self.image_list):
            self.pre_image = self.image_list[int(self.index)]
            self.image = pygame.transform.scale(self.pre_image, (100, 100))
        else:
            self.kill()

    def update(self):
        self.animation()

class Ex(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.group = group

        # ex img
        self.image_list = []
        for i in range(4):
            image = pygame.image.load(f"artwork/ult/{i}.png")
            self.image_list.append(image)

        self.index = 0
        self.image = self.image_list[self.index]

        # sound
        self.sound =  pygame.mixer.Sound("sound/ex_sound.mp3")
        self.sound.set_volume(0.3)
        self.sound.play()

    def animation(self):
        self.index += 0.2

        if self.index < len(self.image_list):
            self.image = self.image_list[int(self.index)]
        else:
            self.kill()

    def update(self):
        self.animation()