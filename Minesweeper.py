import pygame
pygame.init()
from tile import Tile
from os import walk
import random

row_num = 20
col_num = 20
tile_size = 40
bomb_num = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_over = False
game_clear = False

timer = 0