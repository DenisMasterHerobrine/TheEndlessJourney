import os

import pygame

# This is a main class of the game, it does all the processing that the game requires.

# GAME SETTINGS PARAMETERS
# TODO: move this to SETTINGS.CFG file in specific savegame directory
from pygame import DOUBLEBUF, RESIZABLE, HWSURFACE, VIDEORESIZE

WIDTH = 1920
HEIGHT = 1080
FPS = 144

VERSION = "v0.10"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Basic PyGame window implementation
# Launch the game initializer.
pygame.init()

# Start the sound mixer engine.
pygame.mixer.init()

# Create a display with custom WIDTH and HEIGHT.
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)

# Set the game window title.
pygame.display.set_caption("The Endless Journey " + VERSION)

# Clock engine initialization.
CLOCK = pygame.time.Clock()
SPRITES = pygame.sprite.Group()

# Game Assets initialization.
GAME_DIR = os.path.dirname(__file__)
SPRITES_DIR = os.path.join(os.path.join(GAME_DIR, 'assets'), 'sprites')
BACKGROUNDS = os.path.join(os.path.join(GAME_DIR, 'assets'), 'bitmaps')
FONTS = os.path.join(os.path.join(GAME_DIR, 'assets'), 'fonts')

PLAYER_SPACESHIP_SPRITE = pygame.image.load(
    os.path.join(os.path.join(SPRITES_DIR, 'spaceship'), 'SMALL_BLUE_SPIKED_SHIP.PNG')).convert()
BACKGROUND_MAINMENU = pygame.image.load(
    os.path.join(BACKGROUNDS, 'MAINMENU.PNG')).convert()
BACKGROUND_MAINMENU = pygame.transform.scale(BACKGROUND_MAINMENU, (WIDTH, WIDTH * 2.15))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = PLAYER_SPACESHIP_SPRITE
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        # Управление стрелочками:
        if keystate[pygame.K_LEFT]:
            self.speedx = -4
        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
        if keystate[pygame.K_UP]:
            self.speedy = -4
        if keystate[pygame.K_DOWN]:
            self.speedy = 4

        # WASD управление:
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

        # Быть в пределах экрана:
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


PLAYER = Player()
SPRITES.add(PLAYER)

def get_font(size):
    return pygame.font.Font(os.path.join(FONTS, "FONT.TTF"), size)


def MainMenu():
    RUNNING = True;
    screen.blit(BACKGROUND_MAINMENU, (0, 0))


    MENU_TEXT = get_font(int(HEIGHT / 10)).render("The Endless Journey", True, (0, 0, 0))
    MENU_TEXT.set_alpha(125)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

    screen.blit(MENU_TEXT, MENU_RECT)
    pygame.display.flip()

    while RUNNING:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # We are closing our game using the button.
            if event.type == pygame.QUIT:
                RUNNING = False
                pygame.display.quit()
                pygame.quit()
            if event.type == VIDEORESIZE:
                screen.blit(pygame.transform.scale(BACKGROUND_MAINMENU, event.dict['size']), (0, 0))
                pygame.display.flip()


def LevelSelect():
    e = 1


def Options():
    e = 1


def Game():
    RUNNING = True;
    while RUNNING:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            # We are closing our game using the button.
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()

        SPRITES.update()

        screen.fill((0, 0, 0))
        SPRITES.draw(screen)
        pygame.display.flip()


MainMenu()
