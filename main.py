import pygame
import buttonRect
import sys
import json
import random
from enemies import koyuki as koyukiType
from enemies import mutsuki as mutsukiType
from enemies import yuuka as yuukaType
import heart
import player
import AoE

# variable
pygame.font.init()
SCREENWIDTH, SCREENHEIGHT = 640, 640
FPS = 30
CAPTION = "Leave Sensei alone!"
icon = pygame.image.load("artwork/sob.png")
pygame.display.set_icon(icon)
PIXEL_FONT_BIG = pygame.font.Font("font/PixelGameFont.ttf", 80)
PIXEL_FONT = pygame.font.Font("font/PixelGameFont.ttf", 40)
PIXEL_FONT_SMALL = pygame.font.Font("font/PixelGameFont.ttf", 15)
speedupRate = 0.05
koyukiBaseSpeed = 3
mutsukiBaseSpeed = 3
yuukaBaseSpeed = 2
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
        self.help = Help(self.screen, self.gameStateManager)

        self.states = {"main_menu": self.menu, "main_level": self.level, "game_over": self.end, "pause": self.pause,
                       "help": self.help}

    def run(self):
        while 1:
            self.states[self.gameStateManager.getState()].run()

            pygame.display.flip()
            self.clock.tick(FPS)


class MainMenu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.title_scrn = pygame.image.load('artwork/titlescreen.png').convert_alpha()
        self.display.blit(self.title_scrn, (0, 0))

        #drawText(self.display, "LEAVE SENSEI ALONE", PIXEL_FONT, 'white', SCREENWIDTH / 2 - 220, 100)

        startButton = buttonRect.Button("START", SCREENWIDTH / 2 - 77, 260, 154, 40, 5, 5,
                                        [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        resetButton = buttonRect.Button("RESET", SCREENWIDTH / 2 - 70, 340, 140, 40, 5, 5,
                                        [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        helpButton = buttonRect.Button("HELP", SCREENWIDTH / 2 - 57, 420, 114, 40, 5, 5,
                                       [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        quitButton = buttonRect.Button("QUIT", SCREENWIDTH / 2 - 50, 500, 100, 40, 5, 5,
                                       [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        startPressed = startButton.draw(self.display)
        resetPressed = resetButton.draw(self.display)
        quitPressed = quitButton.draw(self.display)
        helpPressed = helpButton.draw(self.display)

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

        if helpPressed:
            self.gameStateManager.setState("help", "sound/th06_05.wav", c=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('save/data.json', 'w') as score_file:
                    json.dump(data, score_file)

                pygame.quit()
                sys.exit()


class Help:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill('grey')
        drawText(self.display, "YOU'RE THE SENSEI, TRYING TO FOCUS ON YOUR DEADLINES."
                 , PIXEL_FONT_SMALL, 'black', 10, 100)
        drawText(self.display, "BUT THE STUDENTS KEEP ANNOYING YOU, SO YOU HAVE TO TAKE MEASURES."
                 , PIXEL_FONT_SMALL, 'black', 10, 120)

        drawText(self.display, "LEFT CLICK - BONK"
                 , PIXEL_FONT_SMALL, 'black', SCREENWIDTH / 2 - 80, 300)
        drawText(self.display, "RIGHT CLICK - EX"
                 , PIXEL_FONT_SMALL, 'black', SCREENWIDTH / 2 - 80, 320)
        drawText(self.display, "SPACE - PAUSE"
                 , PIXEL_FONT_SMALL, 'black', SCREENWIDTH / 2 - 80, 340)

        backButton = buttonRect.Button("BACK", SCREENWIDTH / 2 - 61, 550, 122, 40, 5, 5,
                                       [0, 0, 0], [255, 255, 255], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        backPressed = backButton.draw(self.display)

        if backPressed:
            self.gameStateManager.setState("main_menu", "sound/th06_05.wav", c=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('save/data.json', 'w') as score_file:
                    json.dump(data, score_file)

                pygame.quit()
                sys.exit()


class MainLevel:
    def __init__(self, display, gameStateManager):
        self.display = display

        self.bat0 = pygame.image.load("artwork/bat/0.png").convert_alpha()
        self.bat0 = pygame.transform.scale(self.bat0, (int(self.bat0.get_width() * 2), int(self.bat0.get_height() * 2)))
        self.bat1 = pygame.image.load("artwork/bat/1.png").convert_alpha()
        self.bat1 = pygame.transform.scale(self.bat1, (int(self.bat1.get_width() * 2), int(self.bat1.get_height() * 2)))

        self.gameStateManager = gameStateManager
        self.enemies = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.players = pygame.sprite.GroupSingle()
        self.aoe_group = pygame.sprite.Group()

        self.sensei = player.Player(SCREENWIDTH / 2, SCREENHEIGHT / 2, self.enemies)
        self.players.add(self.sensei)
        self.counter = random.randint(10, 15)

        self.explosions = pygame.sprite.Group()
        self.koyukiSpeed = koyukiBaseSpeed
        self.mutsukiSpeed = mutsukiBaseSpeed
        self.yuukaSpeed = yuukaBaseSpeed
        self.spawnRate = 15

    def run(self):
        global previous_score
        global missed_score
        keys = pygame.key.get_pressed()
        self.counter -= 1
        self.display.fill('grey')
        pygame.mouse.set_visible(False)
        mouse_pos = pygame.mouse.get_pos()

        if self.sensei.hp == 3:
            heart1 = heart.Heart(1, 20, SCREENHEIGHT - 20)
            heart2 = heart.Heart(1, 55, SCREENHEIGHT - 20)
            heart3 = heart.Heart(1, 90, SCREENHEIGHT - 20)
        elif self.sensei.hp == 2:
            heart1 = heart.Heart(1, 20, SCREENHEIGHT - 20)
            heart2 = heart.Heart(1, 55, SCREENHEIGHT - 20)
            heart3 = heart.Heart(0, 90, SCREENHEIGHT - 20)
        elif self.sensei.hp == 1:
            heart1 = heart.Heart(1, 20, SCREENHEIGHT - 20)
            heart2 = heart.Heart(0, 55, SCREENHEIGHT - 20)
            heart3 = heart.Heart(0, 90, SCREENHEIGHT - 20)
        else:
            heart1 = heart.Heart(0, 20, SCREENHEIGHT - 20)
            heart2 = heart.Heart(0, 55, SCREENHEIGHT - 20)
            heart3 = heart.Heart(0, 90, SCREENHEIGHT - 20)

        self.hearts.add(heart1, heart2, heart3)

        self.koyukiSpeed += speedupRate / FPS
        self.mutsukiSpeed += speedupRate / FPS
        self.yuukaSpeed += speedupRate / FPS
        if self.spawnRate != speedupRate / FPS:
            self.spawnRate -= speedupRate / FPS

        self.sensei.explosion_group.update()
        self.players.update()
        self.hearts.update()

        self.sensei.explosion_group.draw(self.display)
        self.enemies.draw(self.display)
        self.players.draw(self.display)
        self.hearts.draw(self.display)
        self.enemies.update(SCREENHEIGHT, SCREENWIDTH, self.aoe_group, self.display)
        self.ult_bar(self.display)

        drawText(self.display, str(self.sensei.score), PIXEL_FONT, 'black', 5, 5)
        drawText(self.display, "HI: " + str(data["hiscore"]), PIXEL_FONT_SMALL, 'black', 5, 40)
        if self.sensei.ult != self.sensei.maxUlt:
            drawText(self.display, "EX: {:.2f}%".format(self.sensei.ult / self.sensei.maxUlt * 100),
                     PIXEL_FONT_SMALL, 'black', SCREENWIDTH - 90, SCREENHEIGHT - 50)
        else:
            drawText(self.display, "EX READY, RIGHT CLICK",
                     PIXEL_FONT_SMALL, 'black', SCREENWIDTH - 190, SCREENHEIGHT - 50)

        if self.sensei.check_death():
            previous_score = self.sensei.score
            missed_score = self.sensei.missed
            self.gameStateManager.setState("game_over", "sound/fadeout.mp3", 0.04)
            self.reset()

        # Spawning mechanics
        if self.counter == 0:
            spawnpoint = random.choice([0, 1, 2, 3])
            spawntype = random.choice([0, 1, 2])

            if spawnpoint == 0:
                pos = (random.randint(0, SCREENWIDTH), SCREENHEIGHT)
            elif spawnpoint == 1:
                pos = (random.randint(0, SCREENWIDTH), 0)
            elif spawnpoint == 2:
                pos = (0, random.randint(0, SCREENHEIGHT))
            else:
                pos = (SCREENWIDTH, random.randint(0, SCREENHEIGHT))

            if spawntype == 0:
                e = koyukiType.Koyuki(self.koyukiSpeed, pos[0], pos[1], self.sensei)
            elif spawntype == 1:
                e = mutsukiType.Mutsuki(self.mutsukiSpeed, pos[0], pos[1], self.sensei)
            elif spawntype == 2:
                e = yuukaType.Yuuka(self.yuukaSpeed, pos[0], pos[1], self.sensei)

            self.enemies.add(e)
            self.counter = random.randint(int(self.spawnRate), int(self.spawnRate) + 5)

        if keys[pygame.K_SPACE]:
            self.gameStateManager.setState("pause", "sound/th06_05.wav", 0.02, c=True)

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('save/data.json', 'w') as score_file:
                    json.dump(data, score_file)

                pygame.quit()
                sys.exit()
            # make AoE
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.sensei.invincible:
                x, y = event.pos
                aoe = AoE.AoE(x, y)
                self.aoe_group.add(aoe)
                self.sensei.missed += 1
                self.display.blit(self.bat1, mouse_pos)
                clicked = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.sensei.ult == self.sensei.maxUlt \
                    and not self.sensei.invincible:
                for enemy in self.enemies:
                    enemy.kill()
                    self.sensei.score += 1
                self.sensei.ult = 0
                self.sensei.maxUlt += 5
                self.display.blit(self.bat1, mouse_pos)

        # Update and draw AoEs
        self.aoe_group.update()

        if not clicked:
            self.display.blit(self.bat0, mouse_pos)

    def reset(self):
        if self.sensei.score > data["hiscore"]:
            data["hiscore"] = self.sensei.score
        self.enemies.empty()
        self.hearts.empty()
        pygame.mouse.set_visible(True)
        self.sensei = player.Player(SCREENWIDTH / 2, SCREENHEIGHT / 2, self.enemies)
        self.players.add(self.sensei)
        self.sensei.hp = 3
        self.sensei.score = 0
        self.sensei.missed = 0
        self.sensei.ult = 0
        self.sensei.maxUlt = 10
        self.koyukiSpeed = koyukiBaseSpeed
        self.mutsukiSpeed = mutsukiBaseSpeed
        self.yuukaSpeed = yuukaBaseSpeed

    def ult_bar(self, screen):
        ratio = self.sensei.ult / self.sensei.maxUlt

        pygame.draw.rect(screen, "black", (SCREENWIDTH - 212, SCREENHEIGHT - 32, 204, 24))
        pygame.draw.rect(screen, "blue", (SCREENWIDTH - 210, SCREENHEIGHT - 30, 200, 20))
        pygame.draw.rect(screen, "lightblue", (SCREENWIDTH - 210, SCREENHEIGHT - 30, 200 * ratio, 20))


class GameOver:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill([74, 74, 74])
        drawText(self.display, "GAME OVER", PIXEL_FONT_BIG, [255, 55, 55], SCREENWIDTH / 2 - 230, 100)
        drawText(self.display, "SCORE: " + str(previous_score),
                 PIXEL_FONT_SMALL, [255, 55, 55], SCREENWIDTH / 2 - 30, 200)
        drawText(self.display, "MISSED: " + str(missed_score),
                 PIXEL_FONT_SMALL, [255, 55, 55], SCREENWIDTH / 2 - 34, 220)
        if missed_score == 0:
            drawText(self.display, "ACCURACY: 100%", PIXEL_FONT_SMALL, [255, 55, 55], SCREENWIDTH / 2 - 64, 240)
        else:
            drawText(self.display, "ACCURACY: {:.2f}%".format(previous_score / (previous_score + missed_score) * 100),
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
        pygame.mouse.set_visible(True)
        self.display.fill([74, 74, 74])
        drawText(self.display, "PAUSED", PIXEL_FONT_BIG, [255, 255, 255], SCREENWIDTH / 2 - 160, 100)
        continueButton = buttonRect.Button("CONTINUE", SCREENWIDTH / 2 - 102, 350, 204, 40, 5, 5,
                                           [255, 255, 255], [0, 0, 0], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        backButton = buttonRect.Button("BACK", SCREENWIDTH / 2 - 61, 450, 122, 40, 5, 5,
                                       [255, 255, 255], [0, 0, 0], PIXEL_FONT, [0, 236, 252], [0, 126, 252])
        backPressed = backButton.draw(self.display)
        continuePressed = continueButton.draw(self.display)

        if continuePressed:
            pygame.mouse.set_visible(False)
            self.gameStateManager.setState("main_level", "sound/th06_05.wav", 0.05, c=True)
        if backPressed:
            self.gameStateManager.setState("main_menu", "sound/endlessCarnival.mp3")

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
