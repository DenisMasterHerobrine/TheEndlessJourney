# TODO: Меню настроек
# TODO: Меню выбора уровней (доп. контент)
# TODO: Миссия 2 и 3 (доп. контент)
# TODO: Запаковать в bundled exe-файл для продакшена.

import random

import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from src.utils.configuration import Configuration
from src.utils.configuration.Configuration import *

global RESET

from pygame import DOUBLEBUF, HWSURFACE


# This is a main class of the game, it does all the processing that the game requires.

# Wraps a Main Menu button in the Settings menu.
def ButtonSettingsWrapper(isReset, isFirstLaunch, resetMusic, musicVolume, soundVolume, modifiers):
    Configuration.updateField("MUSIC_VOLUME", musicVolume)
    Configuration.updateField("SFX_VOLUME", soundVolume)
    Configuration.updateField("SPACESHIP_SPEED_MODIFIER", modifiers[0])
    Configuration.updateField("ENEMY_SPEED_MODIFIER", modifiers[1])
    Configuration.updateField("PARALLAX_SPEED_MODIFIER", modifiers[2])
    MainMenu(isReset, isFirstLaunch, False)


WIDTH = getField('WIDTH')
HEIGHT = getField('HEIGHT')
FPS = getField("FPS")
VERSION = "v0.14.3"

# Colors Constants
BLACK = (0, 0, 0)
# Light Shade of the Button
COLOR_LIGHT = (170, 170, 170)
# Dark Shade of the Button
COLOR_DARK = (100, 100, 100)
COLOR_DARKER = (50, 50, 50)

# Basic PyGame window implementation
# Launch the game initializer.
pygame.init()

# Start the sound mixer engine.
pygame.mixer.init()

# Create a display with custom WIDTH and HEIGHT.
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF)

# Set the game window title.
pygame.display.set_caption("The Endless Journey " + VERSION)

# Get base directory of the game.
GAME_DIR = os.path.dirname(__file__)
SPRITES_DIR = os.path.join(os.path.join(GAME_DIR, 'assets'), 'sprites')
BACKGROUNDS = os.path.join(os.path.join(GAME_DIR, 'assets'), 'bitmaps')
FONTS = os.path.join(os.path.join(GAME_DIR, 'assets'), 'fonts')
MUSIC = os.path.join(os.path.join(GAME_DIR, 'assets'), 'music')
SOUNDS = os.path.join(os.path.join(GAME_DIR, 'assets'), 'sfx')

BULLET_SPRITE = pygame.image.load(os.path.join(os.path.join(SPRITES_DIR, 'entities'), 'SHOTMEDIUM.PNG'))
MOB_ENEMY_SPRITE = pygame.image.load(os.path.join(os.path.join(SPRITES_DIR, 'entities'), 'ALIENSMALL.GIF'))
PLAYER_SPACESHIP_SPRITE = pygame.image.load(
    os.path.join(os.path.join(SPRITES_DIR, 'spaceship'), 'SMALL_BLUE_SPIKED_SHIP.PNG'))

BACKGROUND_MAINMENU = pygame.image.load(os.path.join(BACKGROUNDS, 'MAINMENU.PNG'))
BACKGROUND_MISSION_ONE = pygame.image.load(os.path.join(BACKGROUNDS, 'MISSION1.PNG'))

BACKGROUND_MAINMENU = pygame.transform.scale(BACKGROUND_MAINMENU, (WIDTH, WIDTH * 2.15))
BACKGROUND_MISSION_ONE = pygame.transform.scale(BACKGROUND_MISSION_ONE, (WIDTH, WIDTH * 2.5))

# Get sounds instances.
SHOOT_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS, 'SHOOT.WAV'))
HIT_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS, 'HIT.WAV'))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS, 'EXPLOSION.WAV'))

# Gane Variables Constants
SPRITES = pygame.sprite.Group()
MOBS = pygame.sprite.Group()
BULLETS = pygame.sprite.Group()
EXPLOSIONS = pygame.sprite.Group()

