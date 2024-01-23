import pygame
import buttonRect
import sys
import json
import random
import enemy
import player

# variable
pygame.font.init()
SCREENWIDTH, SCREENHEIGHT = 640, 640
FPS = 30
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
mutsuki = pygame.image.load('artwork/kufufu.png')
koyuki = pygame.image.load('artwork/nihaha.png')


def drawText(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(CAPTION)
        self.gameStateManager = GameStateManager("main_menu", "sound/endlessCarnival.mp3")
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

        # # bgm
        # pygame.mixer.music.load('sound/th06_05.wav')
        # pygame.mixer.music.play(-1)  # -1 = unlimited loop
        # pygame.mixer.music.set_volume(0.05)

    def run(self, event):
        self.display.fill('grey')
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
            self.gameStateManager.setState("main_level", "sound/th06_05.wav")

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
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.GroupSingle()
        self.sensei = player.Player(SCREENWIDTH/2, SCREENHEIGHT/2, self.enemies)
        self.players.add(self.sensei)
        self.counter = random.randint(10,15)

    def run(self, event):
        self.counter -= 1
        self.display.fill('grey')
        drawText(self.display, str(self.sensei.score), PIXEL_FONT, 'black', 5, 5)

        self.enemies.update(SCREENHEIGHT, SCREENWIDTH)
        self.players.update()

        self.enemies.draw(self.display)
        self.players.draw(self.display)

        if self.sensei.hp == 0:
            print("game_over")
            self.reset()
            self.gameStateManager.setState("main_menu", "sound/endlessCarnival.mp3")

        #Check for button
        backButton = buttonRect.Button("BACK", SCREENWIDTH-132, 10, 122, 40, 5, 5,
                                        [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        backPressed = backButton.draw(self.display)
        if backPressed:
            self.gameStateManager.setState("main_menu", "sound/endlessCarnival.mp3")
            self.reset()

        #Check for mouse buttons
        if self.counter == 0:
            spawnpoint = random.choice([0, 1, 2, 3])

            if spawnpoint == 0:
                e = enemy.Enemy(5, koyuki, random.randint(0, SCREENWIDTH),
                                SCREENHEIGHT, self.sensei)
            elif spawnpoint == 1:
                e = enemy.Enemy(5, koyuki, random.randint(0, SCREENWIDTH),
                                0, self.sensei)
            elif spawnpoint == 2:
                e = enemy.Enemy(5, koyuki, 0,
                                random.randint(0, SCREENHEIGHT), self.sensei)
            else:
                e = enemy.Enemy(5, koyuki, SCREENWIDTH,
                                random.randint(0, SCREENHEIGHT), self.sensei)

            self.enemies.add(e)
            self.counter = random.randint(15, 30)

    def reset(self):
        data["score"] = self.sensei.score
        if self.sensei.score > data["hiscore"]:
            data["hiscore"] = self.sensei.score
        self.enemies.empty()
        self.sensei.hp = 3
        self.sensei.score = 0
        self.sensei.missed = 0

class GameStateManager:
    def __init__(self, currentState, bgm):
        self.currentState = currentState
        # bgm
        self.bgm = bgm
        pygame.mixer.music.load(self.bgm)
        pygame.mixer.music.play(-1)  # -1 = unlimited loop
        pygame.mixer.music.set_volume(0.05)

    def getState(self):
        return self.currentState

    def setState(self, state, bgm):
        self.currentState = state
        self.bgm = bgm
        pygame.mixer.music.load(self.bgm)
        pygame.mixer.music.play(-1)  # -1 = unlimited loop
        pygame.mixer.music.set_volume(0.05)


if __name__ == '__main__':
    game = Game()
    game.run()
