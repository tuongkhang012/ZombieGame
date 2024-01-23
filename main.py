import pygame
import buttonRect
import sys
import json
import random
from enemies import koyuki as koyukiType
from enemies import mutsuki as mutsukiType
from enemies import yuuka as yuukaType
import player
import AoE

# variable
pygame.font.init()
SCREENWIDTH, SCREENHEIGHT = 640, 640
FPS = 30
CAPTION = "Hello World!"
PIXEL_FONT_BIG = pygame.font.Font("font/PixelGameFont.ttf", 80)
PIXEL_FONT = pygame.font.Font("font/PixelGameFont.ttf", 40)
PIXEL_FONT_SMALL = pygame.font.Font("font/PixelGameFont.ttf", 15)
speedupRate = 0.05
koyukiBaseSpeed = 3
mutsukiBaseSpeed = 3
yuukaBaseSpeed = 1
previous_score = 0
missed_score = 0

# save game
try:
    with open('save/data.json') as score_file:
        data = json.load(score_file)
    print('save file found!')
except FileNotFoundError:
    print('no save file found! Creating a new save file')
    data = {
        "hiscore": 0,
    }


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
        self.end = GameOver(self.screen, self.gameStateManager)
        self.pause = Pause(self.screen, self.gameStateManager)

        self.states = {"main_menu": self.menu, "main_level": self.level, "game_over": self.end, "pause": self.pause}

    def run(self):
        while 1:
            self.states[self.gameStateManager.getState()].run()

            pygame.display.update()
            self.clock.tick(FPS)