# Initialize clock.
CLOCK = pygame.time.Clock()
score = 0


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        ANIMATION_SPEED = 2
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.size = size
        for num in range(1, 6):
            img = pygame.image.load(
                os.path.join(os.path.join(SPRITES_DIR, 'animations'), f"EXPLOSION{num}-min.PNG"))
            img = pygame.transform.scale(img, (self.size, self.size))
            for _ in range(ANIMATION_SPEED):
                self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.counter = 0

    def update(self):
        explosion_speed = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = MOB_ENEMY_SPRITE.convert()
        self.image.set_colorkey((252, 225, 93))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange( WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 2)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(-2, 2)


# Main Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = PLAYER_SPACESHIP_SPRITE.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        # Arrow movement keys:
        if keystate[pygame.K_LEFT]:
            self.speedx = -4
        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
        if keystate[pygame.K_UP]:
            self.speedy = -4
        if keystate[pygame.K_DOWN]:
            self.speedy = 4

        # WASD movement keys:
        if keystate[pygame.K_a]:
            self.speedx = -4
        if keystate[pygame.K_d]:
            self.speedx = 4
        if keystate[pygame.K_w]:
            self.speedy = -4
        if keystate[pygame.K_s]:
            self.speedy = 4

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Borders of the Game:
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        SPRITES.add(bullet)
        BULLETS.add(bullet)
        SHOOT_SOUND.play()


# Класс пули.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = BULLET_SPRITE.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Remove if out of border
        if self.rect.bottom < 0:
            self.kill()


# Конструктор рендера текста.
def get_font(size):
    return pygame.font.Font(os.path.join(FONTS, "FONT.TTF"), size)

PLAYER = Player()
# Главное меню.
def MainMenu(isReset, isFirstLaunch, resetMusic):
    # Загружаем главную тему.
    if resetMusic:
        pygame.mixer.music.load(os.path.join(MUSIC, "MAINMENU.OGG"))
        pygame.mixer.music.set_volume(getField("MUSIC_VOLUME") / 100)
        pygame.mixer.music.play(loops=-1)
    RUNNING = True
    screen.blit(BACKGROUND_MAINMENU.convert(), (0, 0))

    MENU_TEXT = get_font(int(HEIGHT / 10)).render("The Endless Journey", True, (0, 0, 0))
    MENU_TEXT.set_alpha(125)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))
    screen.blit(MENU_TEXT, MENU_RECT)

    PLAY_TEXT = get_font(int(HEIGHT / 10)).render("Play", True, (0, 0, 0))
    PLAY_TEXT.set_alpha(125)
    PLAY_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2 + 425, HEIGHT / 2 - 17.5))
    screen.blit(PLAY_TEXT, PLAY_RECT)

    OPTIONS_TEXT = get_font(int(HEIGHT / 10)).render("Options", True, (0, 0, 0))
    OPTIONS_TEXT.set_alpha(125)
    OPTIONS_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2 + 337.5, HEIGHT / 2 + 132.5))
    screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

    QUIT_TEXT = get_font(int(HEIGHT / 10)).render("Quit", True, (0, 0, 0))
    QUIT_TEXT.set_alpha(125)
    QUIT_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2 + 425, HEIGHT / 2 + 282.5))
    screen.blit(QUIT_TEXT, QUIT_RECT)

    Utils.draw_rect_alpha(screen, (100, 100, 100, 100),
                          (WIDTH / 2 - 375, HEIGHT / 2 - 75, 750, 100))
    Utils.draw_rect_alpha(screen, (100, 100, 100, 100),
                          (WIDTH / 2 - 375, HEIGHT / 2 + 75, 750, 100))
    Utils.draw_rect_alpha(screen, (100, 100, 100, 100),
                          (WIDTH / 2 - 375, HEIGHT / 2 + 225, 750, 100))

    while RUNNING:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # We are closing our game using the button.
            if event.type == pygame.QUIT:
                RUNNING = False
                pygame.display.quit()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH / 2 - 375 <= MENU_MOUSE_POS[
                    0] <= WIDTH / 2 + 375 and HEIGHT / 2 - 75 <= MENU_MOUSE_POS[
                    1] <= HEIGHT / 2 + 25:
                    if not isFirstLaunch:
                        Game(isReset=isReset)
                        pygame.mixer.music.stop()
                    else:
                        Tutorial(isReset=isReset)
                        pygame.mixer.music.stop()

                if WIDTH / 2 - 375 <= MENU_MOUSE_POS[
                    0] <= WIDTH / 2 + 375 and HEIGHT / 2 + 75 <= MENU_MOUSE_POS[
                    1] <= HEIGHT / 2 + 175:
                    Options(isReset=isReset, isFirstLaunch=isFirstLaunch)
                if WIDTH / 2 - 375 <= MENU_MOUSE_POS[
                    0] <= WIDTH / 2 + 375 and HEIGHT / 2 + 225 <= MENU_MOUSE_POS[
                    1] <= HEIGHT / 2 + 325:
                    Quit()

            # Play button
            if WIDTH / 2 - 375 <= MENU_MOUSE_POS[
                0] <= WIDTH / 2 + 375 and HEIGHT / 2 - 75 <= MENU_MOUSE_POS[
                1] <= HEIGHT / 2 + 25:
                pygame.draw.rect(screen, COLOR_LIGHT,
                                 [WIDTH / 2 - 375, HEIGHT / 2 - 75, 750, 100], 4)
            else:
                pygame.draw.rect(screen, COLOR_DARK,
                                 [WIDTH / 2 - 375, HEIGHT / 2 - 75, 750, 100], 4)

            # Settings
            if WIDTH / 2 - 375 <= MENU_MOUSE_POS[
                0] <= WIDTH / 2 + 375 and HEIGHT / 2 + 75 <= MENU_MOUSE_POS[
                1] <= HEIGHT / 2 + 175:
                pygame.draw.rect(screen, COLOR_LIGHT,
                                 [WIDTH / 2 - 375, HEIGHT / 2 + 75, 750, 100], 4)
            else:
                pygame.draw.rect(screen, COLOR_DARK,
                                 [WIDTH / 2 - 375, HEIGHT / 2 + 75, 750, 100], 4)

            # Quit button
            if WIDTH / 2 - 375 <= MENU_MOUSE_POS[
                0] <= WIDTH / 2 + 375 and HEIGHT / 2 + 225 <= MENU_MOUSE_POS[
                1] <= HEIGHT / 2 + 325:
                pygame.draw.rect(screen, COLOR_LIGHT,
                                 [WIDTH / 2 - 375, HEIGHT / 2 + 225, 750, 100], 4)
            else:
                pygame.draw.rect(screen, COLOR_DARK,
                                 [WIDTH / 2 - 375, HEIGHT / 2 + 225, 750, 100], 4)

        pygame.display.flip()


