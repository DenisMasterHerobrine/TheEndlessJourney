import os

import pygame

# This is a main class of the game, it does all the processing that the game requires.

# GAME SETTINGS PARAMETERS
# TODO: move this to SETTINGS.CFG file in specific savegame directory
from pygame import DOUBLEBUF, HWSURFACE

WIDTH = 1366
HEIGHT = 768
FPS = 144

VERSION = "v0.10"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# light shade of the button
COLOR_LIGHT = (170, 170, 170)

# dark shade of the button
COLOR_DARK = (100, 100, 100)


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


# Basic PyGame window implementation
# Launch the game initializer.
pygame.init()

# Start the sound mixer engine.
pygame.mixer.init()

# Create a display with custom WIDTH and HEIGHT.
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF)

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

PLAYER_SPACESHIP_SPRITE = pygame.image.load(os.path.join(os.path.join(SPRITES_DIR, 'spaceship'), 'SMALL_BLUE_SPIKED_SHIP.PNG')).convert()

BACKGROUND_MAINMENU = pygame.image.load(os.path.join(BACKGROUNDS, 'MAINMENU.PNG')).convert()
BACKGROUND_MISSION_ONE = pygame.image.load(os.path.join(BACKGROUNDS, 'MISSION1.PNG')).convert()

BACKGROUND_MAINMENU = pygame.transform.scale(BACKGROUND_MAINMENU, (WIDTH, WIDTH * 2.15))
BACKGROUND_MISSION_ONE = pygame.transform.scale(BACKGROUND_MISSION_ONE, (WIDTH, WIDTH * 2.5))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = PLAYER_SPACESHIP_SPRITE
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

    PLAY_TEXT = get_font(int(HEIGHT / 10)).render("Play", True, (0, 0, 0))
    PLAY_TEXT.set_alpha(125)
    PLAY_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2 + 425, HEIGHT / 2 - 17.5))

    OPTIONS_TEXT = get_font(int(HEIGHT / 10)).render("Options", True, (0, 0, 0))
    OPTIONS_TEXT.set_alpha(125)
    OPTIONS_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2 + 337.5, HEIGHT / 2 + 132.5))

    QUIT_TEXT = get_font(int(HEIGHT / 10)).render("Quit", True, (0, 0, 0))
    QUIT_TEXT.set_alpha(125)
    QUIT_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2 + 425, HEIGHT / 2 + 282.5))

    draw_rect_alpha(screen, (100, 100, 100, 100), (WIDTH / 2 - 375, HEIGHT / 2 - 75, 750, 100))
    draw_rect_alpha(screen, (100, 100, 100, 100), (WIDTH / 2 - 375, HEIGHT / 2 + 75, 750, 100))
    draw_rect_alpha(screen, (100, 100, 100, 100), (WIDTH / 2 - 375, HEIGHT / 2 + 225, 750, 100))

    screen.blit(MENU_TEXT, MENU_RECT)
    screen.blit(PLAY_TEXT, PLAY_RECT)
    screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
    screen.blit(QUIT_TEXT, QUIT_RECT)

    while RUNNING:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # We are closing our game using the button.
            if event.type == pygame.QUIT:
                RUNNING = False
                pygame.display.quit()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH / 2 - 375 <= MENU_MOUSE_POS[0] <= WIDTH / 2 + 375 and HEIGHT / 2 - 75 <= MENU_MOUSE_POS[1] <= HEIGHT / 2 + 25:
                    Game()
                if WIDTH / 2 - 375 <= MENU_MOUSE_POS[0] <= WIDTH / 2 + 375 and HEIGHT / 2 + 75 <= MENU_MOUSE_POS[1] <= HEIGHT / 2 + 175:
                    Options()
                if WIDTH / 2 - 375 <= MENU_MOUSE_POS[0] <= WIDTH / 2 + 375 and HEIGHT / 2 + 225 <= MENU_MOUSE_POS[1] <= HEIGHT / 2 + 325:
                    Quit()

            # Debug
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(MENU_MOUSE_POS)

            # Play button
            if WIDTH / 2 - 375 <= MENU_MOUSE_POS[0] <= WIDTH / 2 + 375 and HEIGHT / 2 - 75 <= MENU_MOUSE_POS[1] <= HEIGHT / 2 + 25:
                pygame.draw.rect(screen, COLOR_LIGHT, [WIDTH / 2 - 375, HEIGHT / 2 - 75, 750, 100], 4)
            else:
                pygame.draw.rect(screen, COLOR_DARK, [WIDTH / 2 - 375, HEIGHT / 2 - 75, 750, 100], 4)

            # Settings
            if WIDTH / 2 - 375 <= MENU_MOUSE_POS[0] <= WIDTH / 2 + 375 and HEIGHT / 2 + 75 <= MENU_MOUSE_POS[1] <= HEIGHT / 2 + 175:
                pygame.draw.rect(screen, COLOR_LIGHT, [WIDTH / 2 - 375, HEIGHT / 2 + 75, 750, 100], 4)
            else:
                pygame.draw.rect(screen, COLOR_DARK, [WIDTH / 2 - 375, HEIGHT / 2 + 75, 750, 100], 4)

            # Quit button
            if WIDTH / 2 - 375 <= MENU_MOUSE_POS[0] <= WIDTH / 2 + 375 and HEIGHT / 2 + 225 <= MENU_MOUSE_POS[1] <= HEIGHT / 2 + 325:
                pygame.draw.rect(screen, COLOR_LIGHT, [WIDTH / 2 - 375, HEIGHT / 2 + 225, 750, 100], 4)
            else:
                pygame.draw.rect(screen, COLOR_DARK, [WIDTH / 2 - 375, HEIGHT / 2 + 225, 750, 100], 4)

        pygame.display.flip()


def LevelSelect():
    e = 1


def Options():
    e = 1


def Game():
    reverse = False
    background_y = 0;
    RUNNING = True;
    while RUNNING:
        screen.fill((0, 0, 0))
        screen.blit(BACKGROUND_MISSION_ONE, (0, -2624 + background_y))
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            # We are closing our game using the button.
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()

        SPRITES.update()
        SPRITES.draw(screen)
        pygame.display.flip()
        if not reverse:
            background_y += 0.1
        if background_y == 2624:
            reverse = True
        if reverse:
            background_y -= 0.1
        if background_y == 0:
            reverse = False


def Quit():
    pygame.display.quit()
    pygame.quit()


MainMenu()