class MainMenu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill('grey')
        startButton = buttonRect.Button("START", SCREENWIDTH / 2 - 77, 180, 154, 40, 5, 5,
                                        [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        resetButton = buttonRect.Button("RESET", SCREENWIDTH / 2 - 70, 300, 140, 40, 5, 5,
                                        [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        quitButton = buttonRect.Button("QUIT", SCREENWIDTH / 2 - 50, 420, 100, 40, 5, 5,
                                       [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        startPressed = startButton.draw(self.display)
        resetPressed = resetButton.draw(self.display)
        quitPressed = quitButton.draw(self.display)

        if startPressed:
            self.gameStateManager.setState("main_level", "sound/th06_05.wav")

        if resetPressed:
            data["hiscore"] = 0
            with open('save/data.json', 'w') as score_file:
                json.dump(data, score_file)

        if quitPressed:
            with open('save/data.json', 'w') as score_file:
                json.dump(data, score_file)

            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        self.aoe_group = pygame.sprite.Group()
        self.koyukiSpeed = koyukiBaseSpeed
        self.mutsukiSpeed = mutsukiBaseSpeed
        self.yuukaSpeed = yuukaBaseSpeed

    def run(self):
        global previous_score
        global missed_score
        keys = pygame.key.get_pressed()
        mutsuki = pygame.image.load('artwork/kufufu.png')
        koyuki = pygame.image.load('artwork/nihaha.png')
        self.counter -= 1
        self.display.fill('grey')

        self.enemies.update(SCREENHEIGHT, SCREENWIDTH,self.aoe_group)
        self.players.update()

        self.enemies.draw(self.display)
        self.players.draw(self.display)
        drawText(self.display, str(self.sensei.score), PIXEL_FONT, 'black', 5, 5)
        drawText(self.display, "HI: " + str(data["hiscore"]), PIXEL_FONT_SMALL, 'black', 5, 40)
        drawText(self.display, str(self.sensei.hp), PIXEL_FONT, 'black', 5, SCREENHEIGHT-35)

        self.koyukiSpeed += speedupRate/FPS
        self.mutsukiSpeed += speedupRate / FPS
        self.yuukaSpeed += speedupRate / FPS

        if self.sensei.hp <= 0:
            previous_score = self.sensei.score
            missed_score = self.sensei.missed
            self.reset()
            self.gameStateManager.setState("game_over", "sound/fadeout.mp3", 0.04)

        #Check for button
        backButton = buttonRect.Button("BACK", SCREENWIDTH-132, 10, 122, 40, 5, 5,
                                        [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        backPressed = backButton.draw(self.display)
        if backPressed:
            self.gameStateManager.setState("main_menu", "sound/endlessCarnival.mp3")
            self.reset()

        #Spawning mechanics
        if self.counter == 0:
            spawnpoint = random.choice([0, 1, 2, 3])
            spawntype = random.choice([0, 1, 2])

            if spawnpoint == 0:
                pos = (random.randint(0, SCREENWIDTH),SCREENHEIGHT)
            elif spawnpoint == 1:
                pos = (random.randint(0, SCREENWIDTH), 0)
                e = koyukiType.Koyuki(self.koyukiSpeed, random.randint(0, SCREENWIDTH),
                                0, self.sensei)
            elif spawnpoint == 2:
                pos = (0, random.randint(0, SCREENHEIGHT))
                e = koyukiType.Koyuki(self.koyukiSpeed, 0,
                                random.randint(0, SCREENHEIGHT), self.sensei)
            else:
                pos = (SCREENWIDTH, random.randint(0, SCREENHEIGHT))
                e = koyukiType.Koyuki(self.koyukiSpeed, SCREENWIDTH,
                                random.randint(0, SCREENHEIGHT), self.sensei)
            if spawntype == 0:
                e = koyukiType.Koyuki(self.koyukiSpeed, pos[0], pos[1], self.sensei)
            elif spawntype == 1:
                e = mutsukiType.Mutsuki(self.mutsukiSpeed, pos[0], pos[1], self.sensei)
            elif spawntype == 2:
                e = yuukaType.Yuuka(self.yuukaSpeed, pos[0], pos[1], self.sensei)

            self.enemies.add(e)
            self.counter = random.randint(15, 30)

        if keys[pygame.K_SPACE]:
            self.gameStateManager.setState("pause", "sound/th06_05.wav", 0.02, c=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('save/data.json', 'w') as score_file:
                    json.dump(data, score_file)

                pygame.quit()
                sys.exit()
            # make AoE
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                aoe = AoE.AoE(x, y)
                self.aoe_group.add(aoe)
                self.sensei.missed += 1

        # Update and draw AoEs
        self.aoe_group.update()

    def reset(self):
        if self.sensei.score > data["hiscore"]:
            data["hiscore"] = self.sensei.score
        self.enemies.empty()
        self.sensei.hp = 3
        self.sensei.score = 0
        self.sensei.missed = 0
        self.koyukiSpeed = koyukiBaseSpeed
        self.mutsukiSpeed = mutsukiBaseSpeed
        self.yuukaSpeed = yuukaBaseSpeed


class GameOver:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill([74, 74, 74])
        drawText(self.display, "GAME OVER", PIXEL_FONT_BIG, [255, 55, 55], SCREENWIDTH/2 - 230, 100)
        drawText(self.display, "SCORE: " + str(previous_score),
                 PIXEL_FONT_SMALL, [255, 55, 55], SCREENWIDTH / 2 - 30, 200)
        drawText(self.display, "MISSED: " + str(missed_score),
                 PIXEL_FONT_SMALL, [255, 55, 55], SCREENWIDTH / 2 - 34, 220)
        if missed_score == 0:
            drawText(self.display, "ACCURACY: 100%", PIXEL_FONT_SMALL, [255, 55, 55], SCREENWIDTH / 2 - 64, 240)
        else:
            drawText(self.display, "ACCURACY: {:.2f}%".format(previous_score/(previous_score+missed_score) * 100),
                     PIXEL_FONT_SMALL, [255, 55, 55], SCREENWIDTH / 2 - 64, 240)
        restartButton = buttonRect.Button("RESTART", SCREENWIDTH / 2 - 104, 350, 208, 40, 5, 5,
                                        [255, 255, 255], [0, 0, 0], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        titleButton = buttonRect.Button("TITLE", SCREENWIDTH / 2 - 64, 470, 128, 40, 5, 5,
                                       [255, 255, 255], [0, 0, 0], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        restartPressed = restartButton.draw(self.display)
        titlePressed = titleButton.draw(self.display)

        if restartPressed:
            self.gameStateManager.setState("main_level", "sound/th06_05.wav")

        if titlePressed:
            self.gameStateManager.setState("main_menu", "sound/endlessCarnival.mp3")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('save/data.json', 'w') as score_file:
                    json.dump(data, score_file)

                pygame.quit()
                sys.exit()


class Pause:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill([74, 74, 74])
        drawText(self.display, "PAUSED", PIXEL_FONT_BIG, [255, 255, 255], SCREENWIDTH/2 - 160, 100)
        continueButton = buttonRect.Button("CONTINUE", SCREENWIDTH / 2 - 102, 350, 204, 40, 5, 5,
                                           [255, 255, 255], [0, 0, 0], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        continuePressed = continueButton.draw(self.display)

        if continuePressed:
            self.gameStateManager.setState("main_level", "sound/th06_05.wav", 0.05, c=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('save/data.json', 'w') as score_file:
                    json.dump(data, score_file)

                pygame.quit()
                sys.exit()


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

    def setState(self, state, bgm, volume=0.05, c=False):
        self.currentState = state
        self.bgm = bgm
        if not c:
            pygame.mixer.music.load(self.bgm)
            pygame.mixer.music.play(-1)  # -1 = unlimited loop
            pygame.mixer.music.set_volume(volume)
        else:
            pygame.mixer.music.set_volume(volume)



if __name__ == '__main__':
    game = Game()
    game.run()