# Tutorial menu.
def Tutorial(isReset):
    screen.fill((0, 0, 0))
    screen.blit(BACKGROUND_MISSION_ONE.convert(), (0, -2624))
    Utils.draw_rect_alpha(screen, (0, 0, 0, 105), (WIDTH / 2 - 500, HEIGHT / 2 - 250, 1000, 500))

    MENU_TEXT = get_font(int(HEIGHT / 30)).render("Обучение", True, (255, 255, 255))
    MENU_TEXT.set_alpha(200)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 230))
    screen.blit(MENU_TEXT, MENU_RECT)

    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("Управление:", True, (255, 200, 200))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 200))
    screen.blit(MAIN_TEXT, MAIN_RECT)
    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("W или клавиша 'стрелка вверх' - пролететь вперёд", True,
                                                            (230, 230, 230))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 176))
    screen.blit(MAIN_TEXT, MAIN_RECT)
    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("A или клавиша 'стрелка влево' - пролететь влево", True,
                                                            (230, 230, 230))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 148))
    screen.blit(MAIN_TEXT, MAIN_RECT)
    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("S или клавиша 'стрелка вниз' - пролететь назад", True,
                                                            (230, 230, 230))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 122))
    screen.blit(MAIN_TEXT, MAIN_RECT)
    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("D или клавиша 'стрелка вправо' - пролететь вправо", True,
                                                            (230, 230, 230))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 96))
    screen.blit(MAIN_TEXT, MAIN_RECT)
    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("ЛКМ или ПКМ - выстрел из оружия", True, (230, 210, 210))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 70))
    screen.blit(MAIN_TEXT, MAIN_RECT)

    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("Стреляйте из оружия по инопланетянам, ", True,
                                                            (200, 200, 210))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 0))
    screen.blit(MAIN_TEXT, MAIN_RECT)
    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("продержитесь наибольшее количество времени.", True,
                                                            (200, 200, 210))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 26))
    screen.blit(MAIN_TEXT, MAIN_RECT)

    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("У вас всего 3 жизни.", True, (200, 200, 210))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 80))
    screen.blit(MAIN_TEXT, MAIN_RECT)
    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("После каждого столкновения инопланетяне разлетаются.",
                                                            True,
                                                            (200, 200, 210))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 106))
    screen.blit(MAIN_TEXT, MAIN_RECT)

    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("Удачной игры!", True, (200, 200, 210))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 163))
    screen.blit(MAIN_TEXT, MAIN_RECT)

    MAIN_TEXT = get_font(int(HEIGHT / 30)).render("Нажмите любую кнопку, чтобы начать игру.", True,
                                                            (200, 220, 200))
    MAIN_TEXT.set_alpha(200)
    MAIN_RECT = MAIN_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 220))
    screen.blit(MAIN_TEXT, MAIN_RECT)

    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            # We are closing our game using the button.
            if event.type == pygame.QUIT:
                RUNNING = False
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                RUNNING = False
                Game(isReset=isReset)
            if event.type == pygame.MOUSEBUTTONDOWN:
                RUNNING = False
                Game(isReset=isReset)
        pygame.display.flip()


