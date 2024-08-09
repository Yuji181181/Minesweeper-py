import pygame
pygame.init()
from tile import Tile
from os import walk
import random

col_num = 20
row_num = 20
tile_size = 40

screen_width = col_num*tile_size
screen_height = row_num*tile_size
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Minesweeper.py")

bomb_num = 50

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

game_over = False
game_clear = False

timer = 0

images = {}
path = "assets/img"
for _, __, img_files in walk(path):
    for image in img_files:
        full_path = path + "/" + image
        img = pygame.image.load(full_path)
        img = pygame.transform.scale(img, (tile_size,tile_size))
        images[image.split(".")[0]] = img

font = pygame.font.SysFont(None, 130)
game_over_text = font.render("Game Over...",True,BLUE,GREEN)
game_clear_text = font.render("Game Clear", True,RED,GREEN)
reset_text = font.render("click to reset",True,BLACK,GREEN)



field = set_up()




run = True
while run:

    screen.fill(WHITE)
    
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    
    
    
    pygame.display.update()

pygame.quit()











