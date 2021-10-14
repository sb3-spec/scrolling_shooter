import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * .8)
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
SCROLL_THRESH = 200
GRAVITY = .4
screen_scroll = 0
bg_scroll = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))