# Level selection menu.
def LevelSelect():
    e = 1


# Options menu.
def Options(isReset, isFirstLaunch):
    # Do backend config creation.
    Configuration.createConfig()

    screen.fill((0, 0, 0))
    screen.blit(BACKGROUND_MAINMENU.convert(), (0, 0))
    Utils.draw_rect_alpha(screen, (0, 0, 0, 105), (WIDTH / 2 - 500, HEIGHT / 2 - 250, 1000, 500))
    RUNNING = True

    SETTINGS_TEXT = get_font(int(HEIGHT / 20)).render("Настройки игры", True, (255, 255, 255))
    SETTINGS_TEXT.set_alpha(200)
    SETTINGS_TEXT_RECT = SETTINGS_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 225))
    screen.blit(SETTINGS_TEXT, SETTINGS_TEXT_RECT)

    MUSIC_VOLUME_TEXT = get_font(int(HEIGHT / 20)).render("Громкость музыки:", True, (255, 255, 255))
    MUSIC_VOLUME_TEXT.set_alpha(200)
    MUSIC_VOLUME_RECT = MUSIC_VOLUME_TEXT.get_rect(center=(WIDTH / 2 - 240, HEIGHT / 2 - 165))
    screen.blit(MUSIC_VOLUME_TEXT, MUSIC_VOLUME_RECT)

    SETTINGS_TEXT = get_font(int(HEIGHT / 20)).render("Громкость звуков:", True, (255, 255, 255))
    SETTINGS_TEXT.set_alpha(200)
    MENU_RECT = SETTINGS_TEXT.get_rect(center=(WIDTH / 2 - 240, HEIGHT / 2 - 125))
    screen.blit(SETTINGS_TEXT, MENU_RECT)

    sliderMusicVolume = Slider(screen, int(WIDTH / 2 + 50), int(HEIGHT / 2 - 180), 350, 25, min=0,
                               max=100, step=1,
                               handleRadius=10, initial=getField("MUSIC_VOLUME"))
    sliderSoundVolume = Slider(screen, int(WIDTH / 2 + 50), int(HEIGHT / 2 - 140), 350, 25, min=0,
                               max=100, step=1,
                               handleRadius=10, initial=getField("SFX_VOLUME"))
    outputMusicVolume = TextBox(screen, int(WIDTH / 2 + 50 + 370), int(HEIGHT / 2 - 182.5), 62, 30,
                                font=pygame.font.Font(os.path.join(FONTS, "FONT.TTF"), 20),
                                borderColour=COLOR_DARK, textColour=COLOR_DARKER)
    outputMusicVolume.disable()
    outputSoundVolume = TextBox(screen, int(WIDTH / 2 + 50 + 370), int(HEIGHT / 2 - 142.5), 62, 30,
                                font=pygame.font.Font(os.path.join(FONTS, "FONT.TTF"), 20),
                                borderColour=COLOR_DARK, textColour=COLOR_DARKER)
    outputSoundVolume.disable()

    ButtonToMainMenu = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        int(WIDTH / 2 - 500 + 250),  # X-coordinate of top left corner
        570,  # Y-coordinate of top left corner
        500,  # Width
        50,  # Height

        # Optional Parameters
        text='В главное меню',  # Text to display
        font=pygame.font.Font(os.path.join(FONTS, "FONT.TTF"), 30),
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=COLOR_DARK,  # Colour of button when not being interacted with
        hoverColour=COLOR_LIGHT,  # Colour of button when being hovered over
        pressedColour=COLOR_DARKER,  # Colour of button when being clicked
        onClick=lambda: ButtonSettingsWrapper(isReset=isReset,
                                              isFirstLaunch=isFirstLaunch,
                                              resetMusic=False,
                                              musicVolume=sliderMusicVolume.getValue(),
                                              soundVolume=sliderSoundVolume.getValue(),
                                              modifiers=[4, 2, 0.1])  # Function to call when clicked on
    )

    while RUNNING:
        outputMusicVolume.setText(sliderMusicVolume.getValue())
        outputSoundVolume.setText(sliderSoundVolume.getValue())

        pygame.mixer.music.set_volume(sliderMusicVolume.getValue() / 100)

        events = pygame.event.get()
        for event in events:
            # We are closing our game using the button.
            if event.type == pygame.QUIT:
                pygame.quit()
                RUNNING = False
                pygame.display.quit()

        pygame_widgets.update(events)
        pygame.display.update()


