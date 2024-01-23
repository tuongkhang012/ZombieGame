import pygame
import buttonRect
import sys
import json

# variable
pygame.font.init()
SCREENWIDTH, SCREENHEIGHT = 640, 640
FPS = 60
CAPTION = "Hello World!"
PIXEL_FONT = pygame.font.Font("font/PixelGameFont.ttf", 40)

# save game
try:
    with open('save/data.json') as score_file:
        data = json.load(score_file)
    print('save file found!')
except FileNotFoundError:
    print('no save file found! Creating a new save file')
    data = {
        "score": 0,
        "missed": 0,
        "hiscore": 0,
    }
mutsuki = pygame.transform.scale(pygame.image.load('artwork/mutsuki.png'), (SCREENWIDTH, SCREENHEIGHT))
koyuki = pygame.transform.scale(pygame.image.load('artwork/koyuki.jpg'), (SCREENWIDTH, SCREENHEIGHT))


def drawText(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))


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
                    with open('save/data.json', 'w') as score_file:
                        json.dump(data, score_file)

                    pygame.quit()
                    sys.exit()
                self.states[self.gameStateManager.getState()].run(event)

            pygame.display.update()
            self.clock.tick(FPS)


class MainMenu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        # bgm
        pygame.mixer.music.load('sound/th06_05.wav')
        pygame.mixer.music.play(-1)  # -1 = unlimited loop
        pygame.mixer.music.set_volume(0.3)

    def run(self, event):

        self.display.blit(koyuki, (0, 0))
        startButton = buttonRect.Button("START", SCREENWIDTH / 2 - 77, 180, 154, 40, 5, 5,
                                        [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        optionButton = buttonRect.Button("OPTION", SCREENWIDTH / 2 - 75, 300, 150, 40, 5, 5,
                                         [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        quitButton = buttonRect.Button("QUIT", SCREENWIDTH / 2 - 50, 420, 100, 40, 5, 5,
                                       [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        startPressed = startButton.draw(self.display)
        optionPressed = optionButton.draw(self.display)
        quitPressed = quitButton.draw(self.display)

        if startPressed:
            self.gameStateManager.setState("main_level")

        if optionPressed:
            print("Option")

        if quitPressed:
            with open('save/data.json', 'w') as score_file:
                json.dump(data, score_file)

            pygame.quit()
            sys.exit()


class MainLevel:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self, event):
        self.display.blit(mutsuki, (0, 0))
        backButton = buttonRect.Button("BACK", SCREENWIDTH-132, 10, 122, 40, 5, 5,
                                        [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        backPressed = backButton.draw(self.display)
        if backPressed:
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
