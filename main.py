import pygame
import sys
import json

SCREENWIDTH, SCREENHEIGHT = 1366, 768
FPS = 60
CAPTION = "Hello World!"

try:
    with open('data.json') as score_file:
        data = json.load(score_file)
    print('save file found!')
except:
    print('no save file found! Creating a new save file')
    data = {
        "score": 0,
        "missed": 0,
        "hiscore": 0,
    }


mutsuki = pygame.transform.scale(pygame.image.load('mutsuki.png'), (1366,768))
koyuki = pygame.transform.scale(pygame.image.load('koyuki.jpg'), (1366,768))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(CAPTION)
        self.gameStateManager = GameStateManager("main_menu")
        self.menu = MainMenu(self.screen, self.gameStateManager)
        self.level = MainLevel(self.screen, self.gameStateManager)

        self.states = {"main_menu": self.menu, "main_level": self.level}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open('data.json', 'w') as score_file:
                        json.dump(data, score_file)

                    pygame.quit()
                    sys.exit()

            self.states[self.gameStateManager.getState()].run()

            pygame.display.update()
            self.clock.tick(FPS)


class MainMenu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill('blue')
        self.display.blit(koyuki, (0,0))
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.gameStateManager.setState("main_level")


class MainLevel:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill('red')
        self.display.blit(mutsuki, (0,0))
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.gameStateManager.setState("main_menu")


class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def getState(self):
        return self.currentState

    def setState(self, state):
        self.currentState = state


if __name__ == '__main__':
    game = Game()
    game.run()