# Game Process function, game logic and all the processing goes here.
def Game(isReset):
    pygame.mixer.music.load(os.path.join(MUSIC, "MISSION1.OGG"))
    pygame.mixer.music.set_volume(getField("MUSIC_VOLUME") / 100)
    pygame.mixer.music.play(loops=-1)

    global score
    killcounter = 0
    lifecounter = 3
    dead = False
    if isReset:
        PLAYER.rect = PLAYER.image.get_rect()
        PLAYER.rect.centerx = WIDTH / 2
        PLAYER.rect.bottom = HEIGHT - 10
        SPRITES.empty()
        MOBS.empty()
        killcounter = 0
        lifecounter = 3
        dead = False

    SPRITES.add(PLAYER)

    KILLS_TEXT = get_font(int(HEIGHT / 30)).render("Уничтожено:", True, (255, 255, 255))
    KILLS_TEXT.set_alpha(260)
    KILLS_TEXT_RECT = KILLS_TEXT.get_rect(center=(120, 45))

    KILLS_COUNT = get_font(int(HEIGHT / 30)).render(f"{killcounter}", True, (255, 80, 0))
    KILLS_COUNT.set_alpha(260)
    KILLS_COUNT_RECT = KILLS_COUNT.get_rect(center=(250 + len(str(killcounter)) * 7, 45))

    LIVES_TEXT = get_font(int(HEIGHT / 30)).render("Жизни:", True, (255, 255, 255))
    LIVES_TEXT.set_alpha(260)
    LIVES_TEXT_RECT = LIVES_TEXT.get_rect(center=(120 + len(str(killcounter)) * 7, 95))

    LIVES_COUNT = get_font(int(HEIGHT / 30)).render(f"{lifecounter}", True, (255, 80, 0))
    LIVES_COUNT.set_alpha(260)
    LIVES_COUNT_RECT = LIVES_COUNT.get_rect(center=(250 + len(str(killcounter)) * 7, 95))

    ANYKEY_TEXT = get_font(int(HEIGHT / 35)).render("Нажмите любую кнопку, чтобы вернуться в главное меню.",
                                                              True, (255, 10, 10))
    ANYKEY_TEXT.set_alpha(140)
    ANYKEY_TEXT_RECT = ANYKEY_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 80))

    DEATH_TEXT = get_font(int(HEIGHT / 15)).render("Вы проиграли. :(", True, (255, 10, 10))
    DEATH_TEXT.set_alpha(140)
    DEATH_RECT = DEATH_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    reverse = False
    background_y = 0
    RUNNING = True
    while RUNNING:
        screen.fill((0, 0, 0))
        screen.blit(BACKGROUND_MISSION_ONE.convert(), (0, -2624 + background_y))
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            # We are closing our game using the button.
            if event.type == pygame.QUIT:
                RUNNING = False
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not dead:
                    PLAYER.shoot()

        for i in range(1):
            rand = random.randrange(1, 1000)
            if (rand < 25):
                MOB = Mob()
                SPRITES.add(MOB)
                MOBS.add(MOB)

        hits = pygame.sprite.groupcollide(MOBS, BULLETS, True, True)
        for _ in hits:
            m = Mob()
            SPRITES.add(m)
            MOBS.add(m)
            explosion = Explosion(_.rect.center, 75)
            EXPLOSIONS.add(explosion)
            EXPLOSION_SOUND.set_volume(getField("SFX_VOLUME") / 100)
            EXPLOSION_SOUND.play()
            killcounter += 1
            KILLS_COUNT = get_font(int(HEIGHT / 30)).render(f"{killcounter}", True, (255, 80, 0))

        SPRITES.update()
        EXPLOSIONS.update()

        hits = pygame.sprite.spritecollide(PLAYER, MOBS, False)
        if hits:
            lifecounter -= 1
            PLAYER.rect.centerx = WIDTH / 2
            PLAYER.rect.bottom = HEIGHT - 10
            explosion = Explosion(hits[0].rect.center, 800)
            EXPLOSIONS.add(explosion)
            EXPLOSION_SOUND.set_volume(getField("SFX_VOLUME") / 100 + 0.5)
            EXPLOSION_SOUND.play()
            SPRITES.empty()
            SPRITES.add(PLAYER)
            MOBS.empty()
            LIVES_COUNT = get_font(int(HEIGHT / 30)).render(f"{lifecounter}", True, (255, 80, 0))

            if lifecounter <= 0:
                dead = True

                if score == 0:
                    score = killcounter
                elif killcounter > score:
                    score = killcounter

                BEST_SCORE_TEXT = get_font(int(HEIGHT / 35)).render(f"Ваш лучший результат: {score}",
                                                                              True, (255, 10, 10))
                BEST_SCORE_TEXT.set_alpha(140)
                BEST_SCORE_RECT = BEST_SCORE_TEXT.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))

        if not dead:
            SPRITES.draw(screen)
            EXPLOSIONS.draw(screen)

            screen.blit(KILLS_COUNT, KILLS_COUNT_RECT)
            screen.blit(KILLS_TEXT, KILLS_TEXT_RECT)
            screen.blit(LIVES_COUNT, LIVES_COUNT_RECT)
            screen.blit(LIVES_TEXT, LIVES_TEXT_RECT)

            pygame.display.flip()
            if not reverse:
                background_y += 0.1
            if background_y >= 2624:
                reverse = True
            if reverse:
                background_y -= 0.1
            if background_y <= 0:
                reverse = False
        else:
            SPRITES.draw(screen)
            EXPLOSIONS.draw(screen)

            screen.blit(DEATH_TEXT, DEATH_RECT)
            screen.blit(BEST_SCORE_TEXT, BEST_SCORE_RECT)
            screen.blit(ANYKEY_TEXT, ANYKEY_TEXT_RECT)

            SPRITES.remove(PLAYER)
            MOBS.empty()

            pygame.display.flip()

            for event in pygame.event.get():
                # We are closing our game using the button.
                if event.type == pygame.QUIT:
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    RUNNING = False
                    MainMenu(isReset=True, isFirstLaunch=False, resetMusic=True)
                    pygame.mixer.music.stop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    RUNNING = False
                    MainMenu(isReset=True, isFirstLaunch=False, resetMusic=True)
                    pygame.mixer.music.stop()


# Constructor-callback to quit the whole game.
def Quit():
    pygame.display.quit()
    pygame.quit()
    # We don't need to throw an exception when quitting and crashing the whole runtime, we're quitting the game.
    exit(-1)


# Запуск игры.
MainMenu(isReset=False, isFirstLaunch=True, resetMusic=True)
