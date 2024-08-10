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

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

game_over = False
game_clear = False

timer = 0

bomb_num = 50


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


def set_up():
    field = []
    for row in range(row_num):
        tile_list = []
        for col in range(col_num):
            tile = Tile((col * tile_size, row * tile_size), images["empty_block"])
            tile_list.append(tile)
        field.append(tile_list)
    
    count = 0
    while count < bomb_num:
        x = random.randint(0, col_num - 1)
        y = random.randint(0, row_num - 1)
        tile = field[y][x]
        if tile.bomb == False:
            tile.bomb = True
            tile.neighbor_bomb_num = -1
            count += 1
    
    for row_index, tile_list in enumerate(field):
        for col_index, tile in enumerate(tile_list):
            if tile.bomb:
                for y_offset in range(-1, 2):
                    for x_offset in range(-1, 2):
                        x_pos = col_index + x_offset
                        y_pos = row_index + y_offset
                        if 0 <= x_pos < col_num and 0 <= y_pos < row_num and field[y_pos][x_pos].bomb == False:
                            field[y_pos][x_pos].neighbor_bomb_num += 1
    return field

field = set_up()

def open_tile(x, y, field):
    if field[y][x].check:
        return
    
    field[y][x].check = True
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            col = x + x_offset
            row = y + y_offset
            if 0 <= col < col_num and 0 <= row < row_num and field[row][col].image != images["flag"]:
                field[row][col].open = True
                if field[row][col].neighbor_bomb_num == 0:
                    open_tile(col, row, field)


run = True
while run:
    screen.fill(WHITE)
    
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over == False and game_clear == False:
                for tile_list in field:
                    for tile in tile_list:
                        if tile.rect.collidepoint((mx, my)):
                            if event.button == 1:
                                if tile.image != images["flag"]:
                                    tile.open = True
                                    if tile.neighbor_bomb_num == 0 and tile.bomb == False:
                                        x = mx // tile_size
                                        y = my // tile_size
                                        open_tile(x, y, field)
                                if tile.open and tile.image != images["0"]:
                                    flag_num = 0
                                    x = mx // tile_size
                                    y = my// tile_size
                                    for y_offset in range(-1, 2):
                                        for x_offset in range(-1, 2):
                                            col = x + x_offset
                                            row = y + y_offset
                                            if 0 <= col < col_num and 0 <= row < row_num and field[row][col].image == images["flag"]:
                                                flag_num += 1
                                    if flag_num == tile.neighbor_bomb_num and tile.bomb == False:
                                        open_tile(x, y, field)
                            if event.button == 3 and tile.open == False:
                                if tile.image == images["empty_block"]:
                                    tile.image = images["flag"]
                                else:
                                    tile.image = images["empty_block"]
            else:
                field = set_up()
                game_over = False
                game_clear = False
                timer = 0
    
    open_num = 0
    for tile_list in field:
        for tile in tile_list:
            if tile.open:
                if tile.bomb:
                    tile.image = images["click_bomb"]
                else:
                    tile.image = images[f"{tile.neighbor_bomb_num}"]
            screen.blit(tile.image,tile.position)
            if tile.bomb and tile.open and game_clear == False:
                game_over = True
            if tile.open:
                open_num += 1
                if (row_num*col_num) - bomb_num == open_num and game_over == False:
                    game_clear = True
    
    if game_over:
        timer += 1
        if timer > 30:
            screen.blit(game_over_text,(125,200))
            screen.blit(reset_text,(125,400))
    elif game_clear:
        screen.blit(game_clear_text,(125,200))
        screen.blit(reset_text,(125,400))
    
    pygame.display.update()

pygame.quit()